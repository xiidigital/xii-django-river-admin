// CodeMirror 6 completion source for a minimal Python-ish autocomplete,
// mirroring the CodeMirror 5 "python" hint helper this project used to
// ship (keywords + builtins + the function names recognized by the
// backend for a given callback function body).
import { autocompletion } from "@codemirror/autocomplete";

const PYTHON_KEYWORDS =
  "and del from not while as elif global or with assert else if pass yield " +
  "break except import print class exec in raise continue finally is return def for lambda try";

const PYTHON_BUILTINS =
  "abs divmod input open staticmethod all enumerate int ord str " +
  "any eval isinstance pow sum basestring execfile issubclass print super " +
  "bin file iter property tuple bool filter len range type " +
  "bytearray float list raw_input unichr callable format locals reduce unicode " +
  "chr frozenset long reload vars classmethod getattr map repr xrange " +
  "cmp globals max reversed zip compile hasattr memoryview round __import__ " +
  "complex hash min set apply delattr help next setattr buffer " +
  "dict hex object slice coerce dir id oct sorted intern";

export default function initializePythonHints(recognized_functions) {
  var extraWords = (recognized_functions || []).join(" ");
  var keywords = PYTHON_KEYWORDS.split(" ").filter(Boolean);
  var builtins = (PYTHON_BUILTINS + " " + extraWords).split(" ").filter(Boolean);

  var options = keywords
    .map(word => ({ label: word, type: "keyword" }))
    .concat(builtins.map(word => ({ label: word, type: "function", apply: word + "(" })));

  function pythonCompletionSource(context) {
    var word = context.matchBefore(/[\w$_]*/);
    if (!word || (word.from == word.to && !context.explicit)) {
      return null;
    }
    return {
      from: word.from,
      options
    };
  }

  return autocompletion({ override: [pythonCompletionSource] });
}
