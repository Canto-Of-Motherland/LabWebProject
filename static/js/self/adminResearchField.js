function setPath(obj) {
    let photos = $(obj);
    let length = photos.prop('files').length;
    let photoPath = '';
    for (let i = 0; i < length; i++) {
        let photo = photos.prop('files')[i];
        if (i !== length - 1) {
            photoPath = photoPath + photo.name + ' | ';
        } else {
            photoPath = photoPath + photo.name;
        }
    }
    if (photoPath === '') {
        $('.occupy_photo_upload').text('未选择');
    } else {
        $('.occupy_photo_upload').text(photoPath);
    }
    let size = $('.occupy_photo_upload').width();
    $('.btn_clear').css('left', size + 100 + 'px');
}

function clearPath() {
    $('.occupy_photo_upload').text('未选择');
    let size = $('.occupy_photo_upload').width();
    $('.btn_clear').css('left', size + 100 + 'px');
    $('.file_photo').val(null);
}

setInterval(function () {
    let size = $('.occupy_photo_upload').width();
    $('.btn_clear').css('left', size + 100 + 'px');
}, 200);

function save() {
    let content = $('.textarea_content').val();
    let photoPath = $('.occupy_photo_upload').text();
    let formData = new FormData();

    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('content', content);
    formData.append('photo_path', photoPath);

    let photos = $('.file_photo').prop('files');
    for (let i = 0; i < photos.length; i++) {
        let photo  = photos[i];
        formData.append('photo', photo);
    }

    if (content === '') {
        $('.textarea_content').focus();
    } else {
        $.ajax({
            type: 'post',
            url: '/admin/research-field',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response['status'] === '1') {
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
}