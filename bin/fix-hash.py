import os
import json
import requests
import hashlib

workdir = os.getcwd()


def getHash(file):
    h = hashlib.sha256()
    h.update(file)

    return h.hexdigest()


# Clash
cfwdir = workdir + os.sep + "bucket" + os.sep + "clash-for-windows.json"

with open(cfwdir, "r") as f:
    manifest = json.load(f)

with requests.get(manifest["architecture"]["64bit"]["url"].replace("#/dl.7z", "")) as r:
    cfw64_hash = getHash(r.content)

with requests.get(manifest["architecture"]["32bit"]["url"].replace("#/dl.7z", "")) as r:
    cfw32_hash = getHash(r.content)

if (
    cfw64_hash != manifest["architecture"]["64bit"]["hash"]
    or cfw32_hash != manifest["architecture"]["32bit"]["hash"]
):
    manifest["architecture"]["64bit"]["hash"] = cfw64_hash
    manifest["architecture"]["32bit"]["hash"] = cfw32_hash

    with open(cfwdir, "w") as f:
        json.dump(manifest, f, indent=4, separators=(",", ": "))

# Netch
ndir = workdir + os.sep + "bucket" + os.sep + "netch.json"

with open(ndir, "r") as f:
    manifest = json.load(f)

with requests.get("https://api.github.com/repos/NetchX/Netch/releases/latest") as r:
    n = r.json()
    tag = n["tag_name"]
    url = n["assets"][0]["browser_download_url"]

if tag != manifest["version"]:
    manifest["version"] = tag
    manifest["url"] = url

    with requests.get(url) as r:
        n_hash = getHash(r.content)

    manifest["hash"] = n_hash

    with open(ndir, "w") as f:
        json.dump(manifest, f, indent=4, separators=(",", ": "))
