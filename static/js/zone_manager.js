String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

$(document).ready(function(){
           
    var scheduleCounter = 0;
                    

    // Time picker hook
    $('body').on('click', '.time', function() {
        $(this).timepicker({'step': 10, 'timeFormat': 'H:i'});
    });

    // Loads the create zone content
    $("createzone").load("/static/screens/portal/create_zone_include.html");
       
    // Handles the submission of the create zone
    $('body').on('click', '#btnCreateZone', function() {
        // e.preventDefault();
        var jsonData = $("#formData").serializeJSON();
        console.log(jsonData);


        $.ajax({
            url: 'http://localhost:5000/service_hub/zone', // url where to submit the request
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
    });

    // Handles the "Add Schedule" button
    $('body').on('click', '#btnAddSchedule', function() {
        $.get("/static/screens/portal/schedule_template_include.html", function(data){
            var data2 = data.replaceAll("NUMBER_HOLDER", scheduleCounter)
            $("#schedule_area").append(data2);
            scheduleCounter++
        });
    });

    // Side menu navigation - hides zone cards, shows create zone
    $("#nav_create_zone").click(function(){
        // hide the others
        $("zonecards").hide()
        $("createzone").show()
    });

    // Side menu navigation - hides create zone, shows all zones
    $("#nav_view_zone").click(function(){
        // hide the others
        $("zonecards").show()
        $("createzone").hide()

    });

    // Handles the delete button click
    $('body').on('click', '.delButton', function() {
        var id  = $(this).attr('id');
        console.log(id);

        //If they hit delete on the schedule button, then we need to decrement the counter
        if(id == "scheduleDelButton")
        {
            scheduleCounter--;
            console.log("Schedule Counter == " + scheduleCounter);
        }

        $(this).parent().parent().remove();


    });


});
