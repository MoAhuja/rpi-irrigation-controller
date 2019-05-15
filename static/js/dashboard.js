$(document).ready(function()
{
    var dashboard_template = ""
    var history_template = ""
    var history_header_template = ""
    var current_history_selector = ""
    var dashboard_settings_template = ""

    // Initialize all history panels to hide
    console.log("hiding history panels")
    $("historycard").hide();



    $.ajax({
        url: '/static/screens/portal/dashboard/dashboard_include_zone_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            dashboard_template = data
            console.log("Zone template loaded")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/dashboard/dashboard_include_history_row_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            history_template = data;
            console.log("History template loaded");
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/dashboard/dashboard_include_dashboard_settings_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            dashboard_settings_template = data;
            console.log("Dashboard settings template loaded");
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/dashboard/dashboard_include_history_header_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            history_header_template = data;
            console.log("History template loaded");
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    // Default view
    loadDashboardContent();

    // $("#content_dashboard").load("/static/screens/portal/dashboard_include.html");
    $("#btn_dashboard").click(function(){
        loadDashboardContent();

    });

    function loadDashboardContent()
    {
        $("#content_dashboard").html("");

        var alerts_container =  `<div id="alerts_container"></div>`

        $("#content_dashboard").append(alerts_container)
        
        
        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/dashboard', // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'json', // data type
            async: true,
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                system_settings = result['system_settings'];
                zones = result['zones']

                // First we add the header row that has the
                addSystemSettingsToScreen(system_settings);

                zones.forEach(addZoneToScreen)
                $("historycard").hide()

            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });
    }

    function addSystemSettingsToScreen(settings)
    {
        console.log("Adding system settings header");

        var kill_switch = settings["kill_switch"];
        var city = settings["city"];
        var country = settings ["country"];
        var rain_delay = settings["rain_delay"];

        if(rain_delay == null)
        {
            rain_delay = "OFF";
        }

        if(kill_switch == false)
        {
            kill_switch = "OFF"
        }
        else
        {
            kill_switch = "ON";
        }

        var modifiedTemplate = dashboard_settings_template;
        modifiedTemplate = modifiedTemplate.replaceAll("#KILL_SWITCH#", kill_switch);
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_DELAY#", rain_delay);
        modifiedTemplate = modifiedTemplate.replaceAll("#LOCATION#", city + " , " + country);
        

        $("#content_dashboard").append(modifiedTemplate);

    }
    function addZoneToScreen(item, index)
    {  
        console.log(index)
        console.log(item)
        id = item["id"]
        name = item["name"]
        description = item["description"]
        enabled = item["enabled"]
        is_running = item["is_running"]
        if (item["next_run"] != null)
        {
            start = item["next_run"]["start"]
            startDate = Date.parse(start);
            startDateString = toDateString(startDate);
            
            nextRunString = startDateString;
        }
        else
        {
            nextRunString = "N/A"
        }

        if(item["last_run"] != null)
        {
            start = item["last_run"]["start"]
            startDate = Date.parse(start);
            startDateString = toDateString(startDate);
            lastRunString = startDateString;
        }
        else
        {
            lastRunString = "N/A"
        }

        if(dashboard_template != "")
        {
            
            // Set checkmark or x image depending on value
            (enabled ? enabledImage = "check": enabledImage = "x");
            (is_running ? isRunningImage = "check": isRunningImage = "x");

            enabledImageTag = `<img class="status_icon" src="/static/images/${enabledImage}.png" />`;
            isRunningImageTag = `<img class="status_icon" src="/static/images/${isRunningImage}.png" />`;

            var data2 = dashboard_template
            data2 = data2.replaceAll("#NAME#", name)
            data2 = data2.replaceAll("#DESCRIPTION#", description)
            data2 = data2.replaceAll("#ENABLED#", enabledImageTag)
            data2 = data2.replaceAll("#NEXT_RUN#", nextRunString )
            data2 = data2.replaceAll("#LAST_RUN#", lastRunString)
            data2 = data2.replaceAll("#CURRENT_STATUS#", isRunningImageTag)
            data2 = data2.replaceAll("#ID#", id);


            // nextRunDate = Date.parse(next_run_start);
            // alert(nextRunDate);
            
            if(is_running)
            {
                data2 = data2.replaceAll("#STATUS#", "Stop");
                data2 = data2.replaceAll("#STATUS_CLASS#", "Active");
            }
            else
            {
                data2 = data2.replaceAll("#STATUS#", "Start");
                data2 = data2.replaceAll("#STATUS_CLASS#", "Deactive");
            }
            $("#content_dashboard").append(data2);
        }
        else
        {
            console.log("Template is empty, can't populate zones")
        }

    }


    // Load history on click
    $('body').on('click', 'a#history', function() {
        
        // Get the hidden ID field to find the ID of this zone
        var zone_id = $(this).parent().parent().parent().parent().find("#zone_id").text();
        
        // alert(zone_id);
        current_history_selector = "historycard#" + zone_id;

        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/decisionhistory?zone=' + zone_id, // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'json', // data type
            async: true,
            success : function(result) {
                console.log(result)
                decisions = result["DecisionHistory"];
                console.log(decisions);

                // Reset to just the header row
                $(current_history_selector).html(history_header_template);

                decisions.forEach(addDecisionToScreen)
                $(current_history_selector).toggle(500);
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });
    });

    $('body').on('click', 'a#edit', function() {
        
        // Get the hidden ID field to find the ID of this zone
        var zone_id = $(this).parent().parent().parent().parent().find("#zone_id").text();
        
        // alert(zone_id);
        
        // First we need to load the zone manager tab then the edit zone sreen
        
        loadEditZoneScreen(zone_id);

        // Hide the dashboard and load the zone manager screen
        currentlyShowingPanel = $("#content_manager");
        $("#content_dashboard").hide();

        // Hide these ones to start
        $("#content_manager").show()
    });


    // Activation/Deactivation of zone on click
    $('body').on('click', 'a#controller', function() {
        
        // Get the hidden ID field to find the ID of this zone
        var zone_id = $(this).parent().parent().parent().parent().find("#zone_id").text();

        // alert(zone_id);
        
        // Get the current status
        if($(this).hasClass("Active"))
        {
            // Deactivate operation
            // alert("Need to deactivate");
            deactivateZone(zone_id, $(this));
        }
        else
        {
            var duration = prompt("How many minutes should it run?", "30");
            if (duration == null || duration == "") {
                console.log("Duration not provided")
            } else 
            {
                // Check it's a number
                durationInt = parseInt(duration)
                console.log(durationInt)
                if (!isNaN(durationInt))
                {
                    activateZone(zone_id, duration, $(this));
        
                }
                else
                {
                    console.log("Duration specified is not a number")
                }
            }
        }

        

        // alert(selector);
        // $(selector).toggleClass("hide");
        // $(selector).toggle(500);
    });

    function activateZone(zone_id, duration, elementToUpdate)
    {
        // let zone_id_var = zone_id;
        // let duration_var = duration;

        var request = `{"id": ${zone_id}, "duration": ${duration}}`;

        console.log(request);
        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/zones/activate', 
            type : "POST", // type of action POST || GET
            dataType : 'json', // data type
            data: request,
            async: true,
            success : function(result) {
                $(elementToUpdate).html("Stop");
                $(elementToUpdate).removeClass("Deactive");
                $(elementToUpdate).addClass("Active");
            },
            error: function(xhr, resp, text) {
                displayAlert("danger", xhr.responseJSON.error);
            }
        });
    }

    function deactivateZone(zone_id, elementToUpdate)
    {
        // let zone_id_var = zone_id;
        // let duration_var = duration;

        var request = `{"id": ${zone_id}}`;

        console.log(request);
        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/zones/deactivate', 
            type : "POST", // type of action POST || GET
            dataType : 'json', // data type
            data: request,
            async: true,
            success : function(result) {
                $(elementToUpdate).html("Start");
                $(elementToUpdate).removeClass("Active");
                $(elementToUpdate).addClass("Deactive");
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });
    }

    function addDecisionToScreen(item, index)
    {
        console.log(item);
        template = history_template;
        template = template.replaceAll("#DECISION#", SplitByUppercase(item["decision"]));
        template = template.replaceAll("#TIME#", item["event_time"].replaceAll("T", " "));
        template = template.replaceAll("#START_TIME#", item["start_time"].replaceAll("T", " "));
        template = template.replaceAll("#END_TIME#", item["end_time"].replaceAll("T", " "));
        template = template.replaceAll("#REASON#", SplitByUppercase(item["reason"]));
        

        $(current_history_selector).append(template);
    };

    function SplitByUppercase(stringToSplit)
    {
        var splitString = stringToSplit.split(/(?=[A-Z])/).join(" ");
        return splitString;
    };

    function msToTime(duration) 
    {
        var milliseconds = parseInt((duration % 1000) / 100),
          seconds = parseInt((duration / 1000) % 60),
          minutes = parseInt((duration / (1000 * 60)) % 60),
          hours = parseInt((duration / (1000 * 60 * 60)) % 24);
      
        hours = (hours < 10) ? "0" + hours : hours;
        minutes = (minutes < 10) ? "0" + minutes : minutes;
        // seconds = (seconds < 10) ? "0" + seconds : seconds;
      
        if(hours > 0)
        {
            return hours + ":" + minutes + " hours";
        }
        else
        {
            return minutes + " minutes"
        }
        
      }

    function calculateDuration(fromDate, toDate)
    {   
        var diff = Math.abs(fromDate-toDate);
        return msToTime(diff);
    }

    function toDateString(timeAsMilliseconds)
    {
        mlist = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
        dow = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"];


        dateObject = new Date(timeAsMilliseconds);
        // alert(dateObject);
        var dateYear = dateObject.getFullYear();
        var hour = dateObject.getHours();
        var minute = dateObject.getMinutes();

        var dow = dow[dateObject.getDay()];
        var dateMonth = mlist[dateObject.getMonth()];
        var day = dateObject.getDate();
        var dateString = `${dow} ${dateMonth} ${day}`;


        return dateString;

    }

});