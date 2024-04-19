function addMessage() {
    if ($('.operate_panel_item_add').css('display') == 'none') {
        $('.operate_panel_item_add').css('display', 'block');
        $('.operate_panel_item_add').children('.block_change').css('display', 'block');
    }
}

function autoFillGrade(obj) {
    let graduate = $(obj).parent().siblings('.block_change_graduate').children('.inputs').val();
    if (graduate === '') {
        $(obj).parent().siblings('.block_change_graduate').children('.inputs').focus();
    } else {
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
        formData.append('func_code', '1');
        formData.append('graduate', graduate);

        $.ajax({
            type: 'post',
            url: '/admin/message',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $(obj).siblings('.inputs').val(response['student_grade'])
                $(obj).siblings('.inputs').focus();
            }
        })
    }
}

function autoFillLink(obj) {
    let graduate = $(obj).parent().siblings('.block_change_graduate').children('.inputs').val();
    let link_base = window.location.href;
    
    if (graduate === '') {
        $(obj).parent().siblings('.block_change_graduate').children('.inputs').focus();
    } else {
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
        formData.append('func_code', '2');
        formData.append('link_base', link_base);
        formData.append('graduate', graduate);

        $.ajax({
            type: 'post',
            url: '/admin/message',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $(obj).siblings('.inputs').val(response['student_link']);
                $(obj).siblings('.inputs').focus();
            }
        })
    }
}

$(function () {
    $('.input_date').datetimepicker({
        language: 'zh-CN',
        format: 'yyyy-mm-dd',
        startView: 2,
        minView: 2,
        autoclose: true,
        todayHighlight: true,
        clearBtn: true
    });
});

function saveMessage(obj) {
    let graduate = $(obj).siblings('.block_change').children('.block_change_graduate').children('.inputs').val();
    let grade = $(obj).siblings('.block_change').children('.block_change_grade').children('.inputs').val();
    let link = $(obj).siblings('.block_change').children('.block_change_link').children('.inputs').val();
    let message = $(obj).siblings('.block_change').children('.block_change_message').children('.textareas').val();
    let date = $(obj).siblings('.block_change').children('.block_change_date').children('.inputs').val();
    if (graduate === '') {
        $(obj).siblings('.block_change').children('.block_change_graduate').children('.inputs').focus();
    } else if (grade === '') {
        $(obj).siblings('.block_change').children('.block_change_grade').children('.inputs').focus();
    } else if (link === '') {
        $(obj).siblings('.block_change').children('.block_change_link').children('.inputs').focus();
    } else if (message === '') {
        $(obj).siblings('.block_change').children('.block_change_message').children('.textareas').focus();
    } else if (date === '') {
        $(obj).siblings('.block_change').children('.block_change_date').children('.inputs').focus();
    } else {
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
        formData.append('func_code', '3');
        formData.append('graduate', graduate);
        formData.append('grade', grade);
        formData.append('link', link);
        formData.append('message', message);
        formData.append('date', date);

        $.ajax({
            type: 'post',
            url: '/admin/message',
            data: formData,
            processData: false,
            contentType: false,
            success: function () {
                $('.correct_alert_text').text('已保存');
                $('.correct_alert').fadeIn(200);
                setTimeout(function () {
                    location.reload();
                }, 400);
            }
        })
    }
}

function cancelMessage() {
    if ($('.operate_panel_item_add').css('display') == 'block') {
        $('.operate_panel_item_add').css('display', 'none');
    }
}

function editAndSaveMessage(obj) {
    if ($(obj).text() == '编辑') {
        $(obj).text('保存');
        $(obj).siblings('.btn_operate_2').text('取消');
        $(obj).siblings('.block_info').css('display', 'none');
        $(obj).siblings('.block_change').css('display', 'block');
    } else {
        let itemId = $(obj).attr('id');
        let graduate = $(obj).siblings('.block_change').children('.block_change_graduate').children('.inputs').val();
        let grade = $(obj).siblings('.block_change').children('.block_change_grade').children('.inputs').val();
        let link = $(obj).siblings('.block_change').children('.block_change_link').children('.inputs').val();
        let message = $(obj).siblings('.block_change').children('.block_change_message').children('.textareas').val();
        let date = $(obj).siblings('.block_change').children('.block_change_date').children('.inputs').val();
        if (graduate === '') {
            $(obj).siblings('.block_change').children('.block_change_graduate').children('.inputs').focus();
        } else if (grade === '') {
            $(obj).siblings('.block_change').children('.block_change_grade').children('.inputs').focus();
        } else if (link === '') {
            $(obj).siblings('.block_change').children('.block_change_link').children('.inputs').focus();
        } else if (message === '') {
            $(obj).siblings('.block_change').children('.block_change_message').children('.textareas').focus();
        } else if (date === '') {
            $(obj).siblings('.block_change').children('.block_change_date').children('.inputs').focus();
        } else {
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
            formData.append('func_code', '4');
            formData.append('itemId', itemId);
            formData.append('graduate', graduate);
            formData.append('grade', grade);
            formData.append('link', link);
            formData.append('message', message);
            formData.append('date', date);

            $.ajax({
                type: 'post',
                url: '/admin/message',
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    if (response['status'] == '1') {
                        $('.correct_alert_text').text('已修改');
                        $('.correct_alert').fadeIn(200);
                        setTimeout(function () {
                            location.reload();
                        }, 400);
                    } else if (response['status'] == '0') {
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
    }
}

function deleteAndCancelMessage(obj) {
    if ($(obj).text() == '删除') {
        let itemId = $(obj).attr('id');
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
        formData.append('func_code', '5');
        formData.append('itemId', itemId);

        $.ajax({
            type: 'post',
            url: '/admin/message',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response['status'] == '1') {
                    $('.correct_alert_text').text('已删除');
                    $('.correct_alert').fadeIn(200);
                    setTimeout(function () {
                        location.reload();
                    }, 400);
                } else if (response['status'] == '0') {
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
    } else {
        $(obj).text('删除');
        $(obj).siblings('.btn_operate_1').text('编辑');
        $(obj).siblings('.block_info').css('display', 'block');
        $(obj).siblings('.block_change').css('display', 'none');

    }
}