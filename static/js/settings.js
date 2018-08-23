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

    $('body').on('click', '#del_pb_user', function() {
        // Get the name of the user
        console.log($(this).parent());

        name = $(this).parent().find("#name").val();

        deletePushBulletUser(name);
       
    });

    $('body').on('click', '#save_pb_user', function() {
        // Get the name of the user
        
        name = $(this).parent().find("#name").val();
        key = $(this).parent().find("#key").val();
        

        addPushBulletUser(name, key);
       
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
        curTemplate = curTemplate.replaceAll("#PLACEHOLDER_FOR_BUTTON#", "<button id='save_pb_user'>Save</button>");
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
        curTemplate = curTemplate.replaceAll("#IS_DISABLED#", "disabled");
        curTemplate = curTemplate.replaceAll("#PLACEHOLDER_FOR_BUTTON#", "<button id='del_pb_user'>Del</button>");
        
        $("#pushbullet_users").append(curTemplate);
    }

    function addPushBulletUser(name, key)
    {
        jsonData = `{"name": "${name}", "api_key": "${key}"}`

        $.post("/service_hub/settings/notification/pushbullet/user", jsonData);
        
    }
    function deletePushBulletUser(name)
    {
        
        $.ajax({
            url: 'http://127.0.0.1:5000/service_hub/settings/notification/pushbullet/user/' + name, // url where to submit the request
            type : "DELETE", // type of action POST || GET || DELETE
            dataType : 'json', // data type
            // data : jsonData, // post data || get data
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

    function savePushBulletSettings()
    {
        // TODO: Fill in the API call to save push bullet settings
        var jsonData = $("#pbform").serializeJSON();
        
        console.log(jsonData);

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