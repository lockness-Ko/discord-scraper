#!/usr/bin/env python3

# Literally grabs the urls from the scraped messages

import json
import requests
import time

with open("scraped.json") as data_file:
    data_raw = data_file.read()

    data_json = json.loads(data_raw)

    urls = []

    for element in data_json:
        try:
            for i in [x["url"] for x in element["attachments"]]:
                if "mp4" not in i:
                    urls.append(i)
        except:
            pass

    urls = list(dict.fromkeys(urls))

    print(len(urls))

    for url in urls:
        f = url.split("/")[-1]

        print(f"[*] Grabbing {f}")

        resp = requests.get(url)

        open("images/"+f, "wb").write(resp.content)
        time.sleep(1)
