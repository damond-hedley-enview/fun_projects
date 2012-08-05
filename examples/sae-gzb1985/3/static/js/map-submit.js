(function() {
    $(document).ready(function() {
        var mapDiv = $("#map")[0];
        var latlng = new google.maps.LatLng(31.196784, 121.586530); 
        var options = { 
            center: latlng, 
            zoom: 11, 
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            disableDefaultUI: true
        }; 
        var map = new google.maps.Map(mapDiv, options);

        var marker = new google.maps.Marker({ 
            position: new google.maps.LatLng(31.196784, 121.586530), 
            title: "dragtest",
            icon: "/static/img/pin.png"
        });

        marker.setMap(map);
        marker.setDraggable (true);

        google.maps.event.addListener(marker, 'click', function() {
        });

        google.maps.event.addListener(marker, 'dragend', function() {
            var point = marker.getPosition();
            console.log(point.lat());
            console.log(point.lng());
        });

        

        var addressInput = $("#address")[0];
        var address = "";
        var theTimer;
        
        
        addressInput.addEventListener("input",addressChange,false); 
        function addressChange() {
            //console.log(addressInput.value);
        }

        var geocoder;
        geocoder = new google.maps.Geocoder();

        function codeAddress() { 
            var sAddress = addressInput.value;
            console.log("codeAddress: " + sAddress);
            if (sAddress=="" || sAddress == address) {
                theTimer = setTimeout(codeAddress, 500);
                return;
            }
            address = sAddress;
            console.log(address);
            geocoder.geocode( { 'address': sAddress}, function(results, status) { 
                if (status == google.maps.GeocoderStatus.OK) {
                    marker.setPosition(results[0].geometry.location);
                    map.panTo(results[0].geometry.location);
                    theTimer = setTimeout(codeAddress, 500);
                    console.log("geocode suc");
                }
                else {
                    theTimer = setTimeout(codeAddress, 1000);
                    console.log("geocode fail");
                }
            });
        }

        theTimer = setTimeout(codeAddress, 500);



    });
})();

