# Weibo API研究 #

## 版本 ##

当前Weibo API的版本是V2，地址参照：

>http://open.weibo.com/wiki/API%E6%96%87%E6%A1%A3_V2

## SDK ##

Weibo的python sdk在下面网址可以找到：

>http://open.weibo.com/wiki/SDK#Python_SDK

##### SDK使用方法 ###

Weibo采用OAuth认证，需要首先进行认证后，获取到access_token，才能使用api进行数据获取。例如要获取用户的基本信息，api接口是：

>http://open.weibo.com/wiki/2/users/show

代码的调用方式如下：

	client = APIClient(app_key=weibo_appid, app_secret=weibo_app_secret, redirect_uri=redirect_url_weibo)
	r = client.request_access_token(code)
	client.set_access_token(access_token, expires_in)
	weibo_user = client.get.users__show(uid=r.uid)

其中，users__show(uid=r.uid)为users/show接口的调用方法，返回的结果weibo_user是接口说明页面的返回json数据的dict化，在python中可以直接使用。




**MarkdownPad** is a full-featured Markdown editor for Windows. 

## Full control over your documents ##

Want to make something **bold**? Press `Ctrl + B`.

How about *italic*? Press `Ctrl + I`.

> Write a quote with `Ctrl + Q`

No matter what you're working on, you'll have quick access to Markdown syntax with handy keyboard shortcuts and toolbar buttons.

## See your changes instantly with LivePreview ##

Don't guess if your [hyperlink syntax](http://markdownpad.com) is correct; LivePreview will show you exactly what your document looks like every time you press a key.

## Make it your own ##

Fonts, sizes, color schemes, and even the HTML stylesheets are 100% customizable so you can turn MarkdownPad into your ideal editor.