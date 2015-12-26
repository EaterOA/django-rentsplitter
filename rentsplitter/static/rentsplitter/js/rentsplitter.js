$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    }
});

function showAlert(message, alertClass) {
    $('#alert').html('<div class="alert ' + alertClass + ' alert-dismissable fade in"><a href="#" class="close pad-close" data-dismiss="alert" aria-label="close">&times;</a><strong>' + message + '</strong></div>')
}

function deleteExpense(button) {
    expense_id = button.attr('id').split("_")[1];
    $.ajax({
        type: "POST",
        url: "delete",
        data: {"id": expense_id},
        success: function(data) {
            if ('error' in data) {
                showAlert(data.error, "alert-warning");
            } else {
                location.reload();
            }
        },
        error: function(data) {
            showAlert("Error reaching server", "alert-danger");
        },
    });
}

function addExpense(form) {
    var b = $('#expense-submit')
    b.button('loading')
    $.ajax({
        type: "POST",
        url: "expense",
        data: form.serialize(),
        success: function(data) {
            if ('error' in data) {
                showAlert(data.error, "alert-warning");
            } else {
                location.reload();
            }
            b.button('reset');
        },
        error: function(data) {
            showAlert("Error reaching server", "alert-danger");
            b.button('reset');
        },
    });
}

$(document).ready(function()
{
    // set up radio button to hide/unhide payee field
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
    if ($('input[value="debt"]')[0].checked) {
        var o = $('#expense-payee-field');
        o.show();
        o.prop("disabled", false);
    }

    // add handler for expense delete buttons
    $('[id^=delete_]').on('click', function(e) {
        deleteExpense($(e.target));
    });

    // add handler for form submission
    $('#expense-form').submit(function(e) {
        addExpense($(this));
        e.preventDefault();
    });
});
