$(document).ready(function()
{
    var scheduleCounter = 0;
    create_zone_template = ""


    $.ajax({
        url: '/static/screens/portal/zone_manager/create/create_zone_include.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            create_zone_template = data
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $("#btn_manager").click(function(){
        

        loadCreateZoneScreen();

    });

    // Load the create zone screen when it's clicked in the navigation menu
    $('body').on('click', '#nav_create_zone', function() {
        loadCreateZoneScreen();
    });

    // Load the static create zone screen
    function loadCreateZoneScreen()
    {
        scheduleCounter = 0;
        
        console.log("Load create zone called. Template = " + create_zone_template)
        modifiedTemplate = create_zone_template

        // Replace all the placeholder values with defaults
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_NAME#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_DESCRIPTION#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_ENABLED#", "UNCHECKED");
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_ID#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#RELAY#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_SHORT#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_DAILY#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_ENABLED#", "UNCHECKED");
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_ENABLED#", "UNCHECKED");
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_MIN#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_MAX#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_ID#", "");

        // Make teh button a create button
        modifiedTemplate = modifiedTemplate.replaceAll("#OPERATION_TYPE#", "Create");
        


        // Loads the create zone content
        $("#content_manager content").html(modifiedTemplate);
        
        // TODO: Disable the create zone link or something
        // TODO: Enable the mnage zone link
    }

    // When the time is selected in the create zone screen, load the time picker module
    $('body').on('click', '.time', function() {
        $(this).timepicker({'step': 10, 'timeFormat': 'H:i'});
    });

    // delete a schedule
    $('body').on('click', '.delButton', function() {
        var id  = $(this).attr('id');
        console.log(id);

        //If they hit delete on the schedule button, then we need to decrement the counter
        if(id == "scheduleDelButton")
        {
            scheduleCounter--;
            console.log("Schedule Counter == " + scheduleCounter);
        }
        $(this).parent().parent().remove();

    });

    // add a schedule
    $('#btnAddSchedule').click(function(){
                        
        $('#ScheduleTable').append('<tr><td><span>Start Time:</span><span><input class ="time" type="text" name="schedule[' + scheduleCounter + '][startTime]" placeholder="6:00 am"/></span></td><td><span>End Time:</span><span><input class="time" type="text" name="schedule[' + scheduleCounter + '][endTime]" placeholder="7:00 am"/></span></td><td class="cellDynamicButton"><button id="scheduleDelButton" class="delButton">Delete</button></td></tr>');
        scheduleCounter++;
    });



     // Handles the submission of the create zone
    $('body').on('click', '#btnCreateZone', function() {
        // e.preventDefault();
        var jsonData = $("#formData").serializeJSON();
        console.log(jsonData);


        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/zone', // url where to submit the request
            type : "POST", // type of action POST || GET
            dataType : 'json', // data type
            data : jsonData, // post data || get data
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                console.log(result);
                displayAlert("success", "Zone added successfully")

                // Hide the form data
                $("#formData").hide()
            },
            error: function(xhr, resp, text) {
                console.log(text);

                displayAlert("danger", "ERROR: To do - parse error message")
            }
        });
    });

    // Start the page with load create zone content
    loadCreateZoneScreen();
     



});