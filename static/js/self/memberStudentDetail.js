function changeInfoBlock(obj) {
    $('.title_dot').css({
        'border': '#c3c3c3 2px solid',
        'background-color': 'transparent'
    });
    $('.title_text').css('color', '#c3c3c3');
    $('.title_connect').css({
        'background-size': '0% 100%',
        'transition-duration': '150ms',
    });
    $(obj).children('.title_dot').css({
        'border': '#903612 2px solid',
        'background-color': '#903612'
    });
    $(obj).children('.title_text').css({
        'color': '#903612',
        'transition-duration': '150ms'
    });
    $(obj).children('.title_connect').css({
        'background-size': '100% 100%',
        'transition-duration': '150ms',
    });
    
    let dotID = parseInt($(obj).attr('id'));
    $('.content_main_left_inner').css('transform', 'translateY(' + String(-11 - dotID * 62) + 'px)');
    $('.content_main_right_inner').css('transform', 'translateY(' + String(-dotID * 25) + '%)');
}

$(document).ready(function () {
    changeInfoBlock($('.title_info').first());
});