from route import app


import sae

application = sae.create_wsgi_app(app)