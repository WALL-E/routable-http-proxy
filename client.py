#!/usr/local/bin/python3.6


from sdk import request

headers = {
    "X-Router-List": "http://172.28.32.100:5000,http://172.28.32.101:5000,http://172.28.32.102:5000,http://172.28.32.103:5000,http://172.28.32.104:5000"
}

response = request.proxy(url="http://httpbin.org/anything", method="get", headers=headers)

print(response.text)
