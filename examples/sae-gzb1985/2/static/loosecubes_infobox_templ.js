
mapView: function() {
            var a = null, b = null, f = [], k = null, b = null, m = null, 
            n = Hogan.compile([
                '<div class="info_box">', 
                    '<div class="close"></div>', 
                    '<div class="arrow"></div>', 
                    '<div class="price">FREE</div>', 
                    '<div class="top_section">', 
                        '<div class="listing_info">', 
                            '<div class="photo_book">', 
                                '<a href="/workspaces/{{slug}}">', 
                                    '<div class="photo">', 
                                        '<img src="{{image_url}}" />', 
                                    "</div>", 
                                "</a>", 
                            "</div>", 
                            '<div class="info">', 
                                '<a href="/workspaces/{{slug}}">{{name}}</a>', 
                                "<p>{{location_text}}</p>", 
                                "<p><span>Industry:</span> {{industry}}</p>", 
                                "<p><span>Vibe:</span> {{vibe}}</p>", 
                                '<p class="ratings" data-rating="{{rating}}"></p>', 
                            '<div class="host">'
                                '<div class="photo">'
                                    '<div class="banner">'
                                    '</div>'
                                    '<a href="/m/{{host.id}}">'
                                        '<img alt="{{host.name}}" src="{{host.avatar_url}}" />'
                                    '</a>'
                                '</div>'
                            '</div>', 
                        "</div>", 
                    "</div>", 


                '<form accept-charset="UTF-8" action="/workspaces/{{slug}}/instant_bookings" data-forbidden-weekdays="{{forbidden_weekdays}}" class="new_reservation" id="new_reservation" method="post">', 
                '<div style="margin:0;padding:0;display:inline">', 
                '<input name="utf8" type="hidden" value="✓">', 
                '<input name="authenticity_token" type="hidden" value="{{auth_token}}">', 
                "</div>", 
                '<label for="reservation_start_date">Date:</label>', 
                '<input id="reservation_start_date" name="reservation[start_date]" size="30" tabindex="0" value="{{start_date}}" class="date">', 
                '<input id="book" name="commit" type="submit" value="Book" />', 
                "{{#next_available_date}}", 
                '<span class="next_available_date">{{next_available_date}}</span>', 
                "{{/next_available_date}}", 
                '<div class="validate cloak"></div>', 
                "</form>", 
                '<p class="cubes_available cloak">Spaces left: <span class="cubes_available_units_for_date">0</span></p>', 
                "</div>", 
                "</div>"].join("")), o = Hogan.compile(['<ul class="endorsements">', "<h2>{{{mutual_friends_text}}}</h2>", "{{#mutual_friends}}", '<li><a title="{{friendship.name}}" href={{friendship.profile_url}}"><img alt="{{friendship.name}}" src="{{friendship.photo_url}}" /></a></li>', "{{/mutual_friends}}", "</ul>"].join(""));

