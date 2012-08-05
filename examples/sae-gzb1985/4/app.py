from bottle import route, run, debug, Bottle,default_app
from bottle import static_file, response, template, request
from bottle import jinja2_view as view


app = default_app()

@app.route('/')
@view('views/index.html')
def homepage():
    return {}

#@route('/static/img/:filename')
#def server_static(filename):
#    return static_file(filename, root='static/img')

#@route('/static/css/:filename')
#def server_static(filename):
#    return static_file(filename, root='static/css')

#@route('/static/js/:filename')
#def server_static(filename):
#    return static_file(filename, root='static/js')

debug(True)
#run(host='localhost', port=8080)
