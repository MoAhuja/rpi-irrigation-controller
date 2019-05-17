$(document).ready(function()
{
    logTemplateContent = null;
    pageTemplateContent = null;
    log_page_size = 20
    current_page = 1
    current_log_level = 0




    //Fetch the template content
    if(logTemplateContent == null)
    {
        $.ajax({
            url: '/static/screens/portal/logs_include_log_template.html', // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'html', // data type
            async: true,
            success : function(data) {
                logTemplateContent = data;
                console.log("Loaded log template");
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });
    }

    if(pageTemplateContent == null)
    {
        $.ajax({
            url: '/static/screens/portal/logs_include_page_template.html', // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'html', // data type
            false: true,
            success : function(result) {
                pageTemplateContent = result
                console.log("loaded page template");
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });
    }

    $('body').on('click', '.logLevelFilter', function() {
        id = $(this).attr('id');

        // Parse the number from the id
        current_log_level = id.substr(id.length - 1)

        // Reset teh page count back to 1 
        current_page = 1
        
        // Replace logs
        loadLogs();
        
        $(this).addClass('active');
        $(".logLevelFilter").not($(this)).removeClass('active');
        
    });

    $('body').on('click', '#next_page', function() {
       
        // Increase the log level
        current_page++;

        // Replace logs
        loadLogs();
        
         
    });

    $('body').on('click', '#previous_page', function() {

        // Increase the log level
        current_page--;

        // Replace logs
        loadLogs();
        
         
    });

    // Capture enter press on the page number textbox and change the page accordingly
    $('body').on('keydown', '#page_number', function(e) {  
        console.log(e.keyCode)

        // Enter pressed
        if(e.keyCode == 13) {

            // Get the value from the textbox
            current_page = $(this).val();

            // Reload logs
            loadLogs();
        }
    });

    
    $("#btn_logs").click(function(){
        
        // Load the master template
        loadPageTemplate();

        console.log("Current log level is: " + current_page);

        // Set the default values (all logs + page 1)
        current_log_level = 0
        current_page = 1

        // Then load the first set of loads (all logs)
        loadLogs();

    });

    function loadPageTemplate(){
        $("#content_logs").html("");
        $("#content_logs").html(pageTemplateContent);
    }

    // Loads the logs using the global page and log level settings
    function loadLogs() {
        console.log("Load logs called.")
        console.log("Current Page == " + current_page)
        loadLogsWithValues(current_log_level, current_page)
    }

    // Loads logs with a specific log level nad page number
    function loadLogsWithValues(logLevel, page_number){
       
        // Update the global variable
        current_page = page_number
        current_log_level = logLevel


        $("logs").html("");
        log_level_url = "http://127.0.0.1:5000/service_hub/logs"
        
        // Set the URL based on the log level
        if(logLevel != 0){
            log_level_url = "http://127.0.0.1:5000/service_hub/logs?level=" + logLevel
            
            if(page_number > 0)
            {
                log_level_url = log_level_url + "&page=" + page_number
            }
        }
        else
        {
            if(page_number > 0)
            {
                log_level_url = log_level_url + "?page=" + page_number
            }
        }

        // Append the logs page size
        log_level_url = log_level_url + "&page_size=" + log_page_size


        // Fetch the logs from the service
        $.ajax({
            url: log_level_url, // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'json', // data type
            async: true,
            success : function(result) {
                
                zones = result['LOGS']
                
                if (logTemplateContent != null)
                {
                    // TODO: Add logic to disable "No logs" if there are no logs
                    zones.forEach(addLogToScreen)

                    // Parse the more_logs value and disable the next button if no more logs are 
                    // available
                    has_more_logs = result['has_more']

                    // Enable/Disable the next and previous btutons accordingly
                    determineIfNextButtonShouldBeEnabled(has_more_logs)
                    determineIfPreviousButtonShouldBeEnabled(current_page)

                    // Update the textbox with the current page number
                    updatePageNumberTextboxWithCurrentPage(page_number)
                }
                else
                {
                    console.log("log template not loaded yet");
                }
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });

    }

    function updatePageNumberTextboxWithCurrentPage(page_number)
    {
        $("#page_number").val(page_number)
    }
    function determineIfNextButtonShouldBeEnabled(has_more_logs)
    {
        console.log("determine if next should be disabled. Has more logs =" + has_more_logs)
        if(has_more_logs == true)
        {
            $("#next_page").prop('disabled', false)
        }
        else
        {
            console.log("Going to disable next button")
            $("#next_page").prop('disabled', true)
        }
    }

    function determineIfPreviousButtonShouldBeEnabled(page_number)
    {
        if(page_number <= 1)
        {
            $("#previous_page").prop('disabled', true)
        }
        else
        {
            $("#previous_page").prop('disabled', false)
        }
    }

    function addLogToScreen(item, index)
    {  
        
        timestamp = item["timestamp"]
        timestamp = serverTimeToCommonDateTime(timestamp.replaceAll("T", " "));
        
        component = item["component"]
        message = item["message"]

        if(item["level"] == 1)
        {
            level = "ERROR"
        }
        else if(item["level"] == 2)
        {
            level = "INFO"
        }
        else if(item["level"] == 3)
        {
            level = "DEBUG"
        }

        data = logTemplateContent;

        data = data.replaceAll("#LEVEL#", level)
        data = data.replaceAll("#DATE#", timestamp)
        data = data.replaceAll("#COMPONENT#", component)
        data = data.replaceAll("#MESSAGE#", message)
        // console.log(data)
        $("logs").append(data)
        

    }
    

});