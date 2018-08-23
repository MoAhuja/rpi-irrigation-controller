$(document).ready(function()
{
    page_template = "";
    notification_template = "";
    push_bullet_input_user_row_template = ""
    number_of_users = 0;
    notificationConfigData = ""
    pushBulletUsers = ""


    $.ajax({
        url: '/static/screens/portal/settings/include_pushbullet_input_user_row_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            push_bullet_input_user_row_template = data
            console.log("Push Bullet Input user template")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/settings/include_settings_page_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            page_template = data
            console.log("Settings page template loaded")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/settings/include_push_notification_settings_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            notification_template = data
            console.log("Push notification template loaded")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $("#btn_settings").click(function(){

        loadPageTemplate();

    });

    $('body').on('click', '#nav_system_settings', function() {
        loadSystemSettings();
    });

    $('body').on('click', '#nav_push_notifications', function() {
        loadPushNotificationSettings();
    });

    $('body').on('click', '#add_pb_user', function() {
        addPushBulletUserInputRow();
    });


    $('body').on('click', '#save_pb', function() {
        savePushBulletSettings();
    });

    $('body').on('click', '#save_notification_settings', function() {
        saveNotificationSettings();
    });
    
    


    function loadPageTemplate()
    {
        $("#content_settings").html(page_template);
    }

    function loadSystemSettings()
    {
        $("#content_settings content").html("System");
    }

    function loadPushNotificationSettings()
    {
        notificationConfigData = ""
        step = 0

        // $.when(loadConfigData(), loadPushBulletUsersData()).then(drawScreen(), drawErrorScreen())
        $.when(
            $.get('http://127.0.0.1:5000/service_hub/settings/notification/config', function(data){
                console.log("Loaded config data: " + data);
                notificationConfigData = data;

            }), $.get('http://127.0.0.1:5000/service_hub/settings/notification/pushbullet/users', function(data){
                console.log("Loaded user data: " + data);
                pushBulletUsers = data;
            })).then(drawScreen, drawErrorScreen);
    }

    // function loadConfigData()
    // {
    //     var deferred = $.Deferred();

    //     $.ajax({
    //         url: 'http://127.0.0.1:5000/service_hub/settings/notification/config', // url where to submit the request
    //         type : "GET", // type of action POST || GET
    //         dataType : 'json', // data type
    //         async: true,
    //         success : function(data) {
                
    //             console.log("Fetched notification config")
    //             // console.log(data)
    //             notificationConfigData = data
    //             deferred.resolve(data);
    //             // return deferred.promise();
    //         },
    //         error: function(xhr, resp, text) {
    //             console.log(text);
    //             deferred.reject("ERROR: " + xhr.status);
    //             // return deferred.promise();  
    //         }
    //     });

    //     return deferred.promise();
        
    // }

    // function loadPushBulletUsersData()
    // {
    //     var deferred = $.Deferred();

    //     $.ajax({
    //         url: 'http://127.0.0.1:5000/service_hub/settings/notification/pushbullet/users', // url where to submit the request
    //         type : "GET", // type of action POST || GET
    //         dataType : 'json', // data type
    //         async: true,
    //         success : function(data) {
                
    //             console.log("Fetched pushbullet users config")
    //             // console.log(data)
    //             pushBulletUsers = data
    //             deferred.resolve(data);

    //         },
    //         error: function(xhr, resp, text) {
    //             console.log(text);
    //             deferred.resolve(text);
    //         }
    //     });

    //     return deferred.promise();

    // }

    function drawScreen()
    {
        console.log("Draw screen invoked!");
        console.log(notificationConfigData);
        console.log(pushBulletUsers);

        // Update template with the real data
        temp = notification_template;
        temp = temp.replaceAll("#NOTIFY_ON_WATERING_START_CHECKED#", (notificationConfigData["notify_on_watering_start"] == true) ? "checked": "");
        temp = temp.replaceAll("#NOTIFY_ON_WATERING_STOP_CHECKED#", (notificationConfigData["notify_on_watering_stop"] == true) ? "checked": "");
        temp = temp.replaceAll("#NOTIFY_ON_ERROR_CHECKED#", (notificationConfigData["notify_on_error"] == true) ? "checked": "");
        $("#content_settings content").html(temp);

        // Add the users
        pushBulletUsers["users"].forEach(addPushBulletUserInputRowWithData);
        
    }

    function drawErrorScreen()
    {
        console.log("ERROR SCREEN")
    }


    function addPushBulletUserInputRow()
    {
        curTemplate = push_bullet_input_user_row_template;
        curTemplate = curTemplate.replaceAll("NUMBER_HOLDER", number_of_users++);
        curTemplate = curTemplate.replaceAll("#NAME#", "");
        curTemplate = curTemplate.replaceAll("#API_KEY#", "");
        $("#pushbullet_users").append(curTemplate);
    }

    function addPushBulletUserInputRowWithData(item, index)
    {
        name = item["name"];
        apikey = item["api_key"];

        curTemplate = push_bullet_input_user_row_template;
        curTemplate = curTemplate.replaceAll("NUMBER_HOLDER", number_of_users++);
        curTemplate = curTemplate.replaceAll("#NAME#", name);
        curTemplate = curTemplate.replaceAll("#API_KEY#", apikey);
        $("#pushbullet_users").append(curTemplate);
    }

    function savePushBulletSettings()
    {
        // TODO: Fill in the API call to save push bullet settings
        var jsonData = $("#pbform").serializeJSON();
        
        console.log(jsonData);

        // $("#pbform")
    }

    function saveNotificationSettings()
    {
        // TODO: Fill in the API call to save push bullet settings
        var jsonData = $("#notification_settings").serializeJSON();
        
        jsonData = jsonData.replaceAll("\"True\"", "true");
        console.log(jsonData);
        $.ajax({
            url: 'http://localhost:5000/service_hub/settings/notification/config', // url where to submit the request
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
    }
});