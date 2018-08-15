$(document).ready(function()
{
    var dashboard_template = ""
    var history_template = ""
    var history_header_template = ""
    var current_history_selector = ""



    $.ajax({
        url: '/static/screens/portal/dashboard_include_zone_template.html', // url where to submit the request
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
        url: '/static/screens/portal/dashboard_include_history_row_template.html', // url where to submit the request
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
        url: '/static/screens/portal/dashboard_include_history_header_template.html', // url where to submit the request
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

    // $("#content_dashboard").load("/static/screens/portal/dashboard_include.html");
    $("#btn_dashboard").click(function(){
        
        loadDashboardContent();

    });

    function loadDashboardContent()
    {
        $("#content_dashboard").html("");
        
        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/dashboard', // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'json', // data type
            async: false,
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                system_settings = result['system_settings'];
                zones = result['zones']

                zones.forEach(addZoneToScreen)
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });
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
            next_run_start = item["next_run"]["start"]
            nr_startDate = new Date(next_run_start)
            console.log(nr_startDate)
            next_run_end = item["next_run"]["end"]
            nr_endDate = new Date(item["next_run"]["end"])
            console.log(nr_endDate)
            nextRunString = next_run_start + " - " + next_run_end
        }
        else
        {
            nextRunString = "N/A"
        }

        if(item["last_run"] != null)
        {
            last_run_start = item["last_run"]["start"]
            lr_startDate = new Date(next_run_start)
            console.log(nr_startDate)
            last_run_end = item["last_run"]["end"]
            lr_endDate = new Date(item["next_run"]["end"])
            console.log(nr_endDate)
            lastRunString = last_run_start   + " - " +  last_run_end
        }
        else
        {
            lastRunString = "N/A"
        }

        if(dashboard_template != "")
        {
            var data2 = dashboard_template
            data2 = data2.replaceAll("#NAME#", name)
            data2 = data2.replaceAll("#DESCRIPTION#", description)
            data2 = data2.replaceAll("#ENABLED#", enabled)
            data2 = data2.replaceAll("#NEXT_RUN#", nextRunString )
            data2 = data2.replaceAll("#LAST_RUN#", lastRunString)
            data2 = data2.replaceAll("#CURRENT_STATUS#", is_running)
            data2 = data2.replaceAll("#ID#", id);
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

        // alert(selector);
        // $(selector).toggleClass("hide");
        // $(selector).toggle(500);
    })

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
    }

    function SplitByUppercase(stringToSplit)
    {
        var splitString = stringToSplit.split(/(?=[A-Z])/).join(" ");
        return splitString;

            // return stringToSplit.match(/[A-Z][a-z]+|[0-9]+/g).join(" ");
    }

});