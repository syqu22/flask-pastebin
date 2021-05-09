var private_checkbox = document.getElementById("private");
var expire_checkbox = document.getElementById("expire");

var password_input = document.getElementById("password");
var expire_select = document.getElementById("expire_select");

// Change disabled property depending on if checkbox is clicked
private_checkbox.addEventListener('change', function() {
  if (this.checked) {
    password_input.removeAttribute("disabled")
  } else {
    password_input.setAttribute("disabled","")
  }
});

expire_checkbox.addEventListener('change', function() {
  if (this.checked) {
    expire_select.removeAttribute("disabled")
  } else {
    expire_select.setAttribute("disabled","")
  }
});
