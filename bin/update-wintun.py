import os
import re
import requests
import hashlib

workdir = os.getcwd()

def getHash(file):
    h = hashlib.sha256()
    h.update(file)

    return h.hexdigest()

wintundir = workdir + os.sep + "files" + os.sep + "Wintun.zip"
with open(wintundir, "rb") as f:
    data = f.read()
    local_hash = getHash(data)

wintun_web = requests.get("https://www.wintun.net/").text
wintun_urls = re.search(r"href=\"builds/wintun-[\w\.]+\.zip\"", wintun_web).group(0)
wintun_url = "https://www.wintun.net/" + wintun_urls.lstrip("href=\"").rstrip("\"")

with requests.get(wintun_url) as r:
    wintun_hash = getHash(r.content)
    if local_hash != wintun_hash:
        print("Updating Wintun ...")
        with open(wintundir, "wb") as f:
            f.write(r.content)
    else:
        print("Wintun up-to-date!")
