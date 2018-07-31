$(document).ready(function()
{
    templateContent = null;

    // $("#content_dashboard").load("/static/screens/portal/dashboard_include.html");
    $("#btn_logs").click(function(){
        $("logs").html("");
        

        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/logs', // url where to submit the request
            type : "GET", // type of action POST || GET
            dataType : 'json', // data type
            async: false,
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                
                zones = result['LOGS']

                //Fetch the template content
                if(templateContent == null)
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


    });

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