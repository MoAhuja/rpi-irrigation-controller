String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

$(document).ready(function(){
           
    var scheduleCounter = 0;
    manage_zone_row_template = ""
    manage_zone_page_template = ""
    manage_zone_schedule_template = ""
    
    // Prefetch content

    $.ajax({
        url: '/static/screens/portal/zone_manager/manage/manage_zone_row_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            manage_zone_row_template = data
            console.log("Manage zone template loaded")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/zone_manager/manage/manage_zone_schedule_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            manage_zone_schedule_template = data
            console.log("Manage zone schedule template loaded")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/zone_manager/manage/manage_zone_page_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            manage_zone_page_template = data
            console.log("Manage zone page template loaded")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    

    $('body').on('click', '#nav_manage_zone', function() {
        loadManageZoneScreen();
    });

    $('body').on('click', '#nav_manage_zone', function() {
        loadManageZoneScreen();
    });

    

    // Overload to support displaying of alert notification after zones are loaded
    function loadManageZoneScreenWithAlert(alertType, alertContent)
    {
        console.log("Load manage zone screen with alert invoked")
        loadManageZoneScreen();
        displayAlert(alertType, alertContent);

    }

    function loadManageZoneScreen()
    {
        console.log("Load manage zone screen invoked")
        
        $("#content_manager content").html(manage_zone_page_template);

        
        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/zones', // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'json', // data type
            async: true,
            success : function(result) {
                console.log(result)
                result.forEach(addZoneToManageZoneScreen)

            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });

    }

    function addZoneToManageZoneScreen(zone)
    {

        console.log("Evaluating zone")
        console.log(zone)

        zone.temperature.min= (zone.temperature.min==""? "N/A": zone.temperature.min)
        zone.temperature.max = (zone.temperature.max==""? "N/A": zone.temperature.max)
        zone.relay = (zone.relay == null ? "None Assigned": zone.relay)

        // Fetch the template and replace the elements
        var modifiedTemplate = manage_zone_row_template;

        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_NAME#", zone.zone_name);
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_DESCRIPTION#", zone.zone_description);
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_ENABLED#", zone.enabled);
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_ID#", zone.id);
        modifiedTemplate = modifiedTemplate.replaceAll("#RELAY#", zone.relay);
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_SHORT#", zone.rain.shortTermExpectedRainAmount);
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_DAILY#", zone.rain.dailyExpectedRainAmount);
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_ENABLED#", zone.rain.enabled);
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_ENABLED#", zone.temperature.enabled);
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_MIN#", zone.temperature.min);
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_MAX#", zone.temperature.max);
        
        var zone_dom = $($.parseHTML(modifiedTemplate));

        // TODO: Add schedule
        // Find the schedule section in teh template
        zone.schedule.forEach(function(curSchedule)
        {
            
            // Load the template
            scheduleTemplate = manage_zone_schedule_template
            scheduleTemplate = scheduleTemplate.replaceAll("#SCHEDULE_ENABLED#", curSchedule.enabled)
            scheduleTemplate = scheduleTemplate.replaceAll("#START_TIME#", curSchedule.startTime)
            scheduleTemplate = scheduleTemplate.replaceAll("#END_TIME#", curSchedule.endTime)
            scheduleTemplate = scheduleTemplate.replaceAll("#SCHEDULE_TYPE#", curSchedule.schedule_type)
            
            // Convert to DOM
            var schedule_dom = $($.parseHTML(scheduleTemplate));

            // Indicate which days were selected
            curSchedule.days.forEach(function(day)
            {
                // $("#day_" + day, $(scheduleTemplate).context).addClass("enabled")
                day_dom = schedule_dom.find("#day_" + day)

                day_dom.addClass("enabled")
                img_dom = day_dom.find("img")
                img_dom.removeClass("disabled")
                img_dom.addClass("enabled")
            });
            
           
            // Add schedule to the zone data
            zone_dom.find('schedules').append(schedule_dom)

           
        });

        // Add it to the manage zones div
        $("manage_zones").append(zone_dom)
    }

    // Time picker hook
    $('body').on('click', '.time', function() {
        $(this).timepicker({'step': 10, 'timeFormat': 'H:i'});
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
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });
    });

    // Handles the "Add Schedule" button
    // TODO: Prefetch this once and re-use.
    $('body').on('click', '#btnAddSchedule', function() {
        $.get("/static/screens/portal/zone_manager/create/schedule_template_include.html", function(data){
            var data2 = data.replaceAll("NUMBER_HOLDER", scheduleCounter)
            $("#schedule_area").append(data2);
            scheduleCounter++
        });
    });

    // Side menu navigation - hides zone cards, shows create zone
    $("#nav_create_zone").click(function(){
        // hide the others
        $("zonecards").hide()
        $("createzone").show()
    });

    // Side menu navigation - hides create zone, shows all zones
    $("#nav_view_zone").click(function(){
        // hide the others
        $("zonecards").show()
        $("createzone").hide()

    });

    // Catch the press of the delete button in the zone manager screen
    $('body').on('click', '.delete_zone', function() {
        id_string = ($(this).attr('id'))
        index_of_underscore = id_string.indexOf("_")
        id = id_string.substr(index_of_underscore+1)
        
        deleteZone(id)
    });

    // Catch the press of the edit zone button in the zone manager screen
    $('body').on('click', '.edit_zone', function() {
        id_string = ($(this).attr('id'))
        index_of_underscore = id_string.indexOf("_")
        id = id_string.substr(index_of_underscore+1)

        alert("Edit zone clicked. Id = " + id);
    });


    // Delete a zone by calling the REST APi
    function deleteZone(id)
    {
        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/zone/' + id,
            type : "DELETE", // type of action POST || GET
            async: true,
            contentType: 'application/json',
            success : function(data) {
                loadManageZoneScreenWithAlert("success", "Zone deleted successfully. ");
                
            },
            error: function(xhr, resp, text) {
                // alert("Unable to delete zone -> " + id)
                displayAlert("danger", "Failed to delete zone")
            }
        });
    }


    //Eligible types = success, info, warning, danger
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


});
