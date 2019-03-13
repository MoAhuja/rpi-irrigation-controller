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