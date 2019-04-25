function loadRelayDropdownIntoTemplate(templateAsDOM, currentZone)
{
    
    $.when($.ajax('http://127.0.0.1:5000/service_hub/relays'))
        .done(function(relay_mappings)
        {
            if (currentZone == null)
            {
                currentZone = -1;
            }

            // find the select tag
            selectElement = templateAsDOM.find('select');

            // Loop through all the relays in the json response
            for(i = 0; i < relay_mappings.relays.length; i++)
            {
                relay_data = relay_mappings.relays[i];

                // Extract values
                var value = relay_data.relay;
                var text = value;
                
                // Check if the zone provided is mapped to the relay baying interrogated
                var selectedDD = false
                if(relay_data.zone == currentZone)
                {
                    text = text + " [Mapped to this zone]"
                    selectedDD = true
                }
                else if(relay_data.zone == null)
                {
                    text = text + " [Not mapped to any zone]";
                }
                else
                {
                    text = text + " [Already Mapped!]";
                }
                
                var option = new Option(text, value, selectedDD); 

                selectElement.append($(option));

            }
        });

}