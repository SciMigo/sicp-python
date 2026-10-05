// End-to-end check of the browser lab in headless Chromium.
//
//   node tools/preview_smoke.mjs [module-id] [--all] [--root DIR] [--out DIR]
//
// Serves the repository with `python3 -m http.server`, opens /preview/?module=<id> (default: the
// first module in modules/index.json), waits for Pyodide, and for the first exercise (every
// exercise with --all) replaces the code with the exercise's solution, runs it, steps the frame
// slider, answers the questions, and checks that Check my work ticks every step. Then it opens
// the lab embedded (embed=1) and with the lab supplied by a host page (lab=host). Screenshots go
// to --out as preview-<id>-<n>.png. Playwright comes from scimigo-learn's node_modules unless
// PLAYWRIGHT points elsewhere.
import { spawn } from 'node:child_process';
import { readFileSync, existsSync, mkdirSync } from 'node:fs';
import { createServer } from 'node:net';
import { tmpdir } from 'node:os';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const repoRoot = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const defaultPlaywright = path.resolve(repoRoot, '..', 'scimigo-learn', 'node_modules', 'playwright');
const { chromium } = require(process.env.PLAYWRIGHT ?? defaultPlaywright);

const args = process.argv.slice(2);
const option = (name, fallback) => {
  const index = args.indexOf(name);
  return index >= 0 ? args.splice(index, 2)[1] : fallback;
};
const root = path.resolve(option('--root', repoRoot));
const outDir = option('--out', path.join(tmpdir(), 'sicp-python-preview-smoke'));
const all = args.includes('--all');
const runtimeQuery = args.includes('--local-runtime') ? '&runtime=local' : '';
const moduleArg = args.find((arg) => !arg.startsWith('--'));
mkdirSync(outDir, { recursive: true });

const index = JSON.parse(readFileSync(path.join(root, 'modules/index.json'), 'utf8'));
const moduleId = moduleArg ?? index[0]?.id;
if (!moduleId) throw new Error('modules/index.json lists no module; run tools/build_preview_index.py');
const lab = JSON.parse(readFileSync(path.join(root, 'modules', moduleId, 'lab.json'), 'utf8'));
const solutionsPath = path.join(root, 'modules', moduleId, 'lab_solutions.json');
const solutions = existsSync(solutionsPath) ? JSON.parse(readFileSync(solutionsPath, 'utf8')) : {};
const solutionOf = (exercise) => exercise.solution ?? solutions[exercise.exercise_id];

const failures = [];
const expect = (condition, message) => {
  if (!condition) failures.push(message);
  console.log(`${condition ? '  ok  ' : '  FAIL'} ${message}`);
};
let shot = 0;
const screenshot = async (page, label) => {
  const file = path.join(outDir, `preview-${moduleId}-${++shot}.png`);
  await page.screenshot({ path: file, fullPage: true });
  console.log(`  shot ${file} (${label})`);
};

async function freePort() {
  return new Promise((resolve) => {
    const server = createServer().listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      server.close(() => resolve(port));
    });
  });
}

const port = await freePort();
const base = `http://127.0.0.1:${port}`;
const server = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', root], { stdio: 'ignore' });
for (let tries = 0; ; tries++) {
  try {
    if ((await fetch(`${base}/preview/`)).ok) break;
  } catch {
    if (tries > 50) throw new Error('The static server did not start');
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
}

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_EXECUTABLE_PATH });
try {
  const context = await browser.newContext({ viewport: { width: 1360, height: 900 } });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (error) => errors.push(String(error)));
  page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });

  const idle = () => page.waitForFunction(() => !document.getElementById('run').disabled
    && !/^(Running|Checking)…/.test(document.getElementById('feedback').textContent), null, { timeout: 60000 });
  // Distinct colours on the canvas: 0 is blank; an empty figure panel gives only a few.
  const canvasColours = () => page.evaluate(() => {
    const canvas = document.getElementById('picture');
    const data = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data;
    const colours = new Set();
    for (let i = 0; i < data.length; i += 16) if (data[i + 3]) colours.add(`${data[i]},${data[i + 1]},${data[i + 2]}`);
    return colours.size;
  });

  console.log(`module ${moduleId} at ${base}/preview/`);
  const exercises = all ? lab.exercises : lab.exercises.slice(0, 1);
  for (const [position, exercise] of exercises.entries()) {
    const number = lab.exercises.indexOf(exercise) + 1;
    console.log(`exercise ${number}: ${exercise.exercise_id}`);
    await page.goto(`${base}/preview/?module=${moduleId}${runtimeQuery}&exercise=${number}`);
    if (position === 0) {
      await page.waitForSelector('#runtime.ready', { timeout: 180000 });
      expect(true, 'Pyodide ready');
    }
    await page.waitForFunction((title) => document.getElementById('title').textContent === title, exercise.title);
    await idle();
    const solution = solutionOf(exercise);
    if (typeof solution !== 'string') {
      expect(false, 'the exercise has a solution');
      continue;
    }
    // Replace the editor's text the way a learner would: select all, then type over it.
    await page.click('.cm-content');
    await page.keyboard.press('ControlOrMeta+A');
    await page.keyboard.press('Delete');
    await page.keyboard.insertText(solution);
    const draft = await page.evaluate((key) => localStorage.getItem(key), `preview:${lab.lab_spec_id}:${exercise.exercise_id}`);
    expect(draft === solution, 'editor holds the solution exactly');

    await page.click('#run');
    await idle();
    const feedbackBad = await page.$eval('#feedback', (el) => el.classList.contains('bad'));
    const consoleText = await page.$eval('#console', (el) => (el.hidden ? '' : el.textContent));
    expect(!feedbackBad, `Run succeeds${feedbackBad ? `: ${await page.textContent('#feedback')}\n${consoleText}` : ''}`);
    if (solution.includes('figure(')) {
      let colours = 0;
      for (let tries = 0; tries < 30 && colours < 8; tries++) {
        colours = await canvasColours();
        if (colours < 8) await page.waitForTimeout(200);
      }
      expect(colours >= 8, `figure drawn (${colours} colours on the canvas)`);
    } else {
      expect(await canvasColours() > 0 || !/canvas\(|rectangle\(|circle\(|text\(/.test(solution), 'canvas is not blank');
    }
    await screenshot(page, `exercise ${number} after Run`);
    if (/\bframe\(\)/.test(solution)) {
      expect(await page.isVisible('#frame-controls'), 'frame slider is visible');
      await page.click('#frame-prev');
      await page.$eval('#frame-slider', (slider) => {
        slider.value = '1';
        slider.dispatchEvent(new Event('input'));
      });
      await page.waitForTimeout(400);
      expect((await page.textContent('#frame-label')).startsWith('frame 1 /'), 'slider shows frame 1');
      expect(await canvasColours() > 0, 'frame 1 is not blank');
      await screenshot(page, `exercise ${number} at frame 1`);
    }
    if (exercise.title.startsWith('Mastery challenge:')) {
      expect(!(await page.isVisible('#questions')), 'mastery reasoning hidden before first Check');
      await page.click('#tests');
      await idle();
      expect(await page.isVisible('#questions'), 'first Check reveals mastery reasoning');
    }
    for (const [q, question] of (exercise.questions ?? []).entries()) {
      await page.click(`[data-question="${q}"] [data-choice="${question.answer}"]`);
    }
    await page.click('#tests');
    await idle();
    const steps = await page.$$eval('#task-steps li', (items) => items.map((item) => item.classList.contains('done')));
    const feedback = await page.textContent('#feedback');
    expect(steps.length > 0 && steps.every(Boolean), `every task step ticked (${steps.filter(Boolean).length}/${steps.length})${steps.every(Boolean) ? '' : `\n${feedback}`}`);
    await screenshot(page, `exercise ${number} after Check my work`);
  }

  console.log('embedded (embed=1)');
  const embedded = await context.newPage();
  await embedded.addInitScript(() => {
    window.__messages = [];
    addEventListener('message', (event) => { if (event.data?.source === 'scimigo-visual-lab') window.__messages.push(event.data); });
  });
  await embedded.goto(`${base}/preview/?module=${moduleId}${runtimeQuery}&embed=1`);
  await embedded.waitForFunction(() => window.__messages.some((m) => m.type === 'ready'), null, { timeout: 180000 });
  const ready = await embedded.evaluate(() => window.__messages.find((m) => m.type === 'ready'));
  expect(ready.module === moduleId && ready.total === lab.exercises.length, `ready message names the module and ${lab.exercises.length} exercises`);
  expect(await embedded.evaluate(() => window.__messages.some((m) => m.type === 'height' && m.height > 0)), 'height message sent');
  expect(!(await embedded.isVisible('.topbar')) && !(await embedded.isVisible('#modules')), 'embed hides the header and module list');
  await embedded.waitForSelector('#runtime.ready', { timeout: 180000 });
  await embedded.waitForFunction(() => !document.getElementById('run').disabled, null, { timeout: 60000 });
  await screenshot(embedded, 'embedded');

  console.log('lab supplied by the host page (lab=host)');
  const publicLab = { ...lab, exercises: lab.exercises.map(({ solution, ...rest }) => rest) };
  const answers = Object.fromEntries(lab.exercises.map((exercise) => [exercise.exercise_id, solutionOf(exercise)]));
  // A fresh browser profile, so the lab opens on its first exercise rather than resuming.
  const hostContext = await browser.newContext({ viewport: { width: 1360, height: 900 } });
  await hostContext.route(`${base}/__host.html`, (route) => route.fulfill({ contentType: 'text/html', body: `<!doctype html>
<link rel="icon" href="data:,">
<iframe id="lab" style="width:1300px;height:1600px;border:0" src="/preview/?module=${moduleId}${runtimeQuery}&embed=1&lab=host"></iframe>
<script>
const lab = ${JSON.stringify(publicLab)};
const solutions = ${JSON.stringify(answers)};
window.__messages = [];
addEventListener('message', (event) => {
  const data = event.data;
  if (data?.source !== 'scimigo-visual-lab') return;
  window.__messages.push(data);
  const reply = (message) => event.source.postMessage({ source: 'scimigo-host', module: data.module, ...message }, location.origin);
  if (data.type === 'lab-request') reply({ type: 'lab', lab });
  if (data.type === 'solutions-request') reply({ type: 'solutions', solutions });
});
</script>` }));
  const host = await hostContext.newPage();
  host.on('pageerror', (error) => errors.push(String(error)));
  await host.goto(`${base}/__host.html`);
  await host.waitForFunction(() => window.__messages.some((m) => m.type === 'ready'), null, { timeout: 180000 });
  const frame = host.frame({ url: /lab=host/ });
  expect((await frame.textContent('#title')) === lab.exercises[0].title, 'host-supplied lab shows its first exercise');
  await frame.waitForSelector('#runtime.ready', { timeout: 180000 });
  await frame.waitForFunction(() => !document.getElementById('sample').disabled && !document.getElementById('run').disabled);
  await frame.click('#sample');
  await frame.waitForFunction(() => /replaced with the example/.test(document.getElementById('undo-message').textContent), null, { timeout: 30000 });
  expect(await host.evaluate(() => window.__messages.some((m) => m.type === 'solutions-request')), 'Replace with example asks the host for solutions');

  expect(errors.length === 0, `no page errors${errors.length ? `: ${errors.join(' | ')}` : ''}`);
} finally {
  await browser.close();
  server.kill();
}
console.log(failures.length ? `${failures.length} failure(s)` : 'all checks passed');
process.exit(failures.length ? 1 : 0);
