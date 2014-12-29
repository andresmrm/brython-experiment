brython-experiment
==================

Python + Flask + Brython + Websockets + Pixi = ???

Running
=======

gunicorn --reload -k flask_sockets.worker -b 127.0.0.1:8080 server:app

Old Run
=======
uwsgi --py-autoreload 1 --master --http :8080 --http-websockets --wsgi server:app
