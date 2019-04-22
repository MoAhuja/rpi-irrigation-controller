function displayAlert( type, message)
{
    console.log("Displaying alert - " + type);

    var body = `<div class="alert alert-${type} alert-dismissible">
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>`

    $("#alerts_container").append(body);
}

function displayAlertFromXHR( type, xhr)
{
    console.log("Displaying alert - " + type);

    var message = xhr.responseJSON.error + " - " + xhr.responseJSON.field

    var body = `<div class="alert alert-${type} alert-dismissible">
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>`

    $("#alerts_container").append(body);
}