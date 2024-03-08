//TODO 重写修改密码
$('#set_pwd').click(function (e) {
    var pwd = $('#change-pwd [name="password"]').val()
    var pwd1 = $('#change-pwd [name="password1"]').val()
    if (pwd != pwd1) {
        $("#pwd_msg").text('two passwords are different').show()
        return false
    }

    var token = $('#change-pwd [name="csrfmiddlewaretoken"]').val()

    // var form = new FormData(document.getElementById("gender_radio"))
    var form = new FormData();
    form.append("password", pwd);
    form.append("csrfmiddlewaretoken", token);

    $.ajax({
        type: 'POST',
        url: '/user/settings/',
        // data:'json',
        processData: false,
        contentType: false,
        data: form,
        success: function (response) {
            console.log('ok', response)
            window.location.href = '/user/login/';
        },
        error: function (response) {
            console.log('err', response)
            if (response.status == 200) {
                window.location.href = '/user/login/';
            } else {
                $("#pwdmsg").text(response.responseText).show()
            }
        }
    })
})

$('#pwd_msg').click(function (e) {
    $('#pwd_msg').hide()
})