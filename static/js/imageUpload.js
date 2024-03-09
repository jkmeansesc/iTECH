document.getElementById('img_box').addEventListener('change', function(event) {
        // 获取用户选择的文件
        var file = event.target.files[0];

        // 如果用户选择了文件
        if (file) {
            // 获取文件名并显示在页面上
            document.getElementById('file_name').innerText = file.name;
        }
    });