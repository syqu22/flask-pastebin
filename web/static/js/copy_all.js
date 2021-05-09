document.getElementById("copy-all").addEventListener("click", copy_all);

// Copy pastebin's content to clipboard
function copy_all() {
  var r = document.createRange();
  r.selectNode(document.getElementById("pastebin"));
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(r);
  document.execCommand('copy');
  window.getSelection().removeAllRanges();
}
