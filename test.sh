#!/bin/bash

export http_proxy=http://172.28.32.101:5000

curl -H "X-Router-List: http://172.28.32.101:5000,http://172.28.32.102:5000,http://172.28.32.103:5000,http://172.28.32.104:5000" \
http://httpbin.org/anything
