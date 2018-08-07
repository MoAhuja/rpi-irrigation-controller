$(document).ready(function()
{
    logTemplateContent = null;
    pageTemplateContent = null;

    // Handles the "Add Schedule" button
    $('body').on('click', '.logLevelFilter', function() {
        id = $(this).attr('id');

        // Parse the number from the id
        var lastChar = id.substr(id.length - 1)

        // Replace logs
        loadLogs(lastChar);
        
        $(this).addClass('active');
        $(".logLevelFilter").not($(this)).removeClass('active');
        
         
    });

    
    // $("#content_dashboard").load("/static/screens/portal/dashboard_include.html");
    $("#btn_logs").click(function(){
        
        // Load the master template
        loadPageTemplate();

        // Then load the first set of loads (all logs)
        loadLogs(0);

    });

    function loadPageTemplate(){
        $("#content_logs").html("");

        if(pageTemplateContent == null)
        {
            $.ajax({
                url: '/static/screens/portal/logs_include_page_template.html', // url where to submit the request
                type : "GET", // type of action POST || GET
                dataType : 'html', // data type
                false: true,
                success : function(result) {
                    pageTemplateContent = result
                },
                error: function(xhr, resp, text) {
                    console.log(text);
                }
            });
        }

        $("#content_logs").html(pageTemplateContent);


    }
    function loadLogs(logLevel){
        $("logs").html("");
        log_level_url = "http://127.0.0.1:5000/service_hub/logs"
        
        // Set the URL based on the log level
        if(logLevel != 0){
            log_level_url = "http://127.0.0.1:5000/service_hub/logs?level=" + logLevel
        }
        

        $.ajax({
            url: log_level_url, // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'json', // data type
            async: true,
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                
                zones = result['LOGS']

                //Fetch the template content
                if(logTemplateContent == null)
                {
                    $.ajax({
                        url: '/static/screens/portal/logs_include_log_template.html', // url where to submit the request
                        type : "GET", // type of action POST || GET
                        dataType : 'html', // data type
                        async: false,
                        success : function(data) {
                            templateContent = data;
                        },
                        error: function(xhr, resp, text) {
                            console.log(text);
                        }
                    });
                }

                zones.forEach(addLogToScreen)
            },
            error: function(xhr, resp, text) {
                console.log(text);
            }
        });

    }
    function addLogToScreen(item, index)
    {  
        // console.log(item)
        
        timestamp = item["timestamp"]
        timestamp = timestamp.replaceAll("T", " ");
        
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

        data = templateContent;

        data = data.replaceAll("#LEVEL#", level)
        data = data.replaceAll("#DATE#", timestamp)
        data = data.replaceAll("#COMPONENT#", component)
        data = data.replaceAll("#MESSAGE#", message)
        // console.log(data)
        $("logs").append(data)
        

    }
    

});