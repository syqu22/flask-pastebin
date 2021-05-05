var private_checkbox = document.getElementById("private");
var password_input = document.getElementById("password");

private_checkbox.addEventListener('change', function() {
  if (this.checked) {
    password_input.removeAttribute("disabled")
  } else {
    password_input.setAttribute("disabled","")
  }
});
