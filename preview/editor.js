import { EditorState } from '@codemirror/state';
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter } from '@codemirror/view';
import { python } from '@codemirror/lang-python';
import { defaultKeymap, indentWithTab } from '@codemirror/commands';
import { bracketMatching, indentOnInput } from '@codemirror/language';
import { oneDark } from '@codemirror/theme-one-dark';

const previewTheme = EditorView.theme({
  '&': {
    height: '325px',
    borderRadius: '11px',
    border: '1px solid #183b32',
    backgroundColor: '#142920',
    color: '#edfbef',
  },
  '&.cm-focused': {
    outline: 'none',
    boxShadow: '0 0 0 3px #aed8c1',
  },
  '.cm-scroller': {
    fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
    fontSize: '14px',
    lineHeight: '1.65',
  },
  '.cm-content': {
    padding: '17px 0',
    caretColor: '#edfbef',
  },
  '.cm-line': { padding: '0 8px' },
  '.cm-gutters': {
    backgroundColor: '#142920',
    borderRight: '1px solid #315346',
    color: '#789b89',
  },
  '.cm-lineNumbers .cm-gutterElement': { padding: '0 10px 0 12px' },
  '.cm-activeLine': { backgroundColor: 'rgba(136, 194, 157, .08)' },
  '.cm-activeLineGutter': { backgroundColor: 'rgba(136, 194, 157, .12)' },
  '.cm-selectionBackground': { backgroundColor: 'rgba(112, 166, 136, .35) !important' },
}, { dark: true });

export function createPythonEditor(parent, onChange, onRun) {
  let silent = false;
  const state = EditorState.create({
    doc: '',
    extensions: [
      lineNumbers(),
      highlightActiveLine(),
      highlightActiveLineGutter(),
      bracketMatching(),
      indentOnInput(),
      python(),
      oneDark,
      previewTheme,
      EditorView.lineWrapping,
      EditorView.contentAttributes.of({ 'aria-label': 'Python code', spellcheck: 'false' }),
      keymap.of([
        { key: 'Mod-Enter', run: () => { onRun(); return true; } },
        ...defaultKeymap,
        indentWithTab,
      ]),
      EditorView.updateListener.of((update) => {
        if (update.docChanged && !silent) onChange(update.state.doc.toString());
      }),
    ],
  });
  const view = new EditorView({ state, parent });
  return {
    getValue: () => view.state.doc.toString(),
    setValue(value) {
      silent = true;
      view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: value } });
      silent = false;
    },
    focus: () => view.focus(),
  };
}
