function addThesis() {
    $('.edit_panel').attr('id', '')
    $('.edit_panel').attr('name', '0');
    $('.edit_panel').fadeIn(200);
}

function cancelThesis() {
    $('.inputs').val('');
    $('.edit_panel').fadeOut(0);
}

function editThesis(obj) {
    let id = $(obj).siblings('.to_thesis').attr('id');
    let title = $(obj).siblings('.to_thesis').text();
    let author = $(obj).siblings('.item_author').text();
    let date = $(obj).siblings('.item_date').text().slice(5);
    let link = $(obj).siblings('.to_thesis').attr('href');

    $('.input_title').val(title);
    $('.input_author').val(author);
    $('.input_date').val(date);
    $('.input_link').val(link);
    $('.edit_panel').attr('id', id);
    $('.edit_panel').attr('name', '1');
    $('.edit_panel').fadeIn(200);
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

function saveThesis() {
    let id = $('.edit_panel').attr('id');
    let signal = $('.edit_panel').attr('name');
    let title = $('.input_title').val();
    let author = $('.input_author').val();
    let date = $('.input_date').val();
    let link = $('.input_link').val();

    if (title === '') {
        $('.input_title').focus();
    } else if (author === '') {
        $('.input_author').focus();
    } else if (date === '') {
        $('.input_date').focus();
    } else if (link === '') {
        $('.input_link').focus();
    } else {
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
        formData.append('func_code', '1');
        formData.append('signal', signal);
        formData.append('thesis_id', id);
        formData.append('thesis_title', title);
        formData.append('thesis_author', author);
        formData.append('thesis_date', date);
        formData.append('thesis_link', link);

        $.ajax({
            type: 'post',
            url: '/admin/research-thesis',
            data: formData,
            processData: false,
            contentType: false,
            success: function () {
                $('.edit_panel').fadeOut(0);
                $('.correct_alert_text').text('已保存');
                $('.correct_alert').fadeIn(200);
                setTimeout(function () {
                    location.reload();
                }, 400);
            }
        });
    }
}

function deleteThesis(obj) {
    let date = $(obj).siblings('.item_date').text().slice(5);
    let formData = new FormData();

    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('func_code', '2');
    formData.append('thesis_date', date);

    $.ajax({
        type: 'post',
        url: '/admin/research-thesis',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response['status'] === '1') {
                $('.edit_panel').fadeOut(0);
                $('.correct_alert_text').text('已删除');
                $('.correct_alert').fadeIn(200);
                setTimeout(function () {
                    location.reload();
                }, 400);
            } else if (response['status'] === '0') {
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
