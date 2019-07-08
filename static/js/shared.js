currentlyShowingPanel = ""

$(document).ready(function()
{
    currentlyShowingPanel = $("#content_dashboard");
    loadTheme();
    //Indicate the currently showing panel as the dashboard
    

    

    


    function loadTheme()
    {
        console.log("loading theme");
        $.get("/service_hub/settings/display/theme", function(data){
            theme = data.value;
            setTheme(theme);
        });
    }




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

function setTheme(selectedTheme)
{
    var urlOfThemeFile = "/static/css/colours/" + selectedTheme;
    $("#theme-colour").attr('href', urlOfThemeFile);
}

function serverTimeToCommonDateTime(serverDateString)
{
    console.log("parsing: " + serverDateString)
    
    dateAsMilliseconds = Date.parse(serverDateString);

    console.log("Result: " + dateAsMilliseconds);
    dateObject = new Date(dateAsMilliseconds);
    var options = { year: '2-digit', month: 'numeric', day: 'numeric', hour12: 'true' };
    var dateString = dateObject.toLocaleDateString('en-US', options);
    var timeString = dateObject.toLocaleTimeString('en-US')

    return `${dateString} ${timeString}`
}

function serverTimestamptoHumanReadableDate(serverDateString)
{
    
    mlist = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ];
    dow = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"];


    dateAsMilliseconds = Date.parse(serverDateString);

    dateObject = new Date(dateAsMilliseconds);
    // // alert(dateObject);
    // var dateYear = dateObject.getFullYear();
    // var hour = dateObject.getHours();
    // var minute = dateObject.getMinutes();

    // var dow = dow[dateObject.getDay()];
    // var dateMonth = mlist[dateObject.getMonth()];
    // var day = dateObject.getDate();
    // var dateString = `${dow} ${dateMonth} ${day}`;

    var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric', hour12: 'true' };

    return dateObject.toLocaleDateString('default', options);

    // return dateString;
}



function displayAlertInContainer(container, type, message)
{
    if((type == null) || (message == null))
    {
        return;
    }

    console.log("Displaying alert - " + type);

    var body = `<div class="alert alert-${type} alert-dismissible">
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>`

    container.append(body);
}

function displayAlertInContainerFromXHR(container, type, xhr)
{
    console.log("Displaying alert - " + type);

    var message = xhr.responseJSON.error + " - " + xhr.responseJSON.field

    var body = `<div class="alert alert-${type} alert-dismissible">
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>`

    container.append(body);
}

function getHost()
{
    var currentLocation = window.location.toString();
    var indexOfDomain = currentLocation.indexOf("//");
    var indexOfPath = currentLocation.indexOf("/", indexOfDomain+2);
    var host = currentLocation.substring(0, indexOfPath);

    return host;
}
