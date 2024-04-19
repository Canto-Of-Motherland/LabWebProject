$.ajax({
    type: 'post',
    url: '/research/research-field',
    data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
    success: function (response) {
        const researchFieldList = response['research_field_list']
        for (let i = 0; i < researchFieldList.length; i++) {
            let researchFieldItem = researchFieldList[i];
            if (researchFieldItem.substring(0, 3) === '_1_') {
                $('.content_inner').append('<div class="content_text">' + researchFieldItem.substring(3) + '</div>')
            } else if (researchFieldItem.substring(0, 3) === '_2_') {
                $('.content_inner').append('<img class="content_image" src="/media/'+ researchFieldItem.substring(3) +'">')
            } else if (researchFieldItem.substring(0, 3) === '_3_') {
                $('.content_inner').append('<div class="content_image_title">' + researchFieldItem.substring(3) + '</div>')
            }
        }
    }
})