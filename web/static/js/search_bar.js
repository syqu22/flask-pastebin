const searchButton = document.getElementById("search_button");
const searchInput = document.getElementById("search_input");

searchButton.addEventListener("click", () => {
  const inputValue = searchInput.value;
  window.location.href = "search/" + inputValue
});
