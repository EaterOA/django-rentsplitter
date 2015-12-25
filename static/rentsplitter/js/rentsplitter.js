showAlert = function(message, alertClass) {
    $('#alert').html('<div class="alert ' + alertClass + ' alert-dismissable fade in"><a href="#" class="close pad-close" data-dismiss="alert" aria-label="close">&times;</a><strong>' + message + '</strong></div>')
}

$(document).ready(function()
{
    $('input[type=radio]').on('change', function(e) {
        if (!this.checked) {
            return;
        }
        if (this.value == "d") {
            var o = $('#expense-owed-field');
            o.show();
            o.prop("disabled", false);
        } else if (this.value =="u") {
            var o = $('#expense-owed-field');
            o.hide();
            o.prop("disabled", true);
        }
    });

    $('#expense-form').submit(function(e) {
        var b = $('#expense-submit')
        b.button('loading')
        $.ajax({
            type: "POST",
            url: "expense",
            data: $(this).serialize(),
            success: function(data) {
                showAlert("Successfully added", "alert-success");
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