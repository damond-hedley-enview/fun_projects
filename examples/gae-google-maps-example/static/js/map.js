(function() {
    $(document).ready(function(){
      var mapDiv = $("#map")[0];
      var latlng = new google.maps.LatLng(31.196784, 121.586530); 
      var options = { 
        center: latlng, 
        zoom: 11, 
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true
      }; 
       
      var map = new google.maps.Map(mapDiv, options); 

      g_currentSearchXHR = $.ajax({
            url: "/item/latest",
            type: "GET",
            dataType: "json",

            // When the requet completed, then invokes success function.
            success: function(obj, textStatus, xhr) {
                g_currentSearchXHR = null;
                items = [];
                if (obj.status && obj.status == 'success') {
                    for (var i = 0; i < obj.results.length; i++) {
                        items.push(obj.results[i]);
                    }
                }

                var markers = [];
                for(var i = 0; i < items.length; i++) {
                    var marker = new google.maps.Marker({ 
                        position: new google.maps.LatLng(items[i].latlng.lat, items[i].latlng.lng), 
                        map: map,
                        title: items[i].title,
                        icon: "/static/img/pin.png"
                    });
                    markers.push(marker);
                }

                var infoWindow;
                for(var i = 0; i < items.length; i++) {
                    (function(marker, title, latlng) {
                        
                        google.maps.event.addListener(marker, 'click', function() {
                            if (!infoWindow) {
                                infoWindow = new InfoBox(InfoBoxOption());
                            }

                            var boxText = document.createElement("div");
                            boxText.style.cssText = "margin-top: 8px; background: green; padding: 5px;";
                            boxText.innerHTML = "title: " + title + "<br>" + 
                                                "Position: lat(" + latlng.lat.toString() + "), " +
                                                "lng(" + latlng.lng.toString() + ")";
                            infoWindow.setContent(boxText);
                            infoWindow.open(map, marker);
                            map.panTo(marker.getPosition());
                        });
                    })(markers[i], items[i].title, items[i].latlng);
                }
            }
        })
    });
})();

function InfoBoxOption() {
    var myOptions = {
        disableAutoPan: false
        ,maxWidth: 0
        ,pixelOffset: new google.maps.Size(20, -50)
        ,zIndex: null
        ,boxStyle: { 
            background: "green"
            ,opacity: 1
            ,width: "280px"
            ,height: "100px"
        }
        ,closeBoxMargin: "20px 2px 2px 2px"
        //,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
        ,infoBoxClearance: new google.maps.Size(1, 1)
        ,isHidden: false
        ,pane: "floatPane"
        ,enableEventPropagation: false
    };
    return myOptions;
}

