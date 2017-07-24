var postRequest = function(invocationStyle, cmd, exitCodeEl, stdOutEl, stdErrEl) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            var resp = JSON.parse(this.responseText);
            if (this.status == 200) {
                exitCodeEl.innerHTML = '<h3>Exit Code: ' + resp.exit_code + '</h3>';
                stdOutEl.innerHTML = '<pre>' + resp.stdout + '</pre>';
                stdErrEl.innerHTML = '<pre>' + resp.stderr + '</pre>';
            } else {
                var msg = (resp && resp.error) ? resp.error : "You done broke somethin'.";
                alert(msg);
            }
        }
    };
    xhttp.open('POST', 'https://nw4fjuynjg.execute-api.us-west-2.amazonaws.com/beta/invocation?style=' + invocationStyle, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.setRequestHeader('Accept', 'application/json');
    var req = {cmd: cmd};
    xhttp.send(JSON.stringify(req));
};
var initCodeBlocks = function() {
  var codeMirrors = {};
  ['shell', 'perl', 'python'].forEach(function(lang) {
    var textAreas = document.getElementsByClassName(lang + '-block');
    Array.prototype.forEach.call(textAreas, function(el) {
        var mirror = CodeMirror.fromTextArea(el, {
            lineNumbers: true,
            styleActiveLine: true,
            matchBrackets: true,
            theme: 'ambiance',
            mode: lang
        });
        codeMirrors[el.id] = mirror;
    });
  });
  var runButtons = document.getElementsByClassName('run-btn');
  Array.prototype.forEach.call(runButtons, function(el) {
      el.onclick = function() {
          var regex = /([0-9]+)$/;
          var blockNum = regex.exec(el.id)[1];
          var resultsElExitCode = document.getElementById('repl-results-exit-code-' + blockNum);
          var resultsElStdOut = document.getElementById('repl-results-stdout-' + blockNum);
          var resultsElStdErr = document.getElementById('repl-results-stderr-' + blockNum);
          var inputEl = document.getElementById('repl-input-' + blockNum);
          var cmd = codeMirrors[inputEl.id].getValue().trim();
          var invocationType = inputEl.classList.contains('shell-block') ? 'inline' : 'script';
          postRequest(invocationType, cmd, resultsElExitCode, resultsElStdOut, resultsElStdErr);
      }
  });
};
