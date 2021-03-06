$(document).ready(function()
{
    var zone_card_template = ""
    var dashboard_page_template = "";
    var history_template = ""
    var history_header_template = ""
    var history_id = 0;
    var current_history_selector = ""
    var dashboard_settings_template = ""


    // Initialize all history panels to hide
    console.log("hiding history panels")
    $("historycard").hide();
    $("history_details").hide();

    function getAlertsContainer() {

        return $("alerts#dashboard");
    }


    $.ajax({
        url: '/static/screens/portal/dashboard/dashboard_include_zone_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            zone_card_template = data
            console.log("Zone template loaded")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/dashboard/dashboard_page_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            dashboard_page_template = data
            console.log("Page template loaded")
            loadDashboardContent();

            
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
    
    $("#btn_dashboard").click(function(){
        loadDashboardContent();
    });

    function loadDashboardContent()
    {
        $("#content_dashboard").html(dashboard_page_template);
        
        $.ajax({
            url: getHost() + '/service_hub/dashboard', // url where to submit the request
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
        var engine_last_ran = settings["engine_last_ran"]
        var system_time = settings["system_time"]

        if(rain_delay == null)
        {
            rain_delay = "OFF";
        }
        else
        {
            rain_delay = serverTimestamptoHumanReadableDate(rain_delay)
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
        modifiedTemplate = modifiedTemplate.replaceAll("#ENGINE_LAST_RAN#", serverTimeToCommonDateTime(engine_last_ran))
        modifiedTemplate = modifiedTemplate.replaceAll("#SYSTEM_TIME#", serverTimeToCommonDateTime(system_time))
        

        $("subcontent#dashboard").append(modifiedTemplate);

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
            
            startDateString = serverTimeToCommonDateTime(start);
            
            nextRunString = startDateString;
        }
        else
        {
            nextRunString = "N/A"
        }

        if(item["last_run"] != null)
        {
            start = item["last_run"]["start"]
            startDateString = serverTimeToCommonDateTime(start);
            lastRunString = startDateString;
        }
        else
        {
            lastRunString = "N/A"
        }

        if(zone_card_template != "")
        {
            
            // Set checkmark or x image depending on value
            (enabled ? enabledImage = "check": enabledImage = "x");
            (is_running ? isRunningImage = "check": isRunningImage = "x");

            enabledImageTag = `<img class="status_icon" src="/static/images/${enabledImage}.png" />`;
            isRunningImageTag = `<img class="status_icon" src="/static/images/${isRunningImage}.png" />`;

            var modifiedTemplate = zone_card_template
            modifiedTemplate = modifiedTemplate.replaceAll("#NAME#", name)
            modifiedTemplate = modifiedTemplate.replaceAll("#DESCRIPTION#", description)
            modifiedTemplate = modifiedTemplate.replaceAll("#ENABLED#", enabledImageTag)
            modifiedTemplate = modifiedTemplate.replaceAll("#NEXT_RUN#", nextRunString )
            modifiedTemplate = modifiedTemplate.replaceAll("#LAST_RUN#", lastRunString)
            modifiedTemplate = modifiedTemplate.replaceAll("#CURRENT_STATUS#", isRunningImageTag)
            modifiedTemplate = modifiedTemplate.replaceAll("#ID#", id);


            // nextRunDate = Date.parse(next_run_start);
            // alert(nextRunDate);
            
            if(is_running)
            {
                modifiedTemplate = modifiedTemplate.replaceAll("#STATUS#", "Stop");
                modifiedTemplate = modifiedTemplate.replaceAll("#STATUS_CLASS#", "Active");
            }
            else
            {
                modifiedTemplate = modifiedTemplate.replaceAll("#STATUS#", "Start");
                modifiedTemplate = modifiedTemplate.replaceAll("#STATUS_CLASS#", "Deactive");
            }
            $("subcontent#dashboard").append(modifiedTemplate);
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
                     
        history_id = 0;

        // alert(zone_id);
        current_history_selector = "historycard#" + zone_id;

        $.ajax({
            url: getHost() + '/service_hub/decisionhistory?zone=' + zone_id, // url where to submit the request
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
                $("history_details").hide();
                $(current_history_selector).toggle(500);
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });
    });

    $('body').on('click', '.decisiondetails', function() {
        //Find the next decision details
        var id = $(this).attr('id');
        var indexOfUnderscope = id.lastIndexOf('_');
        history_id = id.substring(indexOfUnderscope+1);

        var decisiondetailsSelector = "#history_details_" + history_id;
        $(decisiondetailsSelector).toggle(500);
    })

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
            url: getHost() + '/service_hub/zones/activate', 
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
                displayAlertInContainerFromXHR(getAlertsContainer(), "danger", xhr);
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
            url: getHost() + '/service_hub/zones/deactivate', 
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

    function getYesNoNA(item)
    {
        if((item == null) || (item == ""))
        {
            return "N/A"
        }
        else if(item == true)
        {
            return "Yes"
        }
        else
        {
            return "No"
        }
    }

    function getValueOrNA(item)
    {
        if((item == null) || (item == ""))
        {
            return "N/A"
        }
        else
        {
            return item;
        }
        
    }

    function addDecisionToScreen(item, index)
    {
        history_id++;
        console.log(item);
        template = history_template;

        template = template.replaceAll("#HISTORY_ID#", history_id);
        template = template.replaceAll("#DECISION#", SplitByUppercase(item["decision"]));
        template = template.replaceAll("#TIME#", serverTimeToCommonDateTime(item["event_time"].replaceAll("T", " ")));
        template = template.replaceAll("#START_TIME#", serverTimeToCommonDateTime(item["start_time"].replaceAll("T", " ")));
        template = template.replaceAll("#END_TIME#", serverTimeToCommonDateTime(item["end_time"].replaceAll("T", " ")));
        template = template.replaceAll("#REASON#", SplitByUppercase(item["reason"]));
        template = template.replaceAll("#TEMP_ENABLED#", (getYesNoNA(item["temperature_enabled"])));
        template = template.replaceAll("#RAIN_ENABLED#", (getYesNoNA(item["rain_enabled"])));
        template = template.replaceAll("#CURRENT_TEMP#", getValueOrNA(item["current_temp"]));
        template = template.replaceAll("#RAIN_SHORT_TERM#", getValueOrNA(item["current_3_hour_rain_forecast"]));
        template = template.replaceAll("#TEMP_LOWER_LIMIT#", getValueOrNA(item["temperature_lower_limit"]));
        template = template.replaceAll("#RAIN_SHORT_TERM_LIMIT#", getValueOrNA(item["rain_short_term_limit"]));
        template = template.replaceAll("#TEMP_UPPER_LIMIT#", getValueOrNA(item["temperature_upper_limit"]))
        template = template.replaceAll("#RAIN_DAILY_LIMIT#", getValueOrNA(item["rain_daily_limit"]));
        template = template.replaceAll("#RAIN_DAILY#", getValueOrNA(item["current_daily_rain_forecast"]));
        
        // now replace all the details

        // <hdl>Short Term Rain:</hdl><hdc>#RAIN_SHORT_TERM#</hdc>
        // <hdl>Temp Lower Limit:</hdl><hdc>#TEMP_LOWER_LIMIT#</hdc>
        // <hdl>Short Term Rain Limit:</hdl><hdc>#RAIN_SHORT_TERM_LIMIT#</hdc>
        // <hdl>Temp Upper Limit:</hdl><hdc>#TEMP_UPPER_LIMIT#</hdc>
        // <hdl>&nbsp;</hdl><hdc>&nbsp;</hdc>
        // <hdl>Daily Rain Limit:</hdl><hdc>#RAIN_DAILY_LIMIT#</hdc>
        

        // <!-- "current_temp": null,
        //     "current_3_hour_rain_forecast": null,
        //     "current_daily_rain_forecast": null,
        //     "temperature_enabled": null,
        //     "temperature_lower_limit": null,
        //     "temperature_upper_limit": null,
        //     "rain_enabled": null,
        //     "rain_short_term_limit": null,
        //     "rain_daily_limit": null, -->

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

    
    

});