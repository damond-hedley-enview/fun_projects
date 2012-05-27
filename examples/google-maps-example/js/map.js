$(document).ready(function(){
  var mapDiv = $("#map")[0];
  var latlng = new google.maps.LatLng(31.196784, 121.586530); 
  var options = { 
    center: latlng, 
    zoom: 17, 
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: true
  }; 
   
  var map = new google.maps.Map(mapDiv, options); 
  var marker = new google.maps.Marker({ 
  position: new google.maps.LatLng(31.196784, 121.586530), 
  map: map,
  title: 'bibo lake'
  }); 

  var infowindow = new google.maps.InfoWindow({ 
    content:'ZTE Bibo Lake' 
  });

  google.maps.event.addListener(marker, 'click', function() { 
    infowindow.open(map, marker); 
  });


  places = [];
  places.push(new MarkerMaker(new google.maps.LatLng(31.199, 121.587), 't1', 'd1'));
  places.push(new MarkerMaker(new google.maps.LatLng(31.197, 121.587), 't2', 'd2'));
  places.push(new MarkerMaker(new google.maps.LatLng(31.196, 121.587), 't3', 'd3'));

  for(var i = 0; i < places.length; i++)
  {
      var marker1 = new google.maps.Marker({ 
        position: places[i].postion, 
        map: map,
        title: places[i].title
      });
  }
});

var MarkerMaker = function(postion, title, description) {
    this.postion = postion;
    this.title = title;
    this.description = description;
}