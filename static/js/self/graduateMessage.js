let current = 0;
let dataLength = 0;

function loadData(start) {
    formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append("start", start);
    current = current + 10;
    $.ajax({
        type: 'post',
        url: '/graduate/message',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            let dataMessage = data['message_data_list']
            dataLength = dataMessage.length;
            dataMessage.forEach(message => {
                let messageItem = $('<div>').addClass('message_item').attr('id', message['message_id']);
                $('.content_grid').append(messageItem);
                let messageContent = $('<div>').addClass('message_content').text(message['message_content']);
                let messageGraduate = $('<a>').addClass('message_graduate').text(message['message_graduate'] + ' · ' + message['message_grade']).attr('href', message['message_link'])
                let messageDate = $('<div>').addClass('message_date').text(message['message_date']);
                $('#' + message['message_id']).append(messageContent, messageGraduate, messageDate);
            });
        }
    });
}

function initMasonry() {
    $('.content_grid').masonry({
        itemSelector: '.message_item',
        columnWidth: '.message_item',
        gutter: 10,
        fitWidth: true,
    });
}

function resetMasonry() {
    $('.content_grid').masonry('reloadItems');
    $('.content_grid').masonry('layout');
}


window.onload = function() {
    loadData(current);
    setTimeout(function () {
        initMasonry();
    }, 200);
};

function continueLoad() {
    $('.tip').text('加载中...');
    loadData(current);
    setTimeout(function () {
        if (dataLength === 0) {
            $('.tip').text('我是有底线的');
        } else {
            resetMasonry();
            $('.tip').text('点击加载更多');
        }
    }, 200);
};