// 内容自适应
setInterval(function () {
    photoHeight = $('.slider_img').height();
    windowHeight = $(window).height();
    if (photoHeight < windowHeight) {
        $('.content').css('top', photoHeight + 'px');
    } else {
        $('.content').css('top', '100vh');
    }
}, 100);
// 底部导航栏自适应
setInterval(function () {
    photoHeight = $('.slider_img').height();
    windowHeight = $(window).height();
    if (photoHeight < windowHeight) {
        $('.footer').css('top', photoHeight + 'px');
    } else {
        $('.footer').css('top', '100vh');
    }
}, 100);
// 向下按钮click事件: 内容滚动到头部
$('.btn_to_content').click(function () { 
    $('html, body').animate({scrollTop: $('.content').offset().top}, 300);
});

// 页面内容布局自适应
function changeMainDisplay() {
    screenWidth = $(window).width();
    if (screenWidth < 880) {
        $('.news_title_text').css({
            'font-weight': '200'
        });
    } else {
        $('.news_title_text').css({
            'font-weight': '600'
        });
    }
}
// 自适应启动
$(document).ready(function () {
    setInterval(function () {
        changeMainDisplay();
    }, 100);
});

counter = 0;

function changeValue(element, value) {
    $({count: 0}).animate({count: value}, {
        duration: 2000,
        step: function () {
            element.text(Math.floor(this.count));
        }
    });
}

let observerNumber = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            if (counter === 0) {
                element1 = $('#number_1');
                element2 = $('#number_2');
                element3 = $('#number_3');
                element4 = $('#number_4');
                element5 = $('#number_5');
                changeValue(element1, value1);
                changeValue(element2, value2);
                changeValue(element3, value3);
                changeValue(element4, value4);
                changeValue(element5, value5);
                $('.background_building').fadeIn(1000);
                setTimeout(function () {
                    $('.slogan_text').fadeIn(300);
                }, 1500);
            }
        }
    });
});


observerNumber.observe($('#number_1')[0]);




