var private_checkbox = document.getElementById("private");
var password_input = document.getElementById("password");

// Change disabled property depending on if checkbox is clicked
private_checkbox.addEventListener('change', function() {
  if (this.checked) {
    password_input.removeAttribute("disabled")
  } else {
    password_input.setAttribute("disabled","")
  }
});
