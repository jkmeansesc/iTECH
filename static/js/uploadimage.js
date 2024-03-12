document.addEventListener("DOMContentLoaded", function () {
  var uploadBtn = document.getElementById("upload-btn");
  var fileName = document.getElementById("file-name");
  var realInput = document.getElementById("{{ form.image.id_for_label }}");
  var label = document.getElementById("image-label");

  uploadBtn.addEventListener("click", function () {
    realInput.click(); // Trigger file input click
  });

  realInput.addEventListener("change", function () {
    var name = realInput.value.split("\\").pop(); // Extract file name
    fileName.textContent = name ? name : "No file chosen"; // Update display
  });

  label.addEventListener("click", function (e) {
    e.preventDefault();
  });
});
