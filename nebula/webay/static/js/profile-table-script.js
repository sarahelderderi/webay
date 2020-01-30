$(document).ready(() => {
    if (window.location.pathname === '/notifications/') {
        getNotifications();
        header = 'Messages';
    } else if (window.location.pathname === '/myItems/') {
        header = 'My Items';
        getMyItems();
    }

    $('#profileTableHeader').text(header)
});

function getNotifications() {
    $.ajax({
        type: "GET",
        url: "/getNotifications/",
        contentType: "application/json",
        success: data => {
            for (const notification of data.notifications) {
                $('#profileTable').append('<tr id="notifRow' + notification.id + '" role="button" class="' + (notification.read_message ? '' : 'font-weight-bold') +
                    '" data-toggle="modal" data-target="#notificationModal" data-id="' + notification.id + '"><td>You won item ' + notification.item_id + '!</td></tr>');
            }

        },
        error: error => {
            alert("Could not fetch details, please try again later.");
        }
    });
}


function getMyItems() {
    $.ajax({
        type: "GET",
        url: "/getMyItems/",
        contentType: "application/json",
        success: data => {
            for (const item of data.items) {
                $('#profileTable').append('<tr><td><a href="/item/' + item.id + '">' + item.title + '</a></td></tr>');
            }

        },
        error: error => {
            alert("Could not fetch details, please try again later.");
        }
    });
}

function getNotificationMessage(id) {
    return $.get({
        url: "/getNotificationMessage/" + id,
        contentType: "text/html",
    });
}

$('#notificationModal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget);
    const id = button.data('id');
    getNotificationMessage(id).done(data => {
        const message = data.replace(/\\n/gm, '<br>');
        const modal = $(this);
        modal.find('.modal-body').html(message);
        markNotificationAsRead(id);
    }).fail(error => {
        alert("Failed to get message details. Try again later.")
    });
});

function markNotificationAsRead(id) {
    $.ajax({
        url: "/markNotificationAsRead/" + id,
        type: "PUT",
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        },
        success: () => {
            //calls method from script.js
            getUnreadNotifNumber().done(data => {
                if (data > 0) {
                    $('.notif-badge').text(data);
                } else {
                    $('.notif-badge').remove()
                }
            });
            $('#notifRow' + id).removeClass("font-weight-bold");
        }
    });
}
