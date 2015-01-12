brython-experiment
==================

Python + Flask + Brython + Websockets + Phaser + Howler = ???

Test:

http://amoamo-bosque.rhcloud.com:8000

(**REALLY UNSTABLE!**)


Running
=======

	gunicorn --reload -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" -b 0.0.0.0:8080 server:app

Old Run
=======

	gunicorn --reload -k flask_sockets.worker -b 127.0.0.1:8080 server:app

	uwsgi --py-autoreload 1 --master --http :8080 --http-websockets --wsgi server:app

OpenShift
=========

OpenShift part is based on:

https://github.com/phuslu/openshift-wsgi

Edited Gunicorn to use a Websocket worker.

Install with:

	rhc app create <app-name> diy-0.1 --from-code https://github.com/andresmrm/brython-experiment.git

or

	rhc app create <app-name> diy-0.1
	cd <app-name>
	git remote add upstream -m master https://github.com/andresmrm/brython-experiment.git
	git pull -s recursive -X theirs upstream master
	git push
