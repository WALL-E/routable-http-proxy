#!/bin/bash

set -x
set -e

sudo yum install -y git
sudo yum install -y python-setuptools.noarch
sudo yum install -y gcc gcc-c++ python-devel

sudo pip3 install gunicorn
sudo pip3 install gevent
sudo pip3 install flask
sudo pip3 install requests

gunicorn -v
python3 -c "import flask"
python3 -c "import requests"
