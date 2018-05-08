#!/usr/local/bin/python3.6

from contextlib import closing
import requests
from flask import Flask, request, Response

app = Flask(__name__)

HEADER_ROUTER = "X-Router-List"

@app.before_request
def before_request():
    url = request.url
    method = request.method
    data = request.data or request.form or None
    headers = dict()
    for name, value in request.headers:
        if not value or name == 'Cache-Control':
            continue
        headers[name] = value

    x_forwarded_for = headers.get("X-Forwarded-For", "").split(",")
    x_forwarded_for.append(request.remote_addr)
    headers["X-Forwarded-For"] = ", ".join([i.strip() for i in x_forwarded_for if i != ""])

    proxies = dict()
    router_list = headers.get("X-Router-List", None)
    if router_list is not None:
        routers = headers[HEADER_ROUTER].split(",")
        if len(routers) > 0:
            proxy = routers[0]
            if proxy.startswith("http"):
                proxies["http"] = proxy
            if proxy.startswith("https"):
                proxies["http"] = proxy

        if len(routers) > 1:
            headers[HEADER_ROUTER] = ",".join(routers[1:])
        else:
            headers.pop(HEADER_ROUTER, None)
    
    with closing(
        requests.request(method, url, headers=headers, data=data, stream=True, proxies=proxies)
    ) as r:
        resp_headers = []
        for name, value in r.headers.items():
            if name.lower() in ('content-length', 'connection',
                                'content-encoding'):
                continue
            resp_headers.append((name, value))
        return Response(r.text, status=r.status_code, headers=resp_headers)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
