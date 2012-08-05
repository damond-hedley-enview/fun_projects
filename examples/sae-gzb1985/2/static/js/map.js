(function() {
    function Map(map) { 
        this.map = map;
        this.markers = new Array();
        this.infoWindow = null;
        this.items = new Array();
        this.info_box_text =   
                        "<div class=\"info_box\">" +
                            "<div class=\"custom_close\"></div>" +
                            '<div class="arrow"></div>' + 
                            '<div class="top_section">' +
                                '<div class="listing_info">' +
                                    '<div class="photo_book">' +
                                        '<a href="#">' +
                                            '<div class="photo">' +
                                                '<img src="/static/img/iphone.png" alt=\"\"/>' +
                                            "</div>" +
                                        "</a>" +
                                    "</div>" +
                                    '<div class="info">' +
                                        "<a src=\"#\">{{title}}</a>" + 
                                        "<p><span>User: </span>{{user.name}}</p>" + 
                                        "<p><span>Price: </span>{{price}}</p>" + 
                                        "<p><span>Desc: </span>{{desc}}</p>" + 
                                        "<p><span>Postion: </span>({{latlng.lat}}, {{latlng.lng}})</p>" + 
                                    "</div>" + 
                                "</div>" + 
                            "</div>" +
                        "</div>";
        this.info_box_templ = Hogan.compile(this.info_box_text);

        this.li_text =  '<li id="{{id}}" class="available-{{available}}">' + 
                            '<div class="full_overlay"></div>' + 
                            '<article class="listing">' +
                                '<div class="photo">' +
                                    '<img src="/static/img/iphone.png" />' + 
                                "</div>" +
                                '<div class="info">' +
                                    "<h1>{{title}}</h1>" +
                                    "<p><span>User: </span>{{user.name}}</p>" + 
                                    "<p><span>Price: </span>{{price}}</p>" + 
                                    "<p><span>Desc: </span>{{desc}}</p>" + 
                                "</div>" +
                            "</article>" + 
                            '<div class="unavailable">{{next_available_date}}</div>' +  
                        "</li>";
        this.li_text_templ = Hogan.compile(this.li_text);
    }

    Map.prototype.fetchNearbyItems = function () { 
        var url = this.nearbyItemsUrl();
        $.ajax({
            url: url,
            type: "GET",
            dataType: "json",
            context: this,
            success: this.fetchCallback
        });
    }; 

    Map.prototype.fetchCallback = function(obj, textStatus, xhr) {
        xhr = null;
        if (obj.status && obj.status == 'success') {
            if (obj.results.length > 0) {
                this.clearMarkers();
                this.clearInfoWindow();
                this.clearItems();
            }
            for (var i = 0; i < obj.results.length; i++) {
                this.items.push(obj.results[i]);
                console.log("fetchNearbyItems, new item added");
            }
            this.showMakers();
            this.showInfoWindow();
            this.showItems();
        }
    };

    Map.prototype.showMakers = function() {
        for(var i = 0; i < this.items.length; i++) {
            var marker = new google.maps.Marker({ 
                position: new google.maps.LatLng(this.items[i].latlng.lat, this.items[i].latlng.lng), 
                map: this.map,
                title: this.items[i].title,
                icon: "/static/img/pin.png"
            });
            marker.setDraggable(true);
            this.markers.push(marker);
            console.log("showMakers, new markers added");
        }
    };

    Map.prototype.showItems = function() {
        for(var i = 0; i < this.items.length; i++) {
            this.items[i]['id'] = i;
            itemlist.append(this.li_text_templ.render(this.items[i]));
        }
        (function (theMap) {
            itemlist.delegate("li", "click", function(event) {
                event.stopPropagation();
                var item = $(this);//'this' is a 'li'
                id = item.attr("id");
                marker = theMap.markers[id];
                google.maps.event.trigger(marker, "click");
            });

            itemlist.delegate("li", "mouseover", function() {
                var item = $(this);
                id = item.attr("id");
                marker = theMap.markers[id];
                item.addClass("hover");
                //marker.setIcon();
            });

            itemlist.delegate("li", "mouseout", function() {
                var item = $(this);
                id = item.attr("id");
                marker = theMap.markers[id];
                item.removeClass("hover");
                //marker.setIcon();
            });
        })(this);//'this' is the Map object
        
        itemlist.fadeIn(500);
    };

    Map.prototype.clearItems = function () {
        itemlist = $('#list_view').find("ul");
        itemlist.html("");
        itemlist.hide();
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
        for(var i = 0; i < this.items.length; i++) {
            (function(theMap, marker, item, templ) {
                google.maps.event.addListener(marker, 'click', function() {
                    if (!theMap.infoWindow) {
                        theMap.infoWindow = new InfoBox(InfoBoxOption());
                    }
                    theMap.infoWindow.setContent(templ.render(item));
                    theMap.infoWindow.open(theMap.map, marker);

                    google.maps.event.addListener(theMap.infoWindow, 'domready', function() {
                        (function(theMap){
                            $('.info_box .custom_close').click(function(event) {
                                theMap.infoWindow.close();
                            });
                        })(theMap);
                    });
                });
                
            })(this, this.markers[i], this.items[i], this.info_box_templ);
        }
    };

    Map.prototype.getBounds = function() {
        return this.map.getBounds();
    };

    Map.prototype.nearbyItemsUrl = function() {
        var bounds = this.getBounds();
        var url = "/item/nearby?type=box" + 
            "&north=" + bounds.getNorthEast().lat() +
            "&east=" + bounds.getNorthEast().lng() +
            "&south=" + bounds.getSouthWest().lat() +
            "&west=" + bounds.getSouthWest().lng();
        return url;
    };

    $(document).ready(function() {
        var mapCenter = new google.maps.LatLng(31.196784, 121.586530); 
        var options = { 
            center: mapCenter, 
            zoom: 11, 
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            disableDefaultUI: true
        }; 
        var map = new google.maps.Map($("#map")[0], options);
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
            theMap.clearInfoWindow();
            console.log("drag");
        });

        //not effected
        google.maps.event.addListener(theMap.map, "domready", function() {
            (function(theMap){
                $('.info_box .custom_close').click(function(event) {
                    theMap.clearInfoWindow();
                });
            })(theMap);
        });

        //set the height and width of itemlist view and map view
        (function() {
            window.onresize = arguments.callee;
            var navbarHeight = 40;//height of top navbar
            h = $(window).height() - navbarHeight;
            w = $(window).width() - $("#list_view").outerWidth();
            $('#map').height(h);
            $('#map').width(w);
            $('#list_view').height(h);
        })();
        

    });
})();

function InfoBoxOption() {
    var myOptions = {
        disableAutoPan: false
        ,maxWidth: 0
        ,pixelOffset: new google.maps.Size(-143, -270)
        ,zIndex: null
        ,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
        ,infoBoxClearance: new google.maps.Size(1, 1)
        ,isHidden: false
        ,pane: "floatPane"
        ,enableEventPropagation: false
    };
    return myOptions;
}

