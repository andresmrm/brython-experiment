#!/usr/bin/env python
# coding:utf-8

import sys
import os
import logging
import shlex
import gunicorn.app.wsgiapp

host = os.environ.get('OPENSHIFT_DIY_IP', '127.0.0.1')
port = os.environ.get('OPENSHIFT_DIY_PORT', '8080')

# cmd = 'gunicorn -b %s:%d -w 2 -k gevent app:application' % (host, int(port))
cmd = 'gunicorn -b %s:%d -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" server:app' % (host, int(port))
sys.argv = shlex.split(cmd)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
os.chdir(os.path.abspath(os.path.dirname(__file__)))
gunicorn.app.wsgiapp.run()

