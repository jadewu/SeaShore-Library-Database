$(function() {
    $('#btnRequest').click(function() {
        $.ajax({
            url: '/cusRequest',
            data: $('form').serialize(),
            type: 'POST',
            dataType: 'json',
            success: function (result, status, xhr) {
                console.log(result);
                $("#result").html(result.response);
                if (result.response == "success") window.location.href='/showBill'
                },
            error: function (xhr, status, error) {
                $("#result").html("Error: " + xhr.responseText)
                }
        })
    });
});
