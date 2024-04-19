const currentURL = $(location).attr('pathname');
const newsId = currentURL.split('/')[2];

$.ajax({
    type: 'post',
    url: '/news/' + newsId,
    data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
    success: function (response) {
        const newsContentList = response['news_content_list']
        for (let i = 0; i < newsContentList.length; i++) {
            let newsContentItem = newsContentList[i];
            if (newsContentItem.substring(0, 3) === '_1_') {
                $('.news_content').append('<div class="news_content_text">' + newsContentItem.substring(3) + '</div>')
            } else if (newsContentItem.substring(0, 3) === '_2_') {
                $('.news_content').append('<img class="news_image" src="/media/'+ newsContentItem.substring(3) +'">')
            } else if (newsContentItem.substring(0, 3) === '_3_') {
                $('.news_content').append('<div class="news_image_title">' + newsContentItem.substring(3) + '</div>')
            }
        }
    }
})