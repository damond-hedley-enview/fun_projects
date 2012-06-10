(function() {
    function Map(map) { 
        this.map = map;
        this.markers = new Array();
        this.infoWindow = null;
        this.items = new Array();
    }
    
    Map.prototype.fetchNearbyItems = function () { 
        this.clearMarkers();
        this.clearInfoWindow();
        var url = this.nearbyItemsUrl();
        (function(items, url) {
            $.ajax({
                url: url,
                type: "GET",
                async:false,
                dataType: "json",

                // When the requet completed, then invokes success function.
                success: function(obj, textStatus, xhr) {
                    xhr = null;
                    if (obj.status && obj.status == 'success') {
                        for (var i = 0; i < obj.results.length; i++) {
                            items.push(obj.results[i]);
                            console.log("fetchNearbyItems, new item added");
                        }
                    }
                }
            });
        })(this.items, url);
        this.showMakers();
        this.showInfoWindow();
    }; 

    Map.prototype.showMakers = function() {
        for(var i = 0; i < this.items.length; i++) {
            var marker = new google.maps.Marker({ 
                position: new google.maps.LatLng(this.items[i].latlng.lat, this.items[i].latlng.lng), 
                map: this.map,
                title: this.items[i].title,
                icon: "/static/img/pin.png"
            });
            this.markers.push(marker);
            console.log("showMakers, new markers added");
        }
    };

    Map.prototype.clearMarkers = function () {
        for(var i = 0; i < this.markers.length; i++) {
            this.markers[i].setMap(null);
            google.maps.event.addListener(this.markers[i], 'click', function() {
            });
        }
        this.markers.length = 0;
        this.items.length = 0;
    };

    Map.prototype.clearInfoWindow = function () {
        if (this.infoWindow) {
            this.infoWindow.close();
            this.infoWindow = null;
        }
    };

    Map.prototype.showInfoWindow = function() {
        console.log(this.items.length);
        console.log(this.markers.length);
        for(var i = 0; i < this.items.length; i++) {
            (function(theMap, marker, item) {
                google.maps.event.addListener(marker, 'click', function() {
                    if (!theMap.infoWindow) {
                        theMap.infoWindow = new InfoBox(InfoBoxOption());
                    }

                    var boxText = document.createElement("div");
                    boxText.style.cssText = "margin-top: 8px; background: green; padding: 5px;";
                    boxText.innerHTML = "title: " + item.title + "<br>" + 
                                        "Position: lat(" + item.latlng.lat.toString() + "), " +
                                        "lng(" + item.latlng.lng.toString() + ")";
                    theMap.infoWindow.setContent(boxText);
                    theMap.infoWindow.open(theMap.map, marker);
                    //theMap.map.panTo(marker.getPosition());
                });
            })(this, this.markers[i], this.items[i]);
        }
    };

    Map.prototype.getBounds = function() {
        return this.map.getBounds();
    }

    Map.prototype.nearbyItemsUrl = function() {
        var bounds = this.getBounds();
        var url = "/item/nearby?type=box" + 
            "&north=" + bounds.getNorthEast().lat() +
            "&east=" + bounds.getNorthEast().lng() +
            "&south=" + bounds.getSouthWest().lat() +
            "&west=" + bounds.getSouthWest().lng();
        return url;
    }


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

        var theMap = new Map(map);

        google.maps.event.addListenerOnce(theMap.map, "idle", function() {
            console.log("idle");
            theMap.fetchNearbyItems();
        });

        google.maps.event.addListener(theMap.map, "bounds_changed", function() {
            console.log("bounds_changed");
        });

        google.maps.event.addListener(theMap.map, "zoom_changed", function() {
            console.log("zoom_changed");
            theMap.fetchNearbyItems();
        });

        google.maps.event.addListener(theMap.map, "dragstart", function() {
            console.log("dragstart");
        });

        google.maps.event.addListener(theMap.map, "dragend", function() {
            console.log("dragend");
            theMap.fetchNearbyItems();
        });

        google.maps.event.addListener(theMap.map, "click", function() {
            theMap.clearInfoWindow();
            console.log("click");
        });

        google.maps.event.addListener(theMap.map, "drag", function() {
            console.log("drag");
        });


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

