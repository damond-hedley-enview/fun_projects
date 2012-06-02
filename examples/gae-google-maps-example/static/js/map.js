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
                itemMarkers = [];
                if (obj.status && obj.status == 'success') {
                    for (var i = 0; i < obj.results.length; i++) {
                        itemMarkers.push(new MarkerMaker(new google.maps.LatLng(obj.results[i].lat, obj.results[i].lon), obj.results[i].title, ''))
                    }
                }


                var infoWindow;
                
                for(var i = 0; i < itemMarkers.length; i++) {
                    var marker1 = new google.maps.Marker({ 
                        position: itemMarkers[i].postion, 
                        map: map,
                        title: itemMarkers[i].title
                    });
                    
                    (function(marker, title) {
                        
                        google.maps.event.addListener(marker, 'click', function() {
                            if (!infoWindow) {
                                infoWindow = new google.maps.InfoWindow();
                            }
                            infoWindow.setContent(title);
                            infoWindow.open(map, marker);
                        });
                    })(marker1, itemMarkers[i].title);
                }
            }
        })
    });
})();

var MarkerMaker = function(postion, title, description) {
    this.postion = postion;
    this.title = title;
    this.description = description;
}