function subNavigationIn(objClass) {
    // $('.nav_out').hide();
    $('.nav_out_' + objClass).fadeIn(150);
    $('.split_el').css('width', '100%');
}

function subNavigationOut(objClass) {
    if (!$('.el_' + objClass).is(':hover') && !$('.nav_out_' + objClass).is(':hover') && !$('.split_el').is(':hover')) {
        $('.nav_out').fadeOut(150);
        $('.split_el').css('width', '0%');
    }
}

$('.el_1').mouseover(function () {
    subNavigationIn('1');
});

$('.el_1, .nav_out_1').mouseleave(function () {
    subNavigationOut('1');
});

$('.el_2').mouseover(function () { 
    subNavigationIn('2');
});

$('.el_2, .nav_out_2').mouseleave(function () {
    subNavigationOut('2');
});

$('.el_3').mouseover(function () { 
    subNavigationIn('3');
});

$('.el_3, .nav_out_3').mouseleave(function () {
    subNavigationOut('3');
});

$('.el_5').mouseover(function () { 
    subNavigationIn('5');
});

$('.el_5, .nav_out_5').mouseleave(function () {
    subNavigationOut('5');
});

$('.svg_navigation_cover').mouseover(function () {
    setTimeout(function () {
        $('.nav_hide').css({
            'transform': 'translateY(0)',
            'transition-duration': '1000ms'
        });
    }, 50);
});

$('.svg_navigation_cover').click(function () {
    setTimeout(function () {
        $('.nav_hide').css({
            'transform': 'translateY(0)',
            'transition-duration': '1000ms'
        });
    }, 50);
});

$('.svg_close').click(function () {
    setTimeout(function () {
        $('.nav_hide').css({
            'transform': 'translateY(calc(-100% - 80px))',
            'transition-duration': '1000ms'
        });
    }, 50);
});

function changeDisplay() {
    screenWidth = $(window).width();
    screenHeight = $(window).height();
    if (screenWidth <= 890 && screenWidth >= 690) {
        $('.nav').fadeOut(200);
        $('.svg_navigation').fadeIn(200);
        $('.svg_navigation').css('right', '22vw');
        $('.svg_navigation_cover').fadeIn(200);
        $('.svg_navigation_cover').css('right', '22vw');
        $('.init_show').fadeOut(200);
        $('.user').fadeIn(200);
        $('.svg_search_active').fadeIn(200);
        $('.search_active').fadeIn(200);
        $('.side_label').fadeOut(200);
    } else if (screenWidth < 690) {
        $('.nav').fadeOut(200);
        $('.svg_navigation').fadeIn(200);
        $('.svg_navigation').css('right', '2vw');
        $('.svg_navigation_cover').fadeIn(200);
        $('.svg_navigation_cover').css('right', '2vw');
        $('.init_show').fadeOut(200);
        $('.user').fadeOut(200);
        $('.svg_search_active').fadeOut(200);
        $('.search_active').fadeOut(200);
        $('.side_label').fadeIn(200);
    } else {
        $('.nav').fadeIn(200);
        $('.svg_navigation').fadeOut(200);
        $('.svg_navigation_cover').fadeOut(200);
        $('.init_show').fadeIn(200);
        $('.user').fadeIn(200);
        $('.svg_search_active').fadeOut(200);
        $('.search_active').fadeOut(200);
        $('.side_label').fadeOut(200);
    }   
    if (screenWidth >= 770) {
        $('.nav_out').css('min-height', '9vw');
        $('.svg_building').css({
            'height': '14vw',
            'bottom': '-2vw'
        });
    } else {
        $('.nav_out').css('min-height', '70px');
        $('.svg_building').css({
            'height': '108px',
            'bottom': '-15px'
        });
    }
}

$(document).ready(function () {
    timerChangeDisplay = setInterval(function () {
        changeDisplay();
    }, 100);
});

$('.init_show').mouseover(function () {
    clearInterval(timerChangeDisplay);
    timerChangeDisplay = null;
});

$('.init_show').mouseleave(function () {
    timerChangeDisplay = setInterval(function () {
        changeDisplay();
    }, 100);
});

$('.input_search').blur(function () { 
    timerChangeDisplay = setInterval(function () {
        changeDisplay();
    }, 100);
});

$('.search_active').mouseover(function () { 
    clearInterval(timerChangeDisplay);
    timerChangeDisplay = null;
    $('.init_show').fadeIn(200);
    $('.svg_search_active').fadeOut(200);
    $('.search_active').fadeOut(200);
});


$(window).scroll(function () { 
    let elementPosition = $('.content').offset().top;
    let scrollPosition = $(this).scrollTop();
    if (elementPosition <= scrollPosition) {
        setTimeout(function () {
            $('.navigation').css({
                'background-image': 'none',
                'background-color': '#ffffff',
                'box-shadow': '0 5px 5px 2px rgba(0, 0, 0, 0.2)',
                'transition-duration': '0.3s'
            });
            $('.svg_whu').css({
                'transform': 'translate(-100vw, -50%)',
                'filter': 'drop-shadow(#903612 100vw 0)'
            });
            $('.svg_dasi').css({
                'transform': 'translate(-100vw, -50%)',
                'filter': 'drop-shadow(#903612 100vw 0)'
            });
            $('.el').css({
                'color': '#090909'
            });
            $('.input_search').css({
                'background-color': '#eee5db'
            });
            $('.svg_navigation').css({
                'transform': 'translate(-100vw, -50%)',
                'filter': 'drop-shadow(#903612 100vw 0)'
            });
            $('.occupy').css({
                'background-color': '#eee5db'
            });
            $('.svg_search_active').css({
                'filter': 'drop-shadow(#903612 100vw 0)'
            });
            $('.user_name').css({
                'color': '#090909'
            });
        });
    } else {
        setTimeout(function () {
            $('.navigation').css({
                'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0))',
                'background-color': 'transparent',
                'box-shadow': 'none',
                'transition-duration': '0.3s'
            });
            $('.svg_whu').css({
                'transform': 'translateY(-50%)',
                'filter': 'none'
            });
            $('.svg_dasi').css({
                'transform': 'translateY(-50%)',
                'filter': 'none'
            });
            $('.el').css({
                'color': '#ffffff'
            });
            $('.svg_navigation').css({
                'transform': 'translateY(-50%)',
                'filter': 'none'
            });
            $('.input_search').css({
                'background-color': '#ffffff'
            });
            $('.occupy').css({
                'background-color': '#ffffff'
            });
            $('.svg_search_active').css({
                'filter': 'drop-shadow(#ffffff 100vw 0)'
            })
            $('.user_name').css({
                'color': '#ffffff'
            });
        });
    }
});

function search(obj) {
    let keyWord = $(obj).siblings('input').val();
    if (keyWord !== '') {
        window.location.href = '/search?key=' + keyWord;
    }
}

function searchEnter(obj, event) {
    if (event.keyCode === 13) {
        let keyWord = $(obj).val();
        if (keyWord !== '') {
            window.location.href = '/search?key=' + keyWord;
        }
    }
}