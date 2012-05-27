from bottle import run, route, default_app
import bottle


@route('/')
def hello():
    return "Hello, from bottle-gae."

@route('/login')
def hello():
    return "input your username and password."


bottle.debug(True)
app = default_app()
