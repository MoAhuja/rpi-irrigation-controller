$(document).ready(function()
{
    page_template = "";
    system_settings_template = ""
    notification_template = "";
    push_bullet_input_user_row_template = "";
    push_bullet_input_user_row_template = "";
    number_of_users = 0;
    notificationConfigData = ""
    pushBulletUsers = ""
    pin_relay_mapping_input_row_template = "";
    pin_relay_mapping_display_row_template = "";
    pin_relay_mapping_page_template = "";
    display_settings_page_template = "";
    app_update_history_page_template = ""
    commit_history_row_template = ""
    kill_switch_modified = false
    rain_delay_modified = false
    


    function getAlertContainer()
    {
        return $("alerts#settings");
    }

    $.get('/static/screens/portal/settings/include_system_settings_template.html', 
    function(data)
    {
        system_settings_template = data;
        console.log("System settings template loaded")
    });

    $.get('/static/screens/portal/settings/include_display_settings_page_template.html', 
    function(data)
    {
        display_settings_page_template = data;
        console.log("display settings page template loaded")
    });

    $.ajax({
        url: '/static/screens/portal/settings/include_app_update_page_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            app_update_history_page_template = data
            console.log("App update history page template")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/settings/include_commit_history_row_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            commit_history_row_template = data
            console.log("Commit history row template")
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
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
        url: '/static/screens/portal/settings/include_pushbullet_display_user_row_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            push_bullet_display_user_row_template = data
            console.log("Push Bullet Display user template")
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    // Template for a pin / relay row
    $.ajax({
        url: '/static/screens/portal/settings/include_pin_relay_mapping_input_row_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            pin_relay_mapping_input_row_template = data;
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/settings/include_pin_relay_mapping_display_row_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            pin_relay_mapping_display_row_template = data;
            
        },
        error: function(xhr, resp, text) {
            console.log(text);
        }
    });

    $.ajax({
        url: '/static/screens/portal/settings/include_pin_relay_mapping_page_template.html', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'html', // data type
        async: true,
        success : function(data) {
            pin_relay_mapping_page_template = data;
            
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
        loadSystemSettings();

    });

    $('body').on('click', '#nav_system_settings', function() {
        loadSystemSettings();
    });

    // Load push notification settings when side menu option is selected
    $('body').on('click', '#nav_push_notifications', function() {
        loadPushNotificationSettings();
    });

    //Load pin relay mappings when side menu is selected
    $('body').on('click', '#nav_relay_mappings', function() {
        loadPinRelayMappings();
    });

    $('body').on('click', '#nav_updates', function() {
        loadAppUpdateHistory();
    });

    $('body').on('click', '#nav_display', function() {
        loadDisplaySettings();
    });

    $('body').on('click', '#update_app', function() {
        updateAppToLatestCommit();
    });

    // Add push bullet user
    $('body').on('click', '#add_pb_user', function() {
        addPushBulletUserInputRow();
    });

    // Save push bullet user
    $('body').on('click', '#save_pb', function() {
        savePushBulletSettings();
        // TODO: WHy is there no function for this????
    });  
    
    // Add Relay Mapping
    $('body').on('click', '#add_pin_mapping', function() {
        addPinRelayInputRow();
    });
    
    $('body').on('change', "#theme_selector", function() {
        var selectedTheme = $(this).children("option:selected").val();
        // alert("You have selected the theme - " + selectedTheme);
        var urlOfThemeFile = "/static/css/colours/" + selectedTheme;
        $("#theme-colour").attr('href', urlOfThemeFile)
    })
    

    // Save notification settings button click
    $('body').on('click', '#save_notification_settings', function() {
        saveNotificationSettings();
    });

    $('body').on('click', '.del_pb_user_button', function() {
        // Get the name of the user
        
        // name = $(this).parent().find("#name").val();
        id = $(this).attr('id');
        name = id.substring(id.lastIndexOf("_") + 1);

        
        deletePushBulletUser(name);
       
    });

    $('body').on('click', '.del_pin_mapping_button', function() {
        // Get the relay for this row
        //console.log($(this).parent());

        // relay = $(this).parent().parent().find("#relay").text();
        id = $(this).attr('id');
        relay = id.substring(id.lastIndexOf("_") + 1);

        deleteRelayPinMapping(relay);

        
    });

    // Save pin mapping
    $('body').on('click', '#save_pin_mapping', function() {
        // Get the relay for this row
        //console.log($(this).parent());

        relay = $(this).parent().prev().prev().val();
        pin = $(this).parent().prev().val();

        // Add the pin mapping
        addPinMapping(pin, relay);
    });

    function addPinMapping(pin, relay)
    {
        jsonData = `{"pin": ${pin}, "relay": ${relay}}`

        $.post("/service_hub/relay", jsonData, 
        function(data){
            loadPinRelayMappingsWithAlert("success", "Relay mapping added successfully"); 
        });
        
    }
    

    $('body').on('click', '#save_pb_user', function() {
        // Get the name of the user
        name = $(this).parent().prev().prev().val();
        key = $(this).parent().prev().val();
        
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
                    displayAlertInContainerFromXHR(getAlertContainer(), "danger", a1[1]);
                }

                if(a2[0] != 200)
                {
                    displayAlertInContainerFromXHR(getAlertContainer(), "danger", a2[1]);
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
                url: getHost() + '/service_hub/settings/kill', // url where to submit the request
                type : "POST", // type of action POST || GET || DELETE
                dataType : 'json', // data type
                data : ks_request, // post data || get data
                contentType: "application/json; charset=utf-8",
                async: true,
                success : function(result) {
                    deferredPromise.resolve(200, "")
                },
                error: function(xhr, resp, text) {
                    deferredPromise.resolve(xhr.status, xhr)
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
                url: getHost() + '/service_hub/settings/raindelay', // url where to submit the request
                type : "POST", // type of action POST || GET || DELETE
                dataType : 'json', // data type
                data : rd_request, // post data || get data
                contentType: "application/json; charset=utf-8",
                async: true,
                success : function(result) {
                    deferredPromise.resolve(200, "")
                },
                error: function(xhr, resp, text) {
                    deferredPromise.resolve(xhr.status, xhr)
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
        displayAlertInContainer(getAlertContainer(), "success", "Settings saved successfully!");

    }

    // function saveFailed(data)
    // {
    //     console.log("save failed!!");
    //     displayAlertInContainer(getAlertContainer(), "danger", "Failed to save settings. Please try again.");
    // }

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
            $.ajax(getHost() + '/service_hub/settings/kill'), 
            $.ajax(getHost() + '/service_hub/settings/raindelay'))
            .done(function(kill_switch_data, rain_delay_data)
            {
                kill_switch = kill_switch_data[0]["kill_switch"];
                rain_delay = rain_delay_data[0]["rain_delay"]

                drawSystemSettingsScreen(kill_switch, rain_delay);
            });
            
    }

    function loadPushNotificationSettings(alertType, alertContent)
    {
        notificationConfigData = ""
        step = 0
        var alertTypeResolve = $.Deferred();
        var alertContentResolve = $.Deferred();

        // $.when(loadConfigData(), loadPushBulletUsersData()).then(drawScreen(), drawErrorScreen())
        $.when(
            $.get(getHost() + '/service_hub/settings/notification/config', function(data){
                console.log("Loaded config data: " + data);
                notificationConfigData = data;

            }), $.get(getHost() + '/service_hub/settings/notification/pushbullet/users', function(data){
                console.log("Loaded user data: " + data);
                pushBulletUsers = data;
            }),
            alertTypeResolve,
            alertContentResolve)
        .done(function(configData, pbUsers, alertType, alertContent)
        {
            drawNotificationSettingsScreen();
            displayAlertInContainer(getAlertContainer(), alertType, alertContent);
        });
        
        // drawErrorScreen
        
        alertTypeResolve.resolve(alertType);
        alertContentResolve.resolve(alertContent);
    }


    function loadDisplaySettings()
    {
        loadDisplaySettingsWithAlert(null, null)
    }
    

    function loadDisplaySettingsWithAlert(alertType, alertContent)
    {
        
        // Load the subcontent
        $("#content_settings content subcontent").html(display_settings_page_template);
        

        var currentThemeURL = $("#theme-colour").attr('href');

        var lastslash = currentThemeURL.lastIndexOf("/");
        currentTheme = currentThemeURL.substring(lastslash+1);

        // Select the option matches the current theme
        $("#theme_selector").val(currentTheme)
        
        
        displayAlertInContainer(getAlertContainer(), alertType, alertContent);
         
    }
    

    function loadAppUpdateHistory()
    {
        loadAppUpdateHistoryWithAlert(null, null)
    }

    function updateAppToLatestCommit()
    {
        $.when($.ajax(getHost() + '/service_hub/updater/update'))
        .done(function(response)
        {
            loadAppUpdateHistoryWithAlert("success", "Application updated successfully!");
        })
    }

    function loadAppUpdateHistoryWithAlert(alertType, alertContent)
    {

        // Load the subcontent
        $("#content_settings content subcontent").html(app_update_history_page_template);
        $("#update_app").hide();

        // Get the Git History
        $.when($.ajax(getHost() + '/service_hub/updater/history'))
        .done(function(commit_history)
        {
            //Hide the loading message
            $("#commit_loading_message").hide();

            // disable the update button if we'er already at the latest commit
            if(commit_history.local_commit != commit_history.latest_commit)
            {
                $("#update_app").show();
            }

            commit_history.remote_commits.forEach(
                function(item, index)
                {
                    curTemplate = commit_history_row_template;
                
                    curTemplate = curTemplate.replaceAll("#DATE#", serverTimeToCommonDateTime(item.DATE));
                    // curTemplate = curTemplate.replaceAll("#HASH#", item.HASH);
                    curTemplate = curTemplate.replaceAll("#MESSAGE#", item.MESSAGE);

                    //TODO: Add a class to each one if it's the selected commmit
                    curTemplate = curTemplate.replaceAll("#IS_CURRENT_HIDDEN#", (item.HASH == commit_history.local_commit)? "" : "hidden");
                    curTemplate = curTemplate.replaceAll("#IS_LATEST_HIDDEN#", (item.HASH == commit_history.latest_commit)? "" : "hidden");

                    $("commit_history").append(curTemplate);
                });

            if((alertType != null) & (alertContent != null))
            {
                
                displayAlertInContainer(getAlertContainer(), alertType, alertContent);
            }
            
        });
    }

    function loadPinRelayMappings()
    {
        loadPinRelayMappingsWithAlert(null, null)
    }

    function loadPinRelayMappingsWithAlert(alertType, alertContent)
    {
        
        $.when($.ajax(getHost() + '/service_hub/relays'))
        .done(function(relay_mappings)
        {
            
            // Draw the screen
            $("#content_settings content subcontent").html(pin_relay_mapping_page_template);

            // TODO: For each for the relay mappings to the drawPinRelayMappingsRows functon
            relay_mappings.relays.forEach(
                function(item, index)
                {
                    curTemplate = pin_relay_mapping_display_row_template;
                    curTemplate = curTemplate.replaceAll("NUMBER_HOLDER", number_of_users++);
                    curTemplate = curTemplate.replaceAll("#RELAY#", item.relay);
                    curTemplate = curTemplate.replaceAll("#PIN#", item.pin);
                    $("#pin_mappings_section").append(curTemplate);
                });

            if((alertType != null) & (alertContent != null))
            {
                var x = $("alerts#settings");

                displayAlertInContainer(getAlertContainer(), alertType, alertContent);
            }
            
        });
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
        pushBulletUsers["users"].forEach(addPushBulletDisplayRow);
        
    }

    function drawErrorScreen()
    {
        console.log("ERROR SCREEN")
    }


    function addPinRelayInputRow()
    {

        curTemplate = pin_relay_mapping_input_row_template;
        curTemplate = curTemplate.replaceAll("NUMBER_HOLDER", number_of_users++);
        curTemplate = curTemplate.replaceAll("#RELAY#", "");
        curTemplate = curTemplate.replaceAll("#PIN#", "");
        curTemplate = curTemplate.replaceAll("#PLACEHOLDER_FOR_BUTTON#", "<button id='save_pin_mapping'>Save</button>");
        $("#pin_mappings_section").append(curTemplate);
    }

    function deleteRelayPinMapping(relay)
    {
        
        $.ajax({
            url: getHost() + '/service_hub/relays/' + relay, // url where to submit the request
            type : "DELETE", // type of action POST || GET || DELETE
            dataType : 'json', // data type
            // data : jsonData, // post data || get data
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                console.log(result);
                loadPinRelayMappingsWithAlert("success", "Relay Mapping successfully deleted!");
                
                
            },
            error: function(xhr, resp, text) {
                console.log(text);
                displayAlertInContainer(getAlertContainer(), "danger", "Failed to delete user. Please try again.");
            }
        });
    }

    function addPushBulletUserInputRow()
    {
        curTemplate = push_bullet_input_user_row_template;
        // curTemplate = curTemplate.replaceAll("NUMBER_HOLDER", number_of_users++);
        curTemplate = curTemplate.replaceAll("#NAME#", "");
        curTemplate = curTemplate.replaceAll("#API_KEY#", "");
        // curTemplate = curTemplate.replaceAll("#PLACEHOLDER_FOR_BUTTON#", "<button id='save_pb_user'>Save</button>");
        $("#push_bullet_user_grid").append(curTemplate);
    }

    function addPushBulletDisplayRow(item, index)
    {
        name = item["name"];
        apikey = item["api_key"];

        curTemplate = push_bullet_display_user_row_template;
        curTemplate = curTemplate.replaceAll("NUMBER_HOLDER", number_of_users++);
        curTemplate = curTemplate.replaceAll("#NAME#", name);
        curTemplate = curTemplate.replaceAll("#API_KEY#", apikey);
       
        $("#push_bullet_user_grid").append(curTemplate);
    }

    function addPushBulletUser(name, key)
    {
        jsonData = `{"name": "${name}", "api_key": "${key}"}`

        $.post("/service_hub/settings/notification/pushbullet/user", jsonData, 
            function(data)
            {
                loadPushNotificationSettings("success", "User successfully added!");
            }
        );
       
        
    }
    function deletePushBulletUser(name)
    {
        
        $.ajax({
            url: getHost() + '/service_hub/settings/notification/pushbullet/user/' + name, // url where to submit the request
            type : "DELETE", // type of action POST || GET || DELETE
            dataType : 'json', // data type
            // data : jsonData, // post data || get data
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                console.log(result);
                loadPushNotificationSettings("success", "User successfully deleted!");
                
            },
            error: function(xhr, resp, text) {
                console.log(text);
                displayAlertInContainerFromXHR(getAlertContainer(), "danger", xhr);
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
            url: getHost() + '/service_hub/settings/notification/config', // url where to submit the request
            type : "POST", // type of action POST || GET
            dataType : 'json', // data type
            data : jsonData, // post data || get data
            success : function(result) {
                // you can see the result from the console
                // tab of the developer tools
                console.log(result);
                
                displayAlertInContainer(getAlertContainer(), "success", "Notification preferences saved!")
            },
            error: function(xhr, resp, text) {
                console.log(text);

                displayAlertInContainer(getAlertContainer(), "danger", "Failed to save notifications. Please try again.")
            }
        });
    }


});