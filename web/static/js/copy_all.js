document.getElementById("copy-all").addEventListener("click", copy_all);

function copy_all() {
  document.querySelector("#pastebin").select();
  document.execCommand("copy");
}
