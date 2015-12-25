showAlert = function(message, alertClass) {
    $('#alert').html('<div class="alert ' + alertClass + ' alert-dismissable fade in"><a href="#" class="close pad-close" data-dismiss="alert" aria-label="close">&times;</a><strong>' + message + '</strong></div>')
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    }
});

$(document).ready(function()
{
    $('input[type=radio]').on('change', function(e) {
        if (!this.checked) {
            return;
        }
        if (this.value == "debt") {
            var o = $('#expense-payee-field');
            o.show();
            o.prop("disabled", false);
        } else if (this.value =="utility") {
            var o = $('#expense-payee-field');
            o.hide();
            o.prop("disabled", true);
        }
    });

    $('[id^=delete_]').on('click', function(e) {
        expense_id = e.target.id.split("_")[1];
        $.ajax({
            type: "POST",
            url: "delete",
            data: {"id": expense_id},
            success: function(data) {
                if ('error' in data) {
                    showAlert(data.error, "alert-warning");
                } else {
                    showAlert("Successfully deleted", "alert-success");
                    $(e.target).parent().parent().remove();
                }
            },
            error: function(data) {
                showAlert("Error reaching server", "alert-danger");
            },
        });
    });

    $('#expense-form').submit(function(e) {
        var b = $('#expense-submit')
        b.button('loading')
        $.ajax({
            type: "POST",
            url: "expense",
            data: $(this).serialize(),
            success: function(data) {
                if ('error' in data) {
                    showAlert(data.error, "alert-warning");
                } else {
                    showAlert("Successfully added", "alert-success");
                    location.reload(true);
                }
                b.button('reset');
            },
            error: function(data) {
                showAlert("Error reaching server", "alert-danger");
                b.button('reset');
            },
        });
        e.preventDefault();
    });


});
