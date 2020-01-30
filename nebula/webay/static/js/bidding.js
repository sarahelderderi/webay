$(document).ready(() => {
    const item_id = $('#itemRow').attr('item_id');
    getAllBids(item_id);
    $('#bidForm').on('submit', (event) => {
        event.preventDefault();
        addBid(item_id);
        getAllBids(item_id);
    });

    $(".deleteItemBtn").on("click", function () {
        const id = this.id;
        $.ajax({
            url: `/item/${id}`,
            method: "DELETE",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
            },
            success: () => {
                alert("Item deleted. Redirecting to my items.");
                window.location.replace('/myItems/')
            },
            error: () => {
                alert("Item not deleted. Try again later.");
            }

        })
    });
});

function setMinBidValue(minVal) {
    $('#bidAmount').attr('min', minVal)
}

function getAllBids(id) {
    $('#biddingList tr:not(:first)').remove();
    $.ajax({
        type: "GET",
        url: `/getAllBids/${id}`,
        contentType: "application/json",
        success: data => {
            if (data.bids.length <= 0) {
                $('#biddingList').append(`<tr><td>No bids were made for this item.</td></tr>`);
            } else {
                setMinBidValue(data.bids[0].amount);
                for (const bid of data.bids) {
                    const date = new Date(bid.bid_datetime);
                    $('#biddingList').append(`<tr><td>${bid.user}</td><td>${bid.amount}</td><td>${date}</td></tr>`);
                }
            }
        },
        error: error => {
            alert("Could not fetch details, please try again later.");
        }
    });
}

function addBid(id) {
    const array = $("#bidForm").serializeArray();
    const limit = $("#bidAmount").attr('min');
    let bidAmount = $("#bidAmount").val();
    bidAmount = Number(bidAmount).toFixed(2);
    if (bidAmount < limit) {
        alert('Invalid bid amount');
        return;
    }
    const dataObj = {
        'item_id': id,
        'amount': bidAmount,
        'csrfmiddlewaretoken': array[0].value
    };
    $.ajax({
        url: `/item/${id}/`,
        method: "POST",
        data: dataObj,
        success: () => {
            alert("this bid worked. Yay!");

        },
        error: error => {
            if (error.status === 400) {
                alert(error.responseText);
            } else {
                alert("The bid for item did not work. Contact your admin :D");
            }
        }
    })
}
