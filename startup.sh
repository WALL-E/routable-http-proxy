#!/bin/bash


/usr/local/bin/gunicorn --worker-class=gevent main:app -b 0.0.0.0:5000
