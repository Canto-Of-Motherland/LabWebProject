function submitStatistic(obj) {
    let statistic = $(obj).val();
    let statisticID = $(obj).attr('id');
    let formData = new FormData();

    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('func_code', '1');
    formData.append('statistic', statistic);
    formData.append('statistic_id', statisticID);
    $.ajax({
        type: "post",
        url: '/admin/statistic',
        data: formData,
        processData: false,
        contentType: false,
        success: function () {
            $('.correct_alert').fadeIn(200);
            setTimeout(function () {
                $('.correct_alert').fadeOut(200);
            }, 1600);
        }
    });
}

function autoCalculate(obj) {
    let statistic = $(obj).siblings('.inputs');
    let statisticID = $(obj).siblings('.inputs').attr('id');
    let formData = new FormData();

    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('func_code', '2');
    formData.append('statistic', statistic);
    formData.append('statistic_id', statisticID);

    $.ajax({
        type: "post",
        url: '/admin/statistic',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            $(obj).siblings('.inputs').val(response['statistic_data']);
            $('.correct_alert').fadeIn(200);
            setTimeout(function () {
                $('.correct_alert').fadeOut(200);
            }, 1600);
        }
    })
}