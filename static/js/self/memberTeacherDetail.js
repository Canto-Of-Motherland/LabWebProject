$(window).scroll(function () {
    changeLeft();
});

$(window).resize(function () {
    changeLeft();
})

function changeLeft() {
    let mainPosition = $('.content').offset().top;
    let scrollMainPosition = $(this).scrollTop();
    let footerPosition = $('.footer').offset().top;
    let windowHeight = $(window).height();
    let item2Position = $('.content_main_right').children('#2').offset().top;
    let item3Position = $('.content_main_right').children('#3').offset().top;
    let item4Position = $('.content_main_right').children('#4').offset().top;
    let item5Position = $('.content_main_right').children('#5').offset().top;
    let item6Position = $('.content_main_right').children('#6').offset().top;
    let item7Position = $('.content_main_right').children('#7').offset().top;
    let item8Position = $('.content_main_right').children('#8').offset().top;
    let item9Position = $('.content_main_right').children('#9').offset().top;
    let item10Position = $('.content_main_right').children('#10').offset().top;
    let item11Position = $('.content_main_right').children('#11').offset().top;
    if (mainPosition <= scrollMainPosition) {
        $('.content_main_left').css({
            'position': 'fixed',
            'top': '130px',
        });
    } else {
        $('.content_main_left').css({
            'position': 'absolute',
            'top': '10px'
        });
    }
    if (footerPosition < (windowHeight + scrollMainPosition)) {
        $('.content_main_left').css({
            'height': 'calc(100vh - 180px - ' + (windowHeight + scrollMainPosition - footerPosition).toString() + 'px)'
        });
    }
    if (item2Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#1'));
    } else if (item2Position - 100 <= scrollMainPosition && item3Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#2'));
    } else if (item3Position - 100 <= scrollMainPosition && item4Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#3'));
    } else if (item4Position - 100 <= scrollMainPosition && item5Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#4'));
    } else if (item5Position - 100 <= scrollMainPosition && item6Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#5'));
    } else if (item6Position - 100 <= scrollMainPosition && item7Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#6'));
    } else if (item7Position - 100 <= scrollMainPosition && item8Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#7'));
    } else if (item8Position - 100 <= scrollMainPosition && item9Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#8'));
    } else if (item9Position - 100 <= scrollMainPosition && item10Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#9'));
    } else if (item10Position - 100 <= scrollMainPosition && item11Position - 100 > scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#10'));
    } else if (item11Position - 100 <= scrollMainPosition) {
        changeActiveAuto($('.content_main_left').children('#11'));
    }
}

function changeActiveAuto(obj) {
    $('.left_item').children('.left_item_vertical').css({
        'background-color': '#c3c3c3',
        'width': '1px'
    });
    $('.left_item').children('.left_item_title').css({
        'color': '#6d6d6d',
        'transform': 'translateX(0)'
    });
    $(obj).children('.left_item_vertical').css({
        'background-color': '#903612',
        'width': '2px'
    });
    $(obj).children('.left_item_title').css({
        'color': '#903612',
        'transform': 'translateX(3px)'
    });
}

function changeActive(obj) {
    $('.left_item').children('.left_item_vertical').css({
        'background-color': '#c3c3c3',
        'width': '1px'
    });
    $('.left_item').children('.left_item_title').css({
        'color': '#6d6d6d',
        'transform': 'translateX(0)'
    });
    $(obj).children('.left_item_vertical').css({
        'background-color': '#903612',
        'width': '2px'
    });
    $(obj).children('.left_item_title').css({
        'color': '#903612',
        'transform': 'translateX(3px)'
    });
    titleID = $(obj).attr('id');
    $('html, body').animate({scrollTop: $('.content_main_right').children('#' + titleID).offset().top - 100}, 500, 'swing');
}