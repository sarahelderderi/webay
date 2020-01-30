$(document).ready(() => {
    $('#div_id_password').remove();
    $('#div_id_confirm_pw').remove();
    $('#updateProfileDetails input[name="username"]').attr('disabled', 'disabled');
    getUserDetails();
    $('#updateProfileDetails').on('submit', (event) => {
        event.preventDefault();
        updateProfileDetails();
    });
});


/* ********************************
        AJAX REQUESTS
******************************** */

function getUserDetails() {
    $.ajax({
        type: "GET",
        url: "/getUserDetails/",
        contentType: "application/json",
        success: data => {
            $('#updateProfileDetails input[name="username"]').val(data.username);
            $('#updateProfileDetails input[name="first_name"]').val(data.first_name);
            $('#updateProfileDetails input[name="last_name"]').val(data.last_name);
            $('#updateProfileDetails input[name="email"]').val(data.email);
            $('#updateProfileDetails input[name="dob"]').val(data.dob);
            $('#updateProfileDetails input[name="address"]').val(data.address);
            $('#updateProfileDetails input[name="mobile"]').val(data.mobile);
        },
        error: error => {
            alert("Could not fetch details, please try again later.");
        }
    });
}

function updateProfileDetails() {
    const array = $("#updateProfileDetails").serializeArray();
    $.ajax({
        url: "/updateProfile/",
        type: "PUT",
        data: array,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        },
        success: () => {
            alert("updated successfully!");
        },
        error: error => {
            alert('Error.\nPlease ensure details are valid.\n' + error.responseText)
        }
    });
}