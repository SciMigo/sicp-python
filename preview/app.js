import { createPythonEditor } from './editor.bundle.js';

const $ = (id) => document.getElementById(id);
const ui = {
  modules: $('modules'), nav: $('exercises'), title: $('title'), prompt: $('prompt'), code: $('code'),
  moduleEyebrow: $('module-eyebrow'), moduleHeading: $('module-heading'), moduleSubtitle: $('module-subtitle'),
  runtime: $('runtime'), status: $('canvas-status'), canvas: $('picture'), canvasHint: $('canvas-hint'),
  feedback: $('feedback'), console: $('console'),
  run: $('run'), tests: $('tests'), stop: $('stop'), sample: $('sample'), reset: $('reset'),
  hintButton: $('hint-button'), hints: $('hints'),
  gameControls: $('game-controls'), play: $('play'), tickRate: $('tick-rate'), arrowPad: $('arrow-pad'),
  frameControls: $('frame-controls'), framePrev: $('frame-prev'), frameNext: $('frame-next'), frameSlider: $('frame-slider'), frameLabel: $('frame-label'),
  statePanel: $('state-panel'), stateValues: $('state-values'),
  moduleGuides: $('module-guides'), modulePanels: $('module-panels'),
  questions: $('questions'), questionList: $('question-list'),
  task: $('task'), taskProgress: $('task-progress'), taskSteps: $('task-steps'),
  recap: $('recap'), recapLearned: $('recap-learned'), recapReal: $('recap-real'), recapFacts: $('recap-facts'), recapRetrieval: $('recap-retrieval'), recapNext: $('recap-next'),
  undo: $('undo'), undoMessage: $('undo-message'), undoRestore: $('undo-restore'), undoDismiss: $('undo-dismiss'),
};

const COURSE_ID = 'sicp-python';
const COURSE_PATH = '/learn/sicp-python';
const searchParams = new URLSearchParams(location.search);
const embedded = searchParams.get('embed') === '1';
const requestedModule = searchParams.get('module');
if (embedded) document.documentElement.classList.add('embedded');
ui.modules.hidden = embedded;

// modules/index.json (tools/build_preview_index.py) lists the modules whose lab is served here.
const moduleChoices = await loadModuleIndex();
// ?lab=host (embedded only): the page around the frame fetches this module's lab through the
// signed-in API and hands it over, because a paid module's lab is never at a public URL. The
// lab then also describes the module, so a module this preview does not list can still open.
const labFromHost = embedded && searchParams.get('lab') === 'host' && /^\d{2}-[a-z0-9-]+$/.test(requestedModule ?? '');
const knownModule = moduleChoices.find((choice) => choice.id === requestedModule);
const selectedModule = knownModule
  ?? (labFromHost ? { id: requestedModule, label: `${Number(requestedModule.slice(0, 2))} · Lab`, eyebrow: '', heading: '', subtitle: '' } : moduleChoices[0]);

// On the live site the course page owns this lab; the bare preview redirects there.
if (!embedded && selectedModule && /(^|\.)scimigo\.com$/.test(location.hostname)) {
  location.replace(`${COURSE_PATH}/${selectedModule.id}`);
}

// Embedded in a course page (…/preview/?module=<id>&embed=1): the page owns the course header,
// module navigation and moving between modules. The frame reports its height and progress, and
// hands "continue" links to the page instead of following them itself.
const post = (message) => {
  if (embedded) parent.postMessage({ source: 'scimigo-visual-lab', ...message }, '*');
};
if (embedded) {
  let lastHeight = 0;
  const reportHeight = () => {
    const height = Math.ceil(document.documentElement.getBoundingClientRect().height);
    if (Math.abs(height - lastHeight) > 1) {
      lastHeight = height;
      post({ type: 'height', height });
    }
  };
  new ResizeObserver(reportHeight).observe(document.documentElement);
  addEventListener('load', reportHeight);
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href^="?module="]');
    if (!link) return;
    event.preventDefault();
    post({ type: 'navigate', module: new URLSearchParams(link.getAttribute('href').slice(1)).get('module') });
  });
}

// Requests to the host page, answered by postMessage. Only a trusted page may answer: a host lab
// can carry the module's panel code, which runs in this frame, so a page that merely framed the
// preview must not be able to supply one.
const hostReplies = new Map();
function trustedHost(origin) {
  if (origin === location.origin || /^https:\/\/(www\.)?scimigo\.com$/.test(origin)) return true;
  return /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin);
}
addEventListener('message', (event) => {
  if (event.source !== parent || !trustedHost(event.origin)) return;
  const data = event.data;
  if (!data || data.source !== 'scimigo-host' || data.module !== selectedModule?.id) return;
  const waiting = hostReplies.get(data.type);
  if (waiting) waiting(data);
});
function askHost(type, replyTypes, timeoutMs = 20000) {
  return new Promise((resolve) => {
    const done = (data) => {
      clearTimeout(timer);
      for (const reply of replyTypes) hostReplies.delete(reply);
      resolve(data);
    };
    const timer = setTimeout(() => done({ type: 'timeout' }), timeoutMs);
    for (const reply of replyTypes) hostReplies.set(reply, done);
    post({ type, module: selectedModule.id });
  });
}
const HOST_REFUSALS = {
  entitlement_required: 'This lab is part of the paid course. Unlock it on this page to start.',
  signin_required: 'Sign in to open this lab.',
};

async function labFromHostPage() {
  const reply = await askHost('lab-request', ['lab', 'lab-error']);
  if (reply.type === 'lab' && Array.isArray(reply.lab?.exercises)) return reply.lab;
  throw new Error(HOST_REFUSALS[reply.reason] ?? (reply.type === 'timeout'
    ? 'The lab did not arrive. Reload the page to try again.'
    : 'The lab could not load. Reload the page to try again.'));
}

// Solutions come from the lab itself, from the host page (lab=host), or from lab_solutions.json
// served beside the lab; they are fetched only when the learner asks for the example.
async function ensureSolution(exercise) {
  if (typeof exercise.solution === 'string') return true;
  let solutions = null;
  let reason;
  if (labFromHost) {
    const reply = await askHost('solutions-request', ['solutions', 'solutions-error']);
    if (reply.type === 'solutions') solutions = reply.solutions;
    reason = reply.reason;
  } else {
    try {
      const response = await fetch(`../modules/${selectedModule.id}/lab_solutions.json`);
      if (response.ok) solutions = await response.json();
    } catch {
      // No solutions are served for this module.
    }
  }
  if (solutions && typeof solutions === 'object') {
    for (const item of lab.exercises) {
      if (typeof solutions[item.exercise_id] === 'string') item.solution = solutions[item.exercise_id];
    }
  }
  if (typeof exercise.solution === 'string') return true;
  setFeedback(HOST_REFUSALS[reason] ?? 'No example is available for this exercise.', true);
  return false;
}

let lab;
let active = 0;
let worker;
let ready = false;
let busy = false;
let hasRun = false;
let acceptsClicks = false;
let acceptsKeys = false;
let scene = { width: 600, height: 400, objects: [] };
let displayed = scene;
let nextId = 1;
let pending = new Map();
let hintCount = 0;
let tickMs = null;
let playing = false;
let gameOver = false;
let tickTimer = null;
let frames = [];
let frameIndex = 0;
let extension = null;
let progress = { completed: [], steps: {}, checked: {}, answers: {} };
const editor = createPythonEditor(ui.code, saveDraft, runCode);

function setFeedback(message, bad = false) {
  ui.feedback.textContent = message;
  ui.feedback.classList.toggle('bad', bad);
  ui.feedback.classList.remove('passed');
}

function celebrate() {
  ui.feedback.classList.remove('passed');
  void ui.feedback.offsetWidth; // restart the animation on a repeat pass
  ui.feedback.classList.add('passed');
}

function setConsole(message, isError = false) {
  ui.console.textContent = message || '';
  ui.console.hidden = !message;
  ui.console.classList.toggle('error', isError);
}

function setButtons() {
  ui.run.disabled = !ready || busy;
  ui.tests.disabled = !ready || busy;
  ui.stop.disabled = !busy;
}

function setCanvasInteraction(enabled) {
  acceptsClicks = enabled;
  ui.canvas.classList.toggle('interactive', enabled);
  ui.canvasHint.textContent = enabled ? 'This program responds to clicks. Click the picture.' : '';
  ui.canvasHint.hidden = !enabled;
}

function startWorker() {
  ready = false;
  hasRun = false;
  setCanvasInteraction(false);
  worker = new Worker('./worker.js?v=1', { type: 'module' });
  ui.runtime.textContent = 'Loading Python…';
  ui.runtime.classList.remove('ready');
  setButtons();
  worker.onmessage = ({ data }) => {
    if (data.type === 'ready') {
      ready = true;
      ui.runtime.textContent = 'Python ready';
      ui.runtime.classList.add('ready');
      setButtons();
      if (lab) void runCode();
      return;
    }
    if (data.type === 'fatal') {
      ready = false;
      setButtons();
      setFeedback(`Python could not load: ${data.error}`, true);
      return;
    }
    const entry = pending.get(data.id);
    if (entry) {
      pending.delete(data.id);
      entry.resolve(data.result);
    }
  };
  worker.onerror = (event) => {
    ready = false;
    setButtons();
    setFeedback(`Python worker stopped: ${event.message}`, true);
  };
}

function request(type, payload) {
  return new Promise((resolve, reject) => {
    const id = nextId++;
    pending.set(id, { resolve, reject });
    worker.postMessage({ id, type, fixtures: lab?.fixtures, ...payload });
  });
}

// ---------------------------------------------------------------------------
// Drawing

function number(value, fallback = 0) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? Math.max(-2000, Math.min(2000, parsed)) : fallback;
}

// Figures arrive as SVG text. Each is decoded through an <img>, which never runs the SVG's
// scripts, so the markup needs no sanitising; it must never be inserted into the page as HTML.
const figureImages = new Map();
const FIGURE_CACHE_SIZE = 32;

function figureImage(svg) {
  let entry = figureImages.get(svg);
  if (entry) {
    figureImages.delete(svg); // most recently used goes last
    figureImages.set(svg, entry);
    return entry;
  }
  const url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
  entry = { image: new Image(), state: 'loading' };
  entry.image.onload = () => {
    entry.state = 'ready';
    URL.revokeObjectURL(url);
    render(displayed);
  };
  entry.image.onerror = () => {
    entry.state = 'failed';
    URL.revokeObjectURL(url);
    render(displayed);
  };
  entry.image.src = url;
  figureImages.set(svg, entry);
  while (figureImages.size > FIGURE_CACHE_SIZE) figureImages.delete(figureImages.keys().next().value);
  return entry;
}

function roundedRect(ctx, x, y, width, height, radius) {
  ctx.beginPath();
  ctx.roundRect(x, y, width, height, Math.min(radius, width / 2, height / 2));
}

function drawFigure(ctx, object, view) {
  const x = number(object.x);
  const y = number(object.y);
  const width = Math.max(1, number(object.width, 600));
  const height = Math.max(1, number(object.height, 400));
  ctx.save();
  roundedRect(ctx, x + 0.5, y + 0.5, width - 1, height - 1, 10);
  ctx.fillStyle = '#ffffff';
  ctx.fill();
  // A figure that fills the canvas sits inside the canvas frame; a smaller one gets its own edge.
  if (x > 0 || y > 0 || width < view.width || height < view.height) {
    ctx.strokeStyle = '#dcdfe8';
    ctx.stroke();
  }
  const entry = typeof object.svg === 'string' ? figureImage(object.svg) : { state: 'failed' };
  if (entry.state === 'ready') {
    const pad = Math.min(12, width / 10, height / 10);
    const natural = [entry.image.naturalWidth || width, entry.image.naturalHeight || height];
    const scale = Math.min((width - 2 * pad) / natural[0], (height - 2 * pad) / natural[1]);
    const [w, h] = [natural[0] * scale, natural[1] * scale];
    ctx.drawImage(entry.image, x + (width - w) / 2, y + (height - h) / 2, w, h);
  } else {
    ctx.fillStyle = '#8a90a2';
    ctx.font = '13px system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(entry.state === 'failed' ? 'This figure could not be drawn' : 'Drawing figure…', x + width / 2, y + height / 2);
  }
  ctx.restore();
}

// render() paints one view (the live picture or a recorded frame); draw() also makes it the live picture.
function render(view) {
  displayed = view;
  const width = number(view.width, 600);
  const height = number(view.height, 400);
  if (width <= 0 || height <= 0) return;
  const pixelRatio = Math.min(devicePixelRatio || 1, 2);
  ui.canvas.width = Math.round(width * pixelRatio);
  ui.canvas.height = Math.round(height * pixelRatio);
  ui.canvas.style.aspectRatio = `${width} / ${height}`;
  const ctx = ui.canvas.getContext('2d');
  ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  ctx.clearRect(0, 0, width, height);
  for (const object of (view.objects ?? []).slice(0, 500)) {
    const x = number(object.x);
    const y = number(object.y);
    ctx.fillStyle = typeof object.color === 'string' ? object.color : '#4b5bd6';
    if (object.kind === 'circle') {
      ctx.beginPath();
      ctx.arc(x, y, Math.max(0, number(object.radius)), 0, Math.PI * 2);
      ctx.fill();
    } else if (object.kind === 'rectangle') {
      ctx.fillRect(x, y, Math.max(0, number(object.width)), Math.max(0, number(object.height)));
    } else if (object.kind === 'text') {
      ctx.font = `600 ${Math.max(8, Math.min(64, number(object.size, 20)))}px system-ui, sans-serif`;
      ctx.fillText(String(object.value ?? '').slice(0, 200), x, y);
    } else if (object.kind === 'figure') {
      drawFigure(ctx, object, { width, height });
    }
  }
}

function draw(current) {
  scene = current ?? scene;
  render(scene);
  const count = (scene.objects ?? []).length;
  ui.status.textContent = `${count} object${count === 1 ? '' : 's'}`;
}

// Values in the state panel read like Python: [1, 2], {'a': 1}, True, None.
function pythonRepr(value) {
  if (value === null) return 'None';
  if (value === true || value === false) return value ? 'True' : 'False';
  if (typeof value === 'string') return `'${value}'`;
  if (Array.isArray(value)) return `[${value.map(pythonRepr).join(', ')}]`;
  if (typeof value === 'object') return `{${Object.entries(value).map(([key, item]) => `'${key}': ${pythonRepr(item)}`).join(', ')}}`;
  return String(value);
}

// A program that keeps its values in a dictionary named `state` shows them here.
function renderState(state) {
  ui.statePanel.hidden = !state || typeof state !== 'object';
  if (ui.statePanel.hidden) return;
  const sizes = state.__sizes__ ?? {};
  ui.stateValues.replaceChildren(...Object.entries(state).filter(([key]) => key !== '__sizes__').flatMap(([key, value]) => {
    const term = document.createElement('dt');
    term.textContent = key in sizes ? `${key} (${sizes[key]})` : key;
    const detail = document.createElement('dd');
    detail.textContent = pythonRepr(value);
    return [term, detail];
  }));
}

function showResult(result, successMessage) {
  if (result?.scene) draw(result.scene);
  if (result && 'frames' in result) setFrames(result.frames);
  if (result && 'state' in result) renderState(result.state);
  if (result) extension?.onResult?.(result, active);
  if (result?.error) {
    const last = result.error.trim().split('\n').at(-1);
    setFeedback(last || 'Something went wrong. See the error below.', true);
    setConsole(result.error, true);
  } else {
    setFeedback(successMessage);
    setConsole(result?.output || '');
  }
}

// ---------------------------------------------------------------------------
// Run, check, stop

async function withBusy(task) {
  if (!ready || busy) return;
  busy = true;
  setButtons();
  try {
    await task();
  } catch (error) {
    if (String(error) !== 'Stopped') setFeedback(String(error), true);
  } finally {
    busy = false;
    setButtons();
  }
}

async function runCode() {
  stopPlay();
  await withBusy(async () => {
    setFeedback('Running…');
    const result = await request('run', { code: editor.getValue() });
    hasRun = !result?.error;
    setCanvasInteraction(hasRun && result?.acceptsClicks === true);
    showResult(result, 'Done. Edit and press Run again, or Check my work.');
    setGameControls(result);
  });
}

async function checkCode() {
  reasoningOpened.add(lab.exercises[active].exercise_id);
  renderQuestions();
  stopPlay();
  await withBusy(async () => {
    setFeedback('Checking…');
    const result = await request('tests', { code: editor.getValue(), tests: lab.exercises[active].tests });
    const checks = result.tests ?? [];
    const passed = checks.filter((item) => item.passed).length;
    const summary = checks.map((item) => `${item.passed ? '✓' : '✗'} ${item.name.replaceAll('_', ' ')}${item.error ? ` — ${item.error}` : ''}`).join('\n');
    const outcome = result.error ? null : recordChecks(checks);
    const heading = outcome?.allPassed
      ? `All ${checks.length} checks passed. Exercise complete.${outcome.moduleComplete ? ' Every exercise in this module is done.' : ''}`
      : outcome?.questionsLeft
        ? `All ${checks.length} checks passed. Answer the questions above to finish.`
        : `${passed} of ${checks.length} checks passed.${outcome?.nextStep ? ` Next: ${outcome.nextStep}.` : ''}`;
    showResult(result, `${heading}\n${summary}`);
    if (passed !== checks.length) ui.feedback.classList.add('bad');
    const extensionMessage = extension?.onChecks?.(checks, active);
    if (extensionMessage) setFeedback(extensionMessage, passed !== checks.length);
    if (outcome?.allPassed) celebrate();
  });
}

function restartPython(message, bad = true) {
  stopPlay();
  worker.terminate();
  for (const entry of pending.values()) entry.reject('Stopped');
  pending = new Map();
  busy = false;
  hasRun = false;
  setCanvasInteraction(false);
  ui.gameControls.hidden = true;
  setFeedback(message, bad);
  startWorker();
}

// ---------------------------------------------------------------------------
// Clicks, keys and the clock

const keyNames = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right', w: 'up', s: 'down', a: 'left', d: 'right', W: 'up', S: 'down', A: 'left', D: 'right', ' ': 'space' };

function setGameControls(result) {
  tickMs = hasRun && Number.isInteger(result?.tickMs) ? result.tickMs : null;
  acceptsKeys = hasRun && result?.acceptsKeys === true;
  gameOver = false;
  ui.gameControls.hidden = !(tickMs || acceptsKeys);
  ui.play.hidden = !tickMs;
  ui.play.textContent = '▶ Play';
  ui.tickRate.textContent = tickMs ? `tick every ${tickMs} ms` : '';
  ui.arrowPad.hidden = !acceptsKeys;
  if (acceptsKeys) {
    ui.canvasHint.hidden = false;
    ui.canvasHint.textContent = 'Focus the picture, then use the arrow keys or WASD.';
  }
}

function stopPlay() {
  playing = false;
  clearTimeout(tickTimer);
  if (!ui.play.hidden) ui.play.textContent = gameOver ? '▶ Play again' : '▶ Play';
}

function scheduleTick() {
  clearTimeout(tickTimer);
  if (playing && tickMs) tickTimer = setTimeout(doTick, tickMs);
}

// Keys and ticks run between Runs, outside the busy lock, so a watchdog stands in for the Stop button.
async function eventRequest(type, payload = {}) {
  const watchdog = setTimeout(() => restartPython(`Your ${type} handler ran for more than 2 seconds, so Python was restarted. Look for a loop that never ends.`), 2000);
  try {
    return await request(type, payload);
  } catch {
    return null;
  } finally {
    clearTimeout(watchdog);
  }
}

// A program ends by setting state["over"] = True; the clock then stops and shows state["last_action"].
function applyEventResult(result) {
  if (!result) return;
  if (result.scene) draw(result.scene);
  if ('frames' in result) setFrames(result.frames);
  renderState(result.state);
  extension?.onResult?.(result, active);
  if (result.error) {
    stopPlay();
    showResult(result, '');
  } else if (result.state?.over === true) {
    gameOver = true;
    stopPlay();
    const note = typeof result.state.last_action === 'string' && result.state.last_action ? result.state.last_action : 'Finished.';
    setFeedback(note);
  }
}

async function doTick() {
  if (!playing) return;
  if (busy || !ready || !hasRun) {
    scheduleTick();
    return;
  }
  const result = await eventRequest('tick');
  if (!playing) return;
  applyEventResult(result);
  scheduleTick();
}

async function sendKey(key) {
  if (!ready || busy || !hasRun || !acceptsKeys) return;
  applyEventResult(await eventRequest('key', { key }));
}

async function togglePlay() {
  if (playing) {
    stopPlay();
    return;
  }
  if (gameOver) {
    await runCode();
    if (!tickMs) return;
  }
  playing = true;
  ui.play.textContent = '❚❚ Pause';
  ui.canvas.focus();
  scheduleTick();
}

function clickAt(x, y) {
  if (!ready || busy || !hasRun || !acceptsClicks) return;
  void withBusy(async () => {
    const result = await request('click', { x, y });
    showResult(result, `Clicked at (${x}, ${y}).`);
  });
}

// ---------------------------------------------------------------------------
// Frames: frame() records the picture; the slider steps through the recording, then the final picture.

function setFrames(list) {
  frames = Array.isArray(list) ? list : [];
  ui.frameControls.hidden = frames.length === 0;
  if (!frames.length) return;
  ui.frameSlider.max = String(frames.length + 1);
  showFrame(frames.length + 1, false);
}

function showFrame(position, redraw = true) {
  frameIndex = Math.max(1, Math.min(frames.length + 1, position));
  ui.frameSlider.value = String(frameIndex);
  const final = frameIndex === frames.length + 1;
  ui.frameLabel.textContent = final ? `final · ${frames.length} frame${frames.length === 1 ? '' : 's'}` : `frame ${frameIndex} / ${frames.length}`;
  if (redraw) render(final ? scene : { ...scene, objects: frames[frameIndex - 1] });
  extension?.onFrame?.(final ? null : frameIndex - 1, frames.length, active);
}

// ---------------------------------------------------------------------------
// Lesson text: prompts, hints, questions, task list, recap

function appendInline(target, text) {
  for (const segment of String(text).split(/(`[^`]+`|\*\*[^*]+\*\*|\*[^*\s][^*]*\*)/g)) {
    if (segment.startsWith('`') && segment.endsWith('`') && segment.length > 1) {
      const element = document.createElement('code');
      element.textContent = segment.slice(1, -1);
      target.append(element);
    } else if (segment.startsWith('**') && segment.endsWith('**') && segment.length > 3) {
      const element = document.createElement('strong');
      element.textContent = segment.slice(2, -2);
      target.append(element);
    } else if (/^\*[^*\s][^*]*\*$/.test(segment)) {
      const element = document.createElement('em');
      element.textContent = segment.slice(1, -1);
      target.append(element);
    } else {
      target.append(document.createTextNode(segment));
    }
  }
}

function resetHints() {
  hintCount = 0;
  ui.hints.replaceChildren();
  ui.hints.hidden = true;
  ui.hintButton.textContent = 'Hint';
  ui.hintButton.disabled = !lab.exercises[active].hints?.length;
}

function showNextHint() {
  const hints = lab.exercises[active].hints ?? [];
  if (hintCount >= hints.length) return;
  const paragraph = document.createElement('p');
  const label = document.createElement('strong');
  label.textContent = `Hint ${hintCount + 1}. `;
  paragraph.append(label);
  appendInline(paragraph, hints[hintCount]);
  ui.hints.append(paragraph);
  ui.hints.hidden = false;
  hintCount += 1;
  ui.hintButton.textContent = hintCount < hints.length ? `Next hint (${hintCount + 1}/${hints.length})` : 'No more hints';
  ui.hintButton.disabled = hintCount >= hints.length;
}

// Progress is kept in this browser only: which exercises passed, which checklist steps the latest
// check ticked, and the exercise to reopen. It is a convenience for the learner, not a record.
function storageGet(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function storageSet(key, value) {
  try {
    if (value === null) localStorage.removeItem(key);
    else localStorage.setItem(key, value);
  } catch {
    // Storage can be full or blocked; the value then lasts only for this visit.
  }
}

function readProgress(labId) {
  try {
    const saved = JSON.parse(storageGet(`preview:${labId}:progress`) ?? '{}');
    return {
      completed: Array.isArray(saved.completed) ? saved.completed.filter((id) => typeof id === 'string') : [],
      steps: saved.steps && typeof saved.steps === 'object' ? saved.steps : {},
      last: typeof saved.last === 'string' ? saved.last : null,
      moduleComplete: saved.moduleComplete === true,
      checked: saved.checked && typeof saved.checked === 'object' ? saved.checked : {},
      answers: saved.answers && typeof saved.answers === 'object' ? saved.answers : {},
    };
  } catch {
    return { completed: [], steps: {}, last: null, moduleComplete: false, checked: {}, answers: {} };
  }
}

function writeProgress() {
  storageSet(`preview:${lab.lab_spec_id}:progress`, JSON.stringify(progress));
}

function progressSummary() {
  return {
    module: selectedModule.id,
    exercise: lab.exercises[active].exercise_id,
    completed: lab.exercises.map((exercise) => exercise.exercise_id).filter((id) => progress.completed.includes(id)),
    total: lab.exercises.length,
  };
}

// Tick the checklist steps whose checks all passed, and mark the exercise and module complete.
function recordChecks(checks) {
  const exercise = lab.exercises[active];
  const id = exercise.exercise_id;
  const passedNames = new Set(checks.filter((item) => item.passed).map((item) => item.name));
  const steps = exercise.checklist ?? [];
  const ticks = steps.map((step) => step.checks.every((name) => passedNames.has(name)));
  progress.steps[id] = ticks;
  const checksPassed = checks.length > 0 && checks.every((item) => item.passed);
  progress.checked[id] = checksPassed;
  const { complete, moduleFirst } = completeIfReady();
  return {
    allPassed: complete,
    questionsLeft: checksPassed && !complete,
    moduleComplete: moduleFirst,
    nextStep: steps.find((_, index) => !ticks[index])?.step,
  };
}

// An exercise is complete when its checks pass and, if it asks questions, each is answered correctly.
function completeIfReady() {
  const exercise = lab.exercises[active];
  const id = exercise.exercise_id;
  const complete = progress.checked[id] === true && questionsAnswered(exercise);
  const firstPass = complete && !progress.completed.includes(id);
  if (firstPass) progress.completed.push(id);
  const moduleComplete = lab.exercises.every((item) => progress.completed.includes(item.exercise_id));
  const moduleFirst = moduleComplete && !progress.moduleComplete;
  progress.moduleComplete = moduleComplete;
  writeProgress();
  renderTask();
  renderExerciseNav();
  if (firstPass) post({ type: 'exercise-complete', ...progressSummary() });
  if (moduleFirst) {
    renderRecap(true);
    post({ type: 'module-complete', ...progressSummary() });
  }
  return { complete, moduleFirst };
}

function questionsAnswered(exercise) {
  const answers = progress.answers[exercise.exercise_id] ?? [];
  return (exercise.questions ?? []).every((_, index) => answers[index] === true);
}

// Questions ask the learner to name the plan. Each choice explains itself, right or wrong; only the
// right one is recorded. One question at a time: later questions assume the plan.
const reasoningOpened = new Set();
function renderQuestions() {
  const exercise = lab.exercises[active];
  const questions = exercise.questions ?? [];
  const mastery = exercise.title.startsWith("Mastery challenge:");
  const gated = mastery && !reasoningOpened.has(exercise.exercise_id) && !progress.checked[exercise.exercise_id];
  ui.questions.hidden = questions.length === 0 || gated;
  $("show-reasoning").hidden = !gated;
  $("questions-title").textContent = mastery ? "Explain your solution" : "Predict before running";
  const answers = progress.answers[exercise.exercise_id] ?? [];
  const shown = questions.findIndex((_, index) => answers[index] !== true);
  ui.questionList.replaceChildren(...questions.slice(0, shown < 0 ? questions.length : shown + 1).map((question, index) => {
    const block = document.createElement('fieldset');
    block.className = 'question';
    block.dataset.question = String(index);
    const legend = document.createElement('legend');
    appendInline(legend, `${index + 1}. ${question.prompt}`);
    const choices = document.createElement('div');
    choices.className = 'question-choices';
    question.choices.forEach((choice, choiceIndex) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.dataset.choice = String(choiceIndex);
      appendInline(button, choice.text);
      if (answers[index] === true && choiceIndex === question.answer) button.classList.add('right');
      choices.append(button);
    });
    const result = document.createElement('p');
    result.className = 'question-result';
    result.setAttribute('role', 'status');
    if (answers[index] === true) appendInline(result, `✓ ${question.choices[question.answer].why}`);
    block.append(legend, choices, result);
    return block;
  }));
}

function answerQuestion(index, choiceIndex) {
  const exercise = lab.exercises[active];
  const question = exercise.questions[index];
  const block = ui.questionList.querySelector(`[data-question="${index}"]`);
  const right = choiceIndex === question.answer;
  for (const button of block.querySelectorAll('[data-choice]')) {
    button.classList.toggle('right', right && Number(button.dataset.choice) === choiceIndex);
    button.classList.toggle('wrong', !right && Number(button.dataset.choice) === choiceIndex);
  }
  const result = block.querySelector('.question-result');
  result.replaceChildren();
  appendInline(result, `${right ? '✓' : 'Not quite.'} ${question.choices[choiceIndex].why}`);
  if (!right) return;
  const answers = progress.answers[exercise.exercise_id] ?? [];
  answers[index] = true;
  progress.answers[exercise.exercise_id] = answers;
  const wasComplete = progress.completed.includes(exercise.exercise_id);
  renderQuestions();
  const { complete, moduleFirst } = completeIfReady();
  if (complete && !wasComplete) {
    setFeedback(`Exercise complete: the checks pass and the plan is right.${moduleFirst ? ' Every exercise in this module is done.' : ''}`);
    celebrate();
  }
}

function completedMark() {
  const mark = document.createElement('span');
  mark.className = 'done-mark';
  mark.textContent = ' ✓';
  mark.setAttribute('aria-label', 'completed');
  return mark;
}

function renderExerciseNav() {
  for (const [index, button] of [...ui.nav.querySelectorAll('button')].entries()) {
    const done = progress.completed.includes(lab.exercises[index].exercise_id);
    button.classList.toggle('active', index === active);
    if (index === active) button.setAttribute('aria-current', 'step');
    else button.removeAttribute('aria-current');
    button.classList.toggle('done', done);
    button.querySelector('.done-mark')?.remove();
    if (done) button.append(completedMark());
  }
}

function renderTask() {
  const exercise = lab.exercises[active];
  const answers = progress.answers[exercise.exercise_id] ?? [];
  const checkTicks = progress.steps[exercise.exercise_id] ?? [];
  const steps = [
    ...(exercise.questions ?? []).map((question, index) => ({ text: question.step, done: answers[index] === true })),
    ...(exercise.checklist ?? []).map((step, index) => ({ text: step.step, done: checkTicks[index] === true })),
  ];
  ui.task.hidden = steps.length === 0;
  ui.taskSteps.replaceChildren(...steps.map((step) => {
    const item = document.createElement('li');
    item.classList.toggle('done', step.done);
    appendInline(item, step.text);
    return item;
  }));
  const done = steps.filter((step) => step.done).length;
  ui.taskProgress.textContent = done === steps.length ? 'All done ✓'
    : done > 0 || Array.isArray(progress.steps[exercise.exercise_id]) ? `${done} of ${steps.length} done` : 'Check my work ticks these off';
}

// Once every exercise passes, the recap names what the module taught and where it is used.
function renderRecap(open) {
  const recap = lab.recap;
  ui.recap.hidden = !(recap && progress.moduleComplete);
  if (ui.recap.hidden) return;
  const fill = (list, items) => list.replaceChildren(...(items ?? []).map((text) => {
    const item = document.createElement('li');
    appendInline(item, text);
    return item;
  }));
  fill(ui.recapLearned, recap.learned);
  fill(ui.recapReal, recap.in_real_programs);
  ui.recapFacts.replaceChildren(...[['INVARIANT', recap.invariant], ['COMPLEXITY', recap.complexity], ['COMMON MISTAKE', recap.common_mistake]]
    .filter(([, text]) => text)
    .flatMap(([label, text]) => {
      const heading = document.createElement('strong');
      heading.textContent = label;
      const paragraph = document.createElement('p');
      appendInline(paragraph, text);
      return [heading, paragraph];
    }));
  // A question from an earlier module, answered only when the learner asks.
  ui.recapRetrieval.hidden = !recap.retrieval;
  if (recap.retrieval) {
    const summary = ui.recapRetrieval.querySelector('summary');
    summary.replaceChildren();
    appendInline(summary, `Retrieval: ${recap.retrieval.question}`);
    const answer = ui.recapRetrieval.querySelector('p');
    answer.replaceChildren();
    appendInline(answer, recap.retrieval.answer);
    ui.recapRetrieval.open = false;
  }
  const next = moduleChoices[moduleChoices.indexOf(selectedModule) + 1];
  ui.recapNext.hidden = !next;
  if (next) {
    ui.recapNext.href = `?module=${next.id}`;
    ui.recapNext.textContent = `Next: ${next.label} →`;
  }
  ui.recap.open = open;
}

// ---------------------------------------------------------------------------
// Drafts: the editor saves per exercise; replacing it keeps the learner's code for one undo.

function draftKey(exercise) {
  return `preview:${lab.lab_spec_id}:${exercise.exercise_id}`;
}

function backupKey(exercise) {
  return `${draftKey(exercise)}:replaced`;
}

function backupCode() {
  const exercise = lab.exercises[active];
  const code = editor.getValue();
  if (code.trim() && code !== exercise.starter_code && code !== exercise.solution) storageSet(backupKey(exercise), code);
}

function renderUndo(message) {
  ui.undo.hidden = storageGet(backupKey(lab.exercises[active])) === null;
  if (message) ui.undoMessage.textContent = `${message} `;
}

function saveDraft() {
  const exercise = lab?.exercises[active];
  if (exercise) storageSet(draftKey(exercise), editor.getValue());
  extension?.onEdit?.(active);
}

function selectExercise(index) {
  active = index;
  const exercise = lab.exercises[index];
  progress.last = exercise.exercise_id;
  writeProgress();
  renderTask();
  renderQuestions();
  hasRun = false;
  setCanvasInteraction(false);
  ui.title.textContent = exercise.title;
  ui.prompt.replaceChildren();
  appendInline(ui.prompt, exercise.prompt_md);
  resetHints();
  editor.setValue(storageGet(draftKey(exercise)) ?? exercise.starter_code);
  stopPlay();
  tickMs = null;
  acceptsKeys = false;
  gameOver = false;
  ui.gameControls.hidden = true;
  setFrames([]);
  renderState(null);
  extension?.select?.(index);
  renderExerciseNav();
  renderRecap(false);
  renderUndo('Your earlier code for this exercise is saved.');
  setFeedback('Press Run to see what your Python draws.');
  setConsole('');
  draw({ width: 600, height: 400, objects: [] });
  ui.status.textContent = 'Not run yet';
  if (ready) void runCode();
}

// ---------------------------------------------------------------------------
// Controls

ui.run.addEventListener('click', runCode);
ui.tests.addEventListener('click', checkCode);
$('show-reasoning').addEventListener('click', () => { reasoningOpened.add(lab.exercises[active].exercise_id); renderQuestions(); });
ui.hintButton.addEventListener('click', showNextHint);
ui.sample.addEventListener('click', async () => {
  const exercise = lab.exercises[active];
  if (!await ensureSolution(exercise) || exercise !== lab.exercises[active]) return;
  backupCode();
  editor.setValue(exercise.solution);
  saveDraft();
  renderUndo('Your code was replaced with the example.');
  if (ready && !busy) void runCode();
});
ui.reset.addEventListener('click', () => {
  const exercise = lab.exercises[active];
  backupCode();
  storageSet(draftKey(exercise), null);
  editor.setValue(exercise.starter_code);
  renderUndo('You started over.');
  resetHints();
  if (ready && !busy) void runCode();
});
ui.questionList.addEventListener('click', (event) => {
  const button = event.target.closest('[data-choice]');
  if (button) answerQuestion(Number(button.closest('[data-question]').dataset.question), Number(button.dataset.choice));
});
ui.undoRestore.addEventListener('click', () => {
  const exercise = lab.exercises[active];
  const saved = storageGet(backupKey(exercise));
  if (saved === null) return;
  storageSet(backupKey(exercise), null);
  editor.setValue(saved);
  saveDraft();
  renderUndo();
  setFeedback('Your code is back.');
  if (ready && !busy) void runCode();
});
ui.undoDismiss.addEventListener('click', () => {
  storageSet(backupKey(lab.exercises[active]), null);
  renderUndo();
});
ui.stop.addEventListener('click', () => restartPython('Stopped. Restarting Python.', false));
ui.play.addEventListener('click', togglePlay);
ui.arrowPad.addEventListener('click', (event) => {
  const button = event.target.closest('[data-key]');
  if (button) void sendKey(button.dataset.key);
});
ui.canvas.addEventListener('keydown', (event) => {
  const key = keyNames[event.key];
  if (!key || !acceptsKeys) return;
  event.preventDefault();
  void sendKey(key);
});
document.addEventListener('visibilitychange', () => {
  if (document.hidden) stopPlay();
});
ui.framePrev.addEventListener('click', () => showFrame(frameIndex - 1));
ui.frameNext.addEventListener('click', () => showFrame(frameIndex + 1));
ui.frameSlider.addEventListener('input', () => showFrame(Number(ui.frameSlider.value)));
ui.canvas.addEventListener('click', (event) => {
  const rect = ui.canvas.getBoundingClientRect();
  clickAt(Math.round((event.clientX - rect.left) * scene.width / rect.width),
    Math.round((event.clientY - rect.top) * scene.height / rect.height));
});

// ---------------------------------------------------------------------------
// Start-up

function showModuleIntro(choice) {
  ui.moduleEyebrow.textContent = choice.eyebrow || 'ALGORITHM DESIGN AND ANALYSIS';
  ui.moduleHeading.textContent = choice.heading;
  ui.moduleSubtitle.textContent = choice.subtitle;
  document.title = `${choice.label.replace(/^\d+ · /, '')} · SICP Lab`;
}

async function loadModuleIndex() {
  try {
    const response = await fetch('../modules/index.json');
    if (!response.ok) return [];
    const list = await response.json();
    return Array.isArray(list) ? list.filter((item) => typeof item?.id === 'string' && typeof item?.label === 'string') : [];
  } catch {
    return [];
  }
}

// A module may bring its own panels in modules/<id>/preview.js (index.json marks it with
// "panels": true); a host lab carries them as source in lab.preview.panels.
async function loadExtension() {
  const panels = labFromHost ? lab.preview?.panels : null;
  if (typeof panels !== 'string' && !selectedModule.panels) return null;
  try {
    const module = typeof panels === 'string'
      ? await import(URL.createObjectURL(new Blob([panels], { type: 'text/javascript' })))
      : await import(`../modules/${selectedModule.id}/preview.js`);
    return module.install({ ui, request, setFeedback, sendKey, get lab() { return lab; } }) ?? null;
  } catch (error) {
    setFeedback(`This module's panels could not load: ${error}`, true);
    return null;
  }
}

async function init() {
  draw(scene);
  if (!selectedModule) {
    setFeedback('No lab is published here yet.', true);
    ui.moduleHeading.textContent = 'No lab yet';
    return;
  }
  startWorker();
  try {
    showModuleIntro(selectedModule);
    if (!embedded) {
      for (const choice of moduleChoices) {
        const link = document.createElement('a');
        link.href = `?module=${choice.id}`;
        link.textContent = choice.label;
        link.classList.toggle('active', choice.id === selectedModule.id);
        if (readProgress(`${COURSE_ID}-${choice.id}`).moduleComplete) {
          link.classList.add('done');
          link.append(completedMark());
        }
        if (choice.id === selectedModule.id) link.setAttribute('aria-current', 'page');
        ui.modules.append(link);
      }
    }
    if (labFromHost) {
      lab = await labFromHostPage();
      // The host lab names its own module; take what this preview does not already know.
      for (const field of ['label', 'eyebrow', 'heading', 'subtitle']) {
        if (typeof lab.preview?.[field] === 'string' && !knownModule) selectedModule[field] = lab.preview[field];
      }
      showModuleIntro(selectedModule);
    } else {
      const response = await fetch(`../modules/${selectedModule.id}/lab.json`);
      if (!response.ok) throw new Error(`The lab could not load (${response.status})`);
      lab = await response.json();
    }
    progress = readProgress(lab.lab_spec_id);
    extension = await loadExtension();
    lab.exercises.forEach((exercise, index) => {
      const button = document.createElement('button');
      button.textContent = `${index + 1}. ${exercise.title}`;
      button.addEventListener('click', () => selectExercise(index));
      ui.nav.append(button);
    });
    // ?exercise= takes an exercise id or a 1-based number; otherwise resume the last one opened here.
    const requestedExercise = searchParams.get('exercise') ?? '';
    let start = lab.exercises.findIndex((exercise) => exercise.exercise_id === requestedExercise);
    if (start < 0 && /^[1-9]\d*$/.test(requestedExercise) && Number(requestedExercise) <= lab.exercises.length) start = Number(requestedExercise) - 1;
    const resumed = start < 0 ? lab.exercises.findIndex((exercise) => exercise.exercise_id === progress.last) : -1;
    if (start < 0) start = Math.max(0, resumed);
    if (resumed > 0) {
      const note = document.createElement('span');
      note.className = 'resume-note';
      note.textContent = `Resuming exercise ${resumed + 1}`;
      ui.nav.append(note);
    }
    selectExercise(start);
    post({ type: 'ready', ...progressSummary() });
  } catch (error) {
    setFeedback(error instanceof Error ? error.message : String(error), true);
  }
}

void init();
