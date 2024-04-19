function setPath(obj) {
    let path = $(obj);
    let photo = path.prop('files')[0];
    if (!photo) {
        $('.occupy_photo_upload').text('未选择');
    } else {
        $('.occupy_photo_upload').text(photo.name);
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
    $('.input_grade').datetimepicker({
        language: 'zh-CN',
        format: 'yyyy',
        startView: 4,
        minView: 4,
        autoclose: true,
        todayHighlight: true,
        clearBtn: true
    });
    $('.input_birthday').datetimepicker({
        language: 'zh-CN',
        format: 'yyyy-mm-dd',
        startView: 2,
        minView: 2,
        autoclose: true,
        todayHighlight: true,
        clearBtn: true
    });
});

function submitForm() {
    let name = $('.input_name').val();
    let gender = $("input[name='radios']:checked").val();
    let grade = $('.input_grade').val();
    let degree = $('.select_grade').val();
    let birthday = $('.input_birthday').val();
    let phone = $('.input_phone').val();
    let email = $('.input_email').val();
    let githubURL = $('.input_github_url').val();
    let csdnURL = $('.input_csdn_url').val();
    let proverb = $('.input_proverb').val();
    let selfIntroduction = $('.textarea_self_introduction').val();
    let major = $('.input_major').val();
    let achievement = $('.textarea_achievement').val();
    let photoPath = $('.occupy_photo_upload').text();
    let formData = new FormData();

    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('name', name);
    formData.append('gender', gender);
    formData.append('grade', grade);
    formData.append('degree', degree);
    formData.append('birthday', birthday);
    formData.append('phone', phone);
    formData.append('email', email);
    formData.append('github_url', githubURL);
    formData.append('csdn_url', csdnURL);
    formData.append('proverb', proverb);
    formData.append('self_introduction', selfIntroduction);
    formData.append('major', major);
    formData.append('achievement', achievement);
    formData.append('photo_path', photoPath);
    
    let photos = $('.file_photo').prop('files');
    let photo = photos[0];
    formData.append('photo', photo);

    const patternBirthday = /^\d{4}-\d{2}-\d{2}$/;
    const patternPhone = /^\d{11}$/;
    const patternEmail = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    
    let matchBirthday = birthday.match(patternBirthday);
    let matchPhone = phone.match(patternPhone);
    let matchEmail = email.match(patternEmail);
    if (name === '') {
        $('.label_tip').show();
        $('.label_tip').text('姓名不能为空');
    } else if (!gender) {
        $('.label_tip').show();
        $('.label_tip').text('请选择性别');
    } else if (grade === '' || !degree) {
        $('.label_tip').show();
        $('.label_tip').text('年级不能为空');
    } else if (birthday !== '' && !matchBirthday) {
        $('.label_tip').show();
        $('.label_tip').text('生日格式不正确');
    } else if (phone !== '' && !matchPhone) {
        $('.label_tip').show();
        $('.label_tip').text('手机号格式不正确');
    } else if (email === '') {
        $('.label_tip').show();
        $('.label_tip').text('邮箱不能为空');
    } else if (!matchEmail) {
        $('.label_tip').show();
        $('.label_tip').text('邮箱格式不正确');
    } else if (major === '') {
        $('.label_tip').show();
        $('.label_tip').text('专业不能为空');
    } else {
        $('.label_tip').hide();
        const currentURL = $(location).attr('pathname');
        const userId = currentURL.split('/')[3];
        Swal.fire({
            title: '确定要提交保存吗',
            confirmButtonText: '确　定',
            showCancelButton: true,
            cancelButtonText: '取 消',
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
                    url: '/admin/user/' + userId,
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
                                window.location.href = '../';
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