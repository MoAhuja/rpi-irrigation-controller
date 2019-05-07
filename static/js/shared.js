currentlyShowingPanel = ""

$(document).ready(function()
{
    currentlyShowingPanel = $("#content_dashboard")
    //Indicate the currently showing panel as the dashboard
    

    // Hide/show content by default
    $(function(){
        // Show this pane to start
        $("#content_dashboard").show();

        // Hide these ones to start
        $("#content_manager").hide()
        
        $("#content_logs").hide()

        $("#content_settings").hide();
    });

    $(".main_nav li").click(function() {
        id = ($(this).attr('id'))
        
        //Find the class that's currently showing and toggle it off
        // $("div.show").hide()
        $(currentlyShowingPanel).hide()

        //Find the panel and toggle teh show class
        panelID = "#" + id.replace("btn", "content")
        // $(panelID).toggleClass("show")
        $(panelID).show("puff")
        currentlyShowingPanel = panelID

    });

});





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