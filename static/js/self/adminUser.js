function change(obj) {
    let formData = new FormData();

    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('func_code', '1')
    formData.append('user_item', $(obj).attr('id'));
    formData.append('user_id', $(obj).attr('name'));
    if ($(obj).prop('checked')) {
        formData.append('user_attr', '1');
    } else {
        formData.append('user_attr', '0');
    }
    $.ajax({
        type: 'POST',
        url: '/admin/user',
        data: formData,
        processData: false,
        contentType: false,
        success: function () {
            $('.correct_alert_text').text('已修改');
            $('.correct_alert').fadeIn(200);
            setTimeout(function () {
                $('.correct_alert').fadeOut(200);
            }, 1600);
        }
    });
}

function deleteUser(obj) {
    Swal.fire({
        title: '确认要永久删除吗',
        confirmButtonText: '确　定',
        showCancelButton: true,
        cancelButtonText: '取消',
        text: '删除后将不能恢复，请谨慎操作',
        icon: 'warning',
        width: '400px',
        customClass: {
            confirmButton: 'swal-btn-confirm',
            title: 'swal-title',
            cancelButton: 'swal-btn-cancel',
        }
    }).then(function (result) {
        if (result.isConfirmed) {
            let userId = $(obj).attr('id');
            let formData = new FormData();

            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
            formData.append('func_code', '2');
            formData.append('user_id', userId);
            $.ajax({
                type: 'POST',
                url: '/admin/user',
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    if (response['status'] === '1') {
                        $('.correct_alert_text').text('已删除');
                        $('.correct_alert').fadeIn(200);
                        setTimeout(function () {
                            location.reload();
                        }, 400);
                    } else {
                        message = response['message'];
                        Swal.fire({
                            title: '未知错误，请联系开发者解决',
                            icon: 'error',
                            width: '400px',
                            html: '<label><span>错误信息：</span>'+ message +'</label><br><label><span>联系方式：</span>2562521178@qq.com</label><style>label{color:#545454;line-height: 2rem}span{font-weight: 700;}</style>',
                            confirmButtonText: '确　定',
                            customClass: {
                                confirmButton: 'swal-btn-confirm',
                                title: 'swal-title',
                            }
                        });
                    }
                }
            })
        }
    });
}