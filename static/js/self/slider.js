$(document).ready(function () {
    function changeSlider() {
        photoHeight = $('.slider_img').height();
        windowHeight = $(window).height();
        if (photoHeight < windowHeight) {
            $('.slider').css('height', photoHeight + 'px');
            $('.img_group').css('height', photoHeight + 'px');
            $('.info_slider').css('height', photoHeight + 'px');
            $('.title_slider').css('font-size', photoHeight / 150 + 'vh');
        } else {
            $('.slider').css('height', '100%');
            $('.img_group').css('height', '100%');
            $('.info_slider').css('height', '100%');
            $('.title_slider').css('font-size', '4vh');
        }
    }
    changeSlider();
    setInterval(function () {
        changeSlider();
    }, 100);
});

$(function () {
    $('.info_slider, .btn_change_left, .btn_change_right, .number a').mouseover(function () {
        clearInterval(timer);
        timer = null
    });

    $('.info_slider, .btn_change_left, .btn_change_right, .number a').mouseleave(function () {
        timer = setInterval(function () {
            $(".btn_change_right").click();
        }, 3000);
    });

    let num = 5;
    let number = 0;
    $('.number a').eq(0).addClass('current_label');
    $('.number a').on('click', function () {
        number = parseInt($(this).text()) - 1;
        $('.number a').eq(number).addClass('current_label').siblings().removeClass('current_label');
        $('.img_group').animate({
            'left': (100 * (-number - 1)).toString() + 'vw',
        }, 800, 'swing');
    });

    let firstImg = $('.img_group').children(0)[0].cloneNode(true);
    let lastImg = $('.img_group').children(0)[4].cloneNode(true);
    $(".img_group").append(firstImg);
    $(".img_group").prepend(lastImg);

    let flag = true;

    $('.btn_change_right').on('click', function () {
        if (flag) {
            flag = false;
            number++;
            if (number >= 6) {
                $('.img_group').css('left', '-100vw');
                number = 1;
            }
            getSlide();
        }
    });

    $('.btn_change_left').on('click', function () {
        if (flag) {
            flag = false;
            number--;
            if (number <= -1) {
                $('.img_group').css('left', '-600vw');
                number = 4;
            }
            getSlide();
        }
    });

    function getSlide() {
        $('.img_group').animate({
            'left': (100 * (-number - 1)).toString() + 'vw',
        }, 800, 'swing', function () {
            flag = true;
        });

        if (number >= 5) {
            num = 0;
        } else {
            num = number;
        }
        $('.number a').eq(num).addClass('current_label').siblings().removeClass('current_label');
    }
    timer = setInterval(function () {
        $('.btn_change_right').click();
    }, 3000);
});

$('.info_slider_occupy, .title_slider, .split_slider, .abstract_slider').mouseover(function () { 
    $('.info_slider_occupy').css({
        'top': '72%',
        'visibility': 'visible',
    });
    $('.title_slider').css({
        'top': '72%',
        'transition-duration': '0.3s'
    });
    $('.split_slider').css({
        'top': '82%',
        'visibility': 'visible',
        'transition-duration': '0.3s'
    });
    $('.abstract_slider').css({
        'top': '84%',
        'visibility': 'visible',
        'transition-duration': '0.3s'
    });
});

$('.info_slider_occupy, .title_slider, .split_slider, .abstract_slider').mouseleave(function () { 
    $('.info_slider_occupy').css({
        'top': '80%',
        'visibility': 'hidden',
    });
    $('.title_slider').css({
        'top': '80%',
        'transition-duration': '0.3s'
    });
    $('.split_slider').css({
        'top': '90%',
        'visibility': 'hidden',
        'transition-duration': '0.3s'
    });
    $('.abstract_slider').css({
        'top': '92%',
        'visibility': 'hidden',
        'transition-duration': '0.3s'
    });
});

