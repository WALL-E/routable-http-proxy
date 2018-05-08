#!/usr/local/bin/python3.6

import requests
import json

HEADER_ROUTER = "X-Router-List"

def proxy(method, url, **kwargs):
    headers = kwargs.pop("headers", None) 
    proxies = kwargs.pop("proxies", None)
    if headers is not None:
        router_list = headers.get("X-Router-List", None)
        if router_list is not None:
            routers = headers[HEADER_ROUTER].split(",")
            if len(routers) > 0:
                proxies = proxies or {}
                proxy = routers[0]
            if proxy.startswith("http"):
                proxies["http"] = proxy
            if proxy.startswith("https"):
                proxies["http"] = proxy
            if len(routers) > 1:
                headers[HEADER_ROUTER] = ",".join(routers[1:])
            else:
                headers.pop(HEADER_ROUTER, None) 

    kwargs["proxies"] = proxies
    kwargs["headers"] = headers 
    return requests.request(method=method, url=url, **kwargs)


if __name__ == '__main__':
    headers_102 = {
        "X-Router-List": "http://172.28.32.101:5000,http://172.28.32.102:5000"
    }
    headers_103 = {
        "X-Router-List": "http://172.28.32.101:5000,http://172.28.32.102:5000,http://172.28.32.103:5000"
    }
    headers_104 = {
        "X-Router-List": "http://172.28.32.101:5000,http://172.28.32.102:5000,http://172.28.32.103:5000,http://172.28.32.104:5000"
    }

    response = proxy("GET", "http://httpbin.org/anything", headers=headers_102)
    assert "172.28.32.101" in response.json()["origin"]
    response = proxy("GET", "http://httpbin.org/anything", headers=headers_103)
    assert "172.28.32.102" in response.json()["origin"]
    response = proxy("GET", "http://httpbin.org/anything", headers=headers_104)
    assert "172.28.32.103" in response.json()["origin"]

    print("TESTS PASS")
