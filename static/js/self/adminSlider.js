function switchToSlider1(obj) {
    $('.operate_panel_1').css({
        'transform': 'translateX(-50%)',
        'transition-duration': '300ms'
    })
    $('.operate_panel_2').css({
        'transform': 'translateX(52%)',
        'transition-duration': '300ms'
    });

    $(obj).css('color', '#090909');
    $('.operate_panel_title_2').css('color', '#6d6d6d');
}

function switchToSlider2(obj) {
    $('.operate_panel_1').css({
        'transform': 'translateX(-152%)',
        'transition-duration': '300ms'
    })
    $('.operate_panel_2').css({
        'transform': 'translateX(-50%)',
        'transition-duration': '300ms'
    });

    $(obj).css('color', '#090909');
    $('.operate_panel_title_1').css('color', '#6d6d6d');
}

function setPath(obj) {
    let path = $(obj);
    let photo = path.prop('files')[0];
    if (!photo) {
        $('.occupy_photo_upload').text('未选择');
    } else {
        $('.occupy_photo_upload').text(photo.name);
    }
}

function clearPath() {
    $('.occupy_photo_upload').text('未选择');
    $('.file_photo').val(null);
}

function editAndSaveSlider1(obj) {
    if ($(obj).text() === '编辑') {
        $(obj).text('保存');
        $(obj).siblings('.block_info').css('display', 'none');
        $(obj).siblings('.block_change').css('display', 'block');
    } else {
        let itemNumber = $(obj).siblings('.item_number').text();
        let title = $(obj).siblings('.block_change').children('.block_change_title').children('.inputs').val();
        let abstract = $(obj).siblings('.block_change').children('.block_change_abstract').children('.textarea_abstract').val();
        let url = $(obj).siblings('.block_change').children('.block_change_url').children('.inputs').val();
        let photos = $(obj).siblings('.block_change').children('.block_change_photo').children('.change_photo').children('.file_photo').prop('files');
        let photo = photos[0];
        let photoPath = $(obj).siblings('.block_change').children('.block_change_photo').children('.change_photo').children('.occupy_photo_upload').text();

        if (title === '') {
            $(obj).siblings('.block_change').children('.block_change_title').children('.inputs').focus();
        } else if (abstract === '') {
            $(obj).siblings('.block_change').children('.block_change_abstract').children('.textarea_abstract').focus();
        } else if (url === '') {
            $(obj).siblings('.block_change').children('.block_change_url').children('.inputs').focus();
        } else if (photoPath === '未选择') {
            $(obj).siblings('.block_change').children('.block_change_photo').children('.change_photo').children('.occupy_photo_upload').css('color', '#903612');
            setTimeout(function () {
                $(obj).siblings('.block_change').children('.block_change_photo').children('.change_photo').children('.occupy_photo_upload').css('color', '#6d6d6d');
            }, 3000);
        } else {
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
            formData.append('func_code', '1');
            formData.append('item_number', itemNumber);
            formData.append('slider_title', title);
            formData.append('slider_abstract', abstract);
            formData.append('slider_url', url);
            formData.append('slider_photo', photo);

            $.ajax({
                type: 'post',
                url: '/admin/slider',
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    $(obj).text('编辑');
                    $(obj).siblings('.block_info').css('display', 'block');
                    $(obj).siblings('.block_change').css('display', 'none');
                    if (response['status'] === '1') {
                        $('.correct_alert').fadeIn(200);
                        setTimeout(function () {
                            location.reload();
                        }, 400);
                    }
                }
            });
        }
    }
}

function editAndSaveSlider2(obj) {
    if ($(obj).text() === '编辑') {
        $(obj).text('保存');
        $(obj).siblings('.block_info').css('display', 'none');
        $(obj).siblings('.block_change').css('display', 'block');
    } else {
        let itemNumber = $(obj).siblings('.item_number').text();
        let title = $(obj).siblings('.block_change').children('.block_change_title').children('.inputs').val();
        let url = $(obj).siblings('.block_change').children('.block_change_url').children('.inputs').val();
        let photos = $(obj).siblings('.block_change').children('.block_change_photo').children('.change_photo').children('.file_photo').prop('files');
        let photo = photos[0];
        let photoPath = $(obj).siblings('.block_change').children('.block_change_photo').children('.change_photo').children('.occupy_photo_upload').text();

        if (title === '') {
            $(obj).siblings('.block_change').children('.block_change_title').children('.inputs').focus();
        } else if (url === '') {
            $(obj).siblings('.block_change').children('.block_change_url').children('.inputs').focus();
        } else if (photoPath === '未选择') {
            $(obj).siblings('.block_change').children('.block_change_photo').children('.change_photo').children('.occupy_photo_upload').css('color', '#903612');
            setTimeout(function () {
                $(obj).siblings('.block_change').children('.block_change_photo').children('.change_photo').children('.occupy_photo_upload').css('color', '#6d6d6d');
            }, 3000);
        } else {
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
            formData.append('func_code', '2');
            formData.append('item_number', itemNumber);
            formData.append('slider_title', title);
            formData.append('slider_url', url);
            formData.append('slider_photo', photo);

            $.ajax({
                type: 'post',
                url: '/admin/slider',
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    $(obj).text('编辑');
                    $(obj).siblings('.block_info').css('display', 'block');
                    $(obj).siblings('.block_change').css('display', 'none');
                    if (response['status'] === '1') {
                        $('.correct_alert').fadeIn(200);
                        setTimeout(function () {
                            location.reload();
                        }, 400);
                    }
                }
            });
        }
    }

}