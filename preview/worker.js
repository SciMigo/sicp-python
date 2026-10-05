// Runs learner Python in Pyodide. The Python side (the scimigo API, runs and checks) lives in
// scimigo_bridge.py, which tools/check_lab.py also imports, so both run the same code.
const PYODIDE_BASE = 'https://cdn.jsdelivr.net/pyodide/v0.27.4/full/';
const STRAIGHTEDGE_WHEEL = './vendor/straightedge-0.8.0-py3-none-any.whl';

let pyodide;

async function fetchBytes(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url} could not load (${response.status})`);
  return new Uint8Array(await response.arrayBuffer());
}

async function initialize() {
  // Start the lab's own files downloading while Pyodide loads.
  const files = Promise.all([fetchBytes('./scimigo_bridge.py?v=1'), fetchBytes(STRAIGHTEDGE_WHEEL)]);
  const { loadPyodide } = await import(`${PYODIDE_BASE}pyodide.mjs`);
  pyodide = await loadPyodide({ indexURL: PYODIDE_BASE });
  const [bridge, wheel] = await files;
  pyodide.FS.mkdirTree('/lab/site');
  pyodide.FS.writeFile('/lab/scimigo_bridge.py', bridge);
  pyodide.FS.writeFile('/lab/straightedge.whl', wheel);
  // A wheel is a zip; unpacking it onto sys.path installs the pure-Python package offline.
  pyodide.runPython(`
import sys, zipfile
zipfile.ZipFile('/lab/straightedge.whl').extractall('/lab/site')
sys.path[:0] = ['/lab', '/lab/site']
import scimigo_bridge as _bridge
`);
  postMessage({ type: 'ready' });
  // Import the diagram library now, so the first figure() does not pay for it.
  pyodide.runPython('import straightedge.diagrams.registry');
}

const startup = initialize().catch((error) => {
  postMessage({ type: 'fatal', error: String(error) });
});

const calls = {
  run: (data) => ['_bridge.__preview_run(_src, _fixtures)', { _src: data.code, _fixtures: JSON.stringify(data.fixtures ?? []) }],
  click: (data) => ['_bridge.__preview_click(_x, _y)', { _x: data.x, _y: data.y }],
  key: (data) => ['_bridge.__preview_key(_key)', { _key: data.key }],
  tick: () => ['_bridge.__preview_tick()', {}],
  // Each check runs in a fresh session; the bridge then restores the live picture.
  tests: (data) => ['_bridge.__preview_tests(_src, _tests, _fixtures)', {
    _src: data.code, _tests: JSON.stringify(data.tests), _fixtures: JSON.stringify(data.fixtures ?? []),
  }],
};

onmessage = async ({ data }) => {
  await startup;
  if (!pyodide) return;
  try {
    const [expression, values] = calls[data.type](data);
    for (const [name, value] of Object.entries(values)) pyodide.globals.set(name, value);
    const parsed = JSON.parse(pyodide.runPython(expression));
    postMessage({ type: 'result', id: data.id, result: data.type === 'tests' ? { tests: parsed } : parsed });
  } catch (error) {
    postMessage({ type: 'result', id: data.id, result: { error: String(error) } });
  }
};
