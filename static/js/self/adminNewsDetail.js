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
    $('.input_post_datetime').datetimepicker({
        language: 'zh-CN',
        format: 'yyyy-mm-dd hh:ii:ss',
        startView: 2,
        autoclose: true,
        todayHighlight: true,
        clearBtn: true
    });
})

function submit() {
    let title = $('.input_title').val();
    let category = $("input[name='radios']:checked").val();
    let postDatetime = $('.input_post_datetime').val();
    let author = $('.input_author').val();
    let photographer = $('.input_photographer').val();
    let content = $('.textarea_content').val();
    let photoPath = $('.occupy_photo_upload').text();
    let formData = new FormData();

    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('title', title);
    formData.append('category', category);
    formData.append('post_datetime', postDatetime);
    formData.append('author', author);
    formData.append('photographer', photographer);
    formData.append('content', content);
    formData.append('photo_path', photoPath);

    let photos = $('.file_photo').prop('files');
    for (let i = 0; i < photos.length; i++) {
        let photo = photos[i];
        formData.append('photo', photo);
    }


    const pattern = /\[[^\]]*\]/g;
    let match = content.match(pattern);

    if (title === '') {
        $('.label_tip').show();
        $('.label_tip').text('标题不能为空');
    } else if (!category) {
        $('.label_tip').show();
        $('.label_tip').text('请选择文章类别');
    } else if (author === '') {
        $('.label_tip').show();
        $('.label_tip').text('撰稿人不能为空');
    } else if (photographer === '' && photoPath !== '') {
        $('.label_tip').show();
        $('.label_tip').text('摄影不能为空');
    } else if (content === '') {
        $('.label_tip').show();
        $('.label_tip').text('内容不能为空');
    } else if (match && photoPath === '') {
        $('.label_tip').show();
        $('.label_tip').text('请上传文中涉及的图片');
    } else {
        $('.label_tip').hide();
        const currentURL = $(location).attr('pathname');
        const newsId = currentURL.split('/')[3];
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
                    url: '/admin/news/' + newsId,
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
                                window.location.href = '../news';
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
                });
            }
        });
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
            window.location.href = '../news';
        }
    });
}

