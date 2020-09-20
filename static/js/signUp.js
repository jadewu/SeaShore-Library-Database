$(function() {
    $('#btnSignUp').click(function() {
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            dataType: 'json',
            success: function (result, status, xhr) {
                console.log(result);
                $("#result").html(result.response);
                if (result.response == "user") window.location.href='/customerHome'
                },
            error: function (xhr, status, error) {
                $("#result").html("Error: " + xhr.responseText)
                }
        })
    });
});
