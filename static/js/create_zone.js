$(document).ready(function()
{
    // var scheduleCounter = 0;
    create_zone_template = ""
    
    function getAlertContainer()
    {
        return $("alerts#zone_management");
    }

    function scrollToTopOfAlertContainer()
    {
        $("#content_manager content").animate({ scrollTop: 0 }, "fast");
    }

    $.ajax({
        url: '/static/screens/portal/zone_manager/create/create_zone_subcontent_template.html', // url where to submit the request
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
    

    

    // Load the create zone screen when it's clicked in the navigation menu
    $('body').on('click', '#nav_create_zone', function() {
        loadCreateZoneScreen();
    });

    // Load the static create zone screen
    function loadCreateZoneScreen()
    {
        // loadRelayMappings();

        // $.when($.ajax(getHost() + '/service_hub/relays'))
        //     .done(function(relay_data)
        //     {
                //relay_mappings = relay_data;
                
        scheduleCounter = 0;

        console.log("Load create zone called. Template = " + create_zone_template)
        modifiedTemplate = create_zone_template

        // Replace all the placeholder values with defaults
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_NAME#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_DESCRIPTION#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_ENABLED#", "UNCHECKED");
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_ID#", "");
        // modifiedTemplate = modifiedTemplate.replaceAll("#RELAY#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_SHORT#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_DAILY#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#RAIN_ENABLED#", "UNCHECKED");
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_ENABLED#", "UNCHECKED");
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_MIN#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#TEMP_MAX#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#ZONE_ID#", "");
        modifiedTemplate = modifiedTemplate.replaceAll("#OPERATION_TYPE#", "Create");
        
        //Convert template to DOM so we can use jQuery to edit it
        
        // Find the select tag
        var templateAsDOM = $($.parseHTML(modifiedTemplate));
        loadRelayDropdownIntoTemplate(templateAsDOM, null);
        
        $("#content_manager content subcontent").html(templateAsDOM);
        
        // TODO: Disable the create zone link or something
        // TODO: Enable the mnage zone link

            // });
        
    }

    
    // When the time is selected in the create zone screen, load the time picker module
    $('body').on('click', '.time', function() {
        $(this).timepicker({'step': 10, 'timeFormat': 'H:i'});
    });

    // delete a schedule
    $('body').on('click', '#btnDeleteSchedule', function() {
        // var id  = $(this).attr('id');
        // console.log(id);

        //If they hit delete on the schedule button, then we need to decrement the counter
        // if(id == "scheduleDelButton")
        // {
        scheduleCounter--;
        console.log("Schedule Counter == " + scheduleCounter);
        // }
        
        $(this).parent().parent().remove();

    });

    

    $('body').on('click', '#btnAddSchedule', function() {
        // TODO: Move to only do this once.
        $.get("/static/screens/portal/zone_manager/create/schedule_template_include.html", function(data){
            var templateWithRealData = data.replaceAll("NUMBER_HOLDER", scheduleCounter)
            templateWithRealData = templateWithRealData.replaceAll("#START_TIME#", "");
            templateWithRealData = templateWithRealData.replaceAll("#END_TIME#", "");
            $("#schedule_area").append(templateWithRealData);
            scheduleCounter++
        });
    });


     // Handles the submission of the create zone
    $('body').on('click', '#btnCreateZone', function() {
        // e.preventDefault();
        var jsonData = $("#formData").serializeJSON();
        console.log(jsonData);


        $.ajax({
            url: getHost() + '/service_hub/zone', // url where to submit the request
            type : "POST", // type of action POST || GET
            dataType : 'json', // data type
            data : jsonData, // post data || get data
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                console.log(result);
                displayAlertInContainer(getAlertContainer(), "success", "Zone added successfully")
                scrollToTopOfAlertContainer(); 
                clearZoneData();
                $("#formData").hide()
            },
            error: function(xhr, resp, text) {
                console.log(text);

                displayAlertInContainerFromXHR(getAlertContainer(), "danger", xhr)
                scrollToTopOfAlertContainer();
            }
        });
    });

    // Start the page with load create zone content
    loadCreateZoneScreen();
     



});