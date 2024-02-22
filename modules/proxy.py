import os
from itertools import cycle
import requests as r

def check():
    proxies_file = os.path.join(os.path.dirname(__file__), '..', 'proxies.txt')
    if not os.path.exists(proxies_file):
        print("[!] The file 'proxies.txt' couldn't be found. Make sure the file exists before running again.")
        return None
    else:
        with open(proxies_file, "r") as f:
            proxies = [x.strip() for x in f.readlines()]
            return cycle(proxies)

proxy_pool = check()

def workingProxy():
    proxy = next(proxy_pool)
    try:
        r.get("http://ipinfo.io/json",
                proxies = {
                    "http": "http://" + proxy
                    },
                timeout = 5)
        return proxy
    except Exception as e:
        return workingProxy()
