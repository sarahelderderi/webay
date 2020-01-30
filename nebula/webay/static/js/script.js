$(document).ready(() => {
    if (window.location.pathname === '/closedauctions/') {
        $('#searchBar').remove()
    }
    $('#id_dob').attr('type', 'date');
    //$('#id_end_datetime').attr('type', 'datetime-local');
    $('#id_end_datetime').datetimepicker({
        format: 'd/m/Y H:i:s'
    });
    $('#id_start_datetime').datetimepicker({
        format: 'd/m/Y H:i:s'
    });
    readURL = function (input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                $('.avatar').attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    };
    $(".file-upload").on('change', function () {
        readURL(this);
    });

    getUnreadNotifNumber().done(data => {
        if (data > 0) {
            notifBadge = '<span class="notif-badge badge badge-info ml-2">' + data + '</span>';
            $('#navbarDropdownMenuLink').append(notifBadge);
            $('#notificationBtn').append(notifBadge);
            $('#notificationNavLink').append(notifBadge);

        }
    });

    $("#searchButton").click(function () {

        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/search/',
            data: {'search': $('#search').val(), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
            success: handleSuccess,
            error: handleError
        });

        function handleSuccess(data) {
            $('#search-results').html(data);
        }

        function handleError(ThrowError) {
            console.log(ThrowError);
        }
    });
});

function getUnreadNotifNumber() {
    return $.get({
        url: "/getUnreadNotifNumber/",
        contentType: "text/html",
    });
}

//UPLOADING IMAGE USING AJAX.
$(function () {
    $('#img_file').change(function uploadFile() {
        const formdata = new FormData();
        const file = document.getElementById('img_file').files[0];
        formdata.append('img_file', file);
        formdata.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
        $.ajax({
            type: 'POST',
            url: '/updateProfilePic/',
            data: formdata,
            success: function (data) {
                $('#profile-img').attr("src", data);
            },
            error: error => {
                alert('Picture not updated');
                console.log('error', error)
            },
            processData: false,
            contentType: false,
        });
    });
});