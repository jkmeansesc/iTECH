 document.addEventListener('DOMContentLoaded', function() {
        var fileInput = document.getElementById('img_box');
        var uploadButton = document.getElementById('upload-btn');
        var fileNameSpan = document.getElementById('file-name');

        uploadButton.addEventListener('click', function() {
            fileInput.click();
        });

        fileInput.addEventListener('change', function() {
            var selectedFile = fileInput.files[0];

            if (selectedFile) {
                fileNameSpan.textContent = selectedFile.name;
            } else {
                fileNameSpan.textContent = 'No file chosen';
            }
        });
    });