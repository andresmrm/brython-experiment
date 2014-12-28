brython-experiment
==================

Python + Flask + Brython + Websockets + Pixi = ???

Running
=======

uwsgi --py-autoreload 1 --master --http :8080 --http-websockets --wsgi server:app
