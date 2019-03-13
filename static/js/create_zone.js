$(document).ready(function()
{
    var scheduleCounter = 0;


    // Load the create zone screen when it's clicked in the navigation menu
    $('body').on('click', '#nav_create_zone', function() {
        loadCreateZoneScreen();
    });

    // Load the static create zone screen
    function loadCreateZoneScreen()
    {
        // Loads the create zone content
        $("#content_manager content").load("/static/screens/portal/zone_manager/create/create_zone_include.html");
        
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


    // Form submission to create zone
    $("form").submit(function(e){
                        
        e.preventDefault();
        var jsonData = $("form#formData").serializeJSON();
        console.log(jsonData);


        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/zones/create_zone', // url where to submit the request
            type : "POST", // type of action POST || GET
            dataType : 'json', // data type
            data : jsonData, // post data || get data
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                console.log(result);
                
                alert(result)
                // TODO: Change content to display successful creation?
            },
            error: function(xhr, resp, text) {
                console.log(text);
                alert("Zone creation failed")

                // TODO: Change content to display successful creation?

            }
        });
    });

    // Start the page with load create zone content
    loadCreateZoneScreen();
     



});