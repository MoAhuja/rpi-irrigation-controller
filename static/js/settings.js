$(document).ready(function()
{
    page_template = "";
    system_settings_template = ""
    notification_template = "";
    push_bullet_input_user_row_template = ""
    number_of_users = 0;
    notificationConfigData = ""
    pushBulletUsers = ""
    kill_switch_modified = false
    rain_delay_modified = false


    $.get('/static/screens/portal/settings/include_system_settings_template.html', 
    function(data)
    {
        system_settings_template = data;
        console.log("System settings template loaded")
    });

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

    $('body').on('change', '#kill_switch', function() {
        console.log("kill switch toggled");
        kill_switch_modified = true
        enableSaveButton();
    });

    $('body').on('input', '#rain_delay', function() {
        console.log("rain delay modified");
        rain_delay_modified = true
        enableSaveButton();
    });

    $('body').on('click', '#save_system_settings', function() {
        // saveSystem settings
        saveSystemSettings();
    });

    

    function saveSystemSettings()
    {
        $.when(
            callKillSwitchService(), 
            callRainDelayService())
        .done(function(a1, a2){
            console.log("Both promises resolved")
            if((a1[0] == 200 && a2[0] == 200))
            {
                console.log("Saved successfully");
                savedSuccessfully();
            }
            else
            {
                if(a1[0]!= 200)
                {
                    console.log("KS != 200 ");
                    displayAlert(a1[1]);
                }

                if(a2[0] != 200)
                {
                    console.log("RD != 200");
                    displayAlert(a2[1]);
                }
            }
        });
    }

    function callKillSwitchService()
    {
        var deferredPromise = jQuery.Deferred();
        
        if(kill_switch_modified == true)
        {

            kill_switch_value = $("#kill_switch").prop('checked')
            ks_request = `{"value": ${kill_switch_value}}`
            console.log("Kill switch request  is " + ks_request);

            $.ajax({
                url: 'http://localhost:5000/service_hub/settings/kill', // url where to submit the request
                type : "POST", // type of action POST || GET || DELETE
                dataType : 'json', // data type
                data : ks_request, // post data || get data
                contentType: "application/json; charset=utf-8",
                async: true,
                success : function(result) {
                    deferredPromise.resolve(200, "")
                },
                error: function(xhr, resp, text) {
                    deferredPromise.resolve(xhr.status, text)
                }
            });
        }
        else
        {
            console.log('Kill switch not modified - Resolving Promise');
            deferredPromise.resolve(200, "");
        }

        

        return deferredPromise.promise();
    }

    function callRainDelayService()
    {
        var deferredPromise = jQuery.Deferred();
        
        if(rain_delay_modified == true)
        {
            rain_delay_value = $("#rain_delay").val();

            rd_request = `{"value": "${rain_delay_value}"}`
    
            console.log(rd_request);
            

            $.ajax({
                url: 'http://localhost:5000/service_hub/settings/raindelay', // url where to submit the request
                type : "POST", // type of action POST || GET || DELETE
                dataType : 'json', // data type
                data : rd_request, // post data || get data
                contentType: "application/json; charset=utf-8",
                async: true,
                success : function(result) {
                    deferredPromise.resolve(200, "")
                },
                error: function(xhr, resp, text) {
                    deferredPromise.resolve(xhr.status, text)
                }
            });
        }
        else
        {
            console.log("Rain delay not modified - Resolving promise");
            deferredPromise.resolve(200, "");
        }

        return deferredPromise.promise();
    }

    function savedSuccessfully()
    {
        console.log("Saved successfully invoked!!");
        rain_delay_modified = false
        kill_switch_modified = false

        // disable the save button
        disableSaveButton();

        // Throw up an alert
        displayAlert("success", "Settings saved successfully!");

    }

    function saveFailed(data)
    {
        console.log("save failed!!");
        displayAlert("danger", "Failed to save settings. Please try again.");
    }

    function enableSaveButton()
    {
        $("#save_system_settings").prop('disabled', false);
    }

    function disableSaveButton()
    {
        $("#save_system_settings").prop('disabled', true);
    }
    
    


    function loadPageTemplate()
    {
        $("#content_settings").html(page_template);
    }

    function loadSystemSettings()
    {
        
        // $.when(loadConfigData(), loadPushBulletUsersData()).then(drawScreen(), drawErrorScreen())
        $.when(
            $.ajax('http://localhost:5000/service_hub/settings/kill'), 
            $.ajax('http://localhost:5000/service_hub/settings/raindelay'))
            .done(function(kill_switch_data, rain_delay_data)
            {
                kill_switch = kill_switch_data[0]["kill_switch"];
                rain_delay = rain_delay_data[0]["rain_delay"]

                drawSystemSettingsScreen(kill_switch, rain_delay);
            });
            
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
            })).then(drawNotificationSettingsScreen, drawErrorScreen);
    }


    function drawSystemSettingsScreen(kill_switch, rain_delay)
    {
        if(rain_delay == null)
        {
            rain_delay = ""
        }
        console.log("Draw system settings screen invoked!");
        
        // Update template with the real data
        temp = system_settings_template;
        temp = temp.replaceAll("#KILL_SWITCH_CHECKED#", (kill_switch == 1) ? "checked": "");
        temp = temp.replaceAll("#RAIN_DELAY#", rain_delay)
        $("#content_settings content subcontent").html(temp);

        
    }

    function drawNotificationSettingsScreen()
    {
        console.log("Draw notification screen invoked!");
        console.log(notificationConfigData);
        console.log(pushBulletUsers);

        // Update template with the real data
        temp = notification_template;
        temp = temp.replaceAll("#NOTIFY_ON_WATERING_START_CHECKED#", (notificationConfigData["notify_on_watering_start"] == true) ? "checked": "");
        temp = temp.replaceAll("#NOTIFY_ON_WATERING_STOP_CHECKED#", (notificationConfigData["notify_on_watering_stop"] == true) ? "checked": "");
        temp = temp.replaceAll("#NOTIFY_ON_ERROR_CHECKED#", (notificationConfigData["notify_on_error"] == true) ? "checked": "");
        $("#content_settings content subcontent").html(temp);

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

        $.post("/service_hub/settings/notification/pushbullet/user", jsonData, 
        function(data){displayAlert("success", "User successfully added!"); loadPushNotificationSettings();});
        
    }
    function deletePushBulletUser(name)
    {
        
        $.ajax({
            url: 'http://localhost:5000/service_hub/settings/notification/pushbullet/user/' + name, // url where to submit the request
            type : "DELETE", // type of action POST || GET || DELETE
            dataType : 'json', // data type
            // data : jsonData, // post data || get data
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                console.log(result);
                loadPushNotificationSettings();
                displayAlert("success", "User successfully deleted!");
                
            },
            error: function(xhr, resp, text) {
                console.log(text);
                displayAlert("danger", "Failed to delete user. Please try again.");
            }
        });
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
                
                displayAlert("success", "Notification preferences saved!")
            },
            error: function(xhr, resp, text) {
                console.log(text);

                displayAlert("danger", "Failed to save notifications. Please try again.")
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