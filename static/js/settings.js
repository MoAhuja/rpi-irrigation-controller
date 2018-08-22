$(document).ready(function()
{
    page_template = "";
    notification_template = "";
    push_bullet_input_user_row_template = ""
    number_of_users = 0;

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
        $("#content_settings content").html(notification_template);
    }

    function addPushBulletUserInputRow()
    {
        curTemplate = push_bullet_input_user_row_template;
        curTemplate = curTemplate.replaceAll("NUMBER_HOLDER", number_of_users++);
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