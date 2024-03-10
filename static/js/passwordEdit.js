document.addEventListener('DOMContentLoaded', function () {
    var changePwdForm = document.getElementById('change-pwd');

    changePwdForm.addEventListener('submit', function (event) {
        // 在这里可以添加密码匹配的逻辑，例如：
        var password = changePwdForm.querySelector('[name="password"]').value;
        var password1 = changePwdForm.querySelector('[name="password1"]').value;

        if (password !== password1) {
            var errorMsg = document.getElementById('pwd_msg');
            errorMsg.textContent = 'Two passwords are different';
            errorMsg.style.display = 'block';

            event.preventDefault(); // 阻止表单的默认提交行为
            return false; // 阻止任何可能的事件传播
        }
    });
});
