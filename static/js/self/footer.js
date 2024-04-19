function changeFooter() {
    let windowHeightFooter = $(window).height();
    let headPhotoCoverHeight = $('.head_photo_cover').height();
    let contentHeight = $('.content').height();
    let footerHeight = $('.footer').height();
    if (windowHeightFooter > headPhotoCoverHeight + contentHeight + footerHeight) {
        $('.footer').css({
            'position': 'absolute',
            'bottom': '0'
        });
    } else {
        $('.footer').css({
            'position': 'relative',
        })
    }
}

$(window).resize(function () {
    changeFooter();
});

$(document).ready(function () {
    changeFooter();
})