<!DOCTYPE html>
<html lang="en">
<head>
        <meta property="qc:admins" content="35315630321105631611006375" />
	<meta charset="utf-8">
	<title>mainpage</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="">
	<meta name="author" content="">

	<!== Le styles -->
  <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.css">
	<style type="text/css">
		body {
			padding-top: 60px;
			padding-bottom: 40px;
		}
	</style>
  <link rel="stylesheet" type="text/css" href="/static/css/bootstrap-responsive.css">
</head>

<body>
  
  <ul>
      {% for weiboInfo in weiboDict %}
      <li>
        <ul>
          {% for weibo in weiboInfo %}
            {% if weibo == 'user' %}
              <ul>
                {% for userInfo in weiboInfo[weibo] %}
                <li>{{userInfo}}:::::::{{weiboInfo[weibo][userInfo]}}</li>
                {% endfor %}
              </ul>
            {% else %}
              <li>{{weibo}}::{{weiboInfo[weibo]}}</li>
            {% endif %}
          {% endfor %}
        </ul>
      </li>
      {% endfor %}
  </ul>

<!--
  <ul>
  {% for weibo in weiboDict %}
        {% if weibo == 'user' %}
          <ul>
          {% for userinfo in weiboDict[weibo] %}
            <li>{{userinfo}}:::::{{weiboDict[weibo][userinfo]}}</li>
          {% endfor %}
        {% else %}
          <li>{{weibo}}::{{weiboDict[weibo]}}</li>
        {% endif %}
  {% endfor %}
  </ul>
  
-->
  <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/js/jquery-1.7.2.js"></script>
    <script src="/static/js/bootstrap-transition.js"></script>
    <script src="/static/js/bootstrap-alert.js"></script>
    <script src="/static/js/bootstrap-modal.js"></script>
    <script src="/static/js/bootstrap-dropdown.js"></script>
    <script src="/static/js/bootstrap-scrollspy.js"></script>
    <script src="/static/js/bootstrap-tab.js"></script>
    <script src="/static/js/bootstrap-tooltip.js"></script>
    <script src="/static/js/bootstrap-popover.js"></script>
    <script src="/static/js/bootstrap-button.js"></script>
    <script src="/static/js/bootstrap-collapse.js"></script>
    <script src="/static/js/bootstrap-carousel.js"></script>
    <script src="/static/js/bootstrap-typeahead.js"></script>

</body>

</html>