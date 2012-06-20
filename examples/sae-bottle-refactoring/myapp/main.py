
from bottle import run, debug

from controller import app

if __name__ == '__main__':
    debug(True)
    run(app, port=8080, reloader=True)