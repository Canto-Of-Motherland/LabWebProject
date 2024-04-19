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

function submit() {
    let title = $('.input_title').val();
    let author = $('.input_author').val();
    let abstract = $('.textarea_abstract').val();
    let date = $('.input_date').val();
    let link = $('.input_link').val();
    let photoPath = $('.occupy_photo_upload').text();
    let formData = new FormData();

    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('title', title);
    formData.append('author', author);
    formData.append('abstract', abstract);
    formData.append('date', date);
    formData.append('link', link);
    formData.append('photo_path', photoPath);

    let photos = $('.file_photo').prop('files');
    let photo = photos[0];
    formData.append('photo', photo);

    if (title === '') {
        $('.label_tip').show();
        $('.label_tip').text('著作标题不能为空');
    } else if (author === '') {
        $('.label_tip').show();
        $('.label_tip').text('著作作者不能为空');
    } else if (abstract === '') {
        $('.label_tip').show();
        $('.label_tip').text('著作摘要不能为空');
    } else if (date === '') {
        $('.label_tip').show();
        $('.label_tip').text('出版日期不能为空');
    } else if (link === '') {
        $('.label_tip').show();
        $('.label_tip').text('著作链接不能为空');
    } else if (photoPath === '未选择') {
        $('.label_tip').show();
        $('.label_tip').text('著作图片不能为空');
    } else {
        $('.label_tip').hide();
        const currentURL = $(location).attr('pathname');
        const workId = currentURL.split('/')[3];
        Swal.fire({
            title: '确认要提交保存吗',
            confirmButtonText: '确　定',
            showCancelButton: true,
            cancelButtonText: '取消',
            icon: 'info',
            width: '400px',
            customClass: {
                confirmButton: 'swal-btn-confirm',
                title: 'swal-title',
                cancelButton: 'swal-btn-cancel',
            }
        }).then(function (result) {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'post',
                    url: '/admin/research-work/' + workId,
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        if (response['status'] === '1') {
                            Swal.fire({
                                title: '保存成功',
                                html: '将在 <b></b> 秒后自动跳转',
                                icon: 'success',
                                timer: 3000,
                                width: '400px',
                                timerProgressBar: true,
                                showConfirmButton: true,
                                confirmButtonText: "确　定",
                                customClass: {
                                    confirmButton: 'swal-btn-confirm',
                                    title: 'swal-title',
                                },
                                onBeforeOpen: () => {
                                    timerInterval = setInterval(() => {
                                        const content = Swal.getContent()
                                        if (content) {
                                            const b = content.querySelector('b');
                                            if (b) {
                                            b.textContent = parseInt(Swal.getTimerLeft() / 1000);
                                            }
                                        }
                                    }, 100)
                                },
                                onClose: () => {
                                    clearInterval(timerInterval);
                                }
                            }).then(() => {
                                window.location.href = '../research-work';
                            });
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
        })
    }
}

function cancel() {
    Swal.fire({
        title: '确认要取消编辑吗',
        confirmButtonText: '确　定',
        showCancelButton: true,
        cancelButtonText: '取消',
        text: '所做编辑将不会被保存，请谨慎操作',
        icon: 'warning',
        width: '400px',
        customClass: {
            confirmButton: 'swal-btn-confirm',
            title: 'swal-title',
            cancelButton: 'swal-btn-cancel',
        }
    }).then(function (result) {
        if (result.isConfirmed) {
            window.location.href = '../research-work';
        }
    });
}