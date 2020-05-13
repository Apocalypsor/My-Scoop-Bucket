import os
import json
import requests
import hashlib

workdir = os.getcwd()

def getHash(filename):
   h = hashlib.sha256()

   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)

   return h.hexdigest()

# Clash
cfwdir = workdir + os.sep + 'bucket' + os.sep + 'clash-for-windows.json'

with open(cfwdir, 'r') as f:
    manifest = json.load(f)

with requests.get('https://github.com/Fndroid/clash_for_windows_pkg/releases/download/' + manifest['version'] + '/sha256sum') as r:
    sha256sum = r.text
    cfw_hash = sha256sum.split('7z: ')[1].split('\n')[0].lower()

if cfw_hash != manifest['hash']:
    manifest['hash'] = cfw_hash

with open(cfwdir, 'w') as f:
    json.dump(manifest, f, indent=4, separators=(',', ': '))

# Netch
ndir = workdir + os.sep + 'bucket' + os.sep + 'netch.json'

with open(ndir, 'r') as f:
    manifest = json.load(f)

with requests.get('https://api.github.com/repos/NetchX/Netch/releases/latest') as r:
    n = r.json()
    tag = n['tag_name']
    url = n['assets'][0]['browser_download_url']

if tag != manifest['version']:
    manifest['version'] = tag
    manifest['url'] = url
    tmp = 'tmp'
    with requests.get(url) as r:
        with open(tmp, 'wb') as f:
            f.write(r.content)
    n_hash = getHash(tmp)
    os.remove(tmp) 
            
    manifest['hash'] = n_hash

with open(ndir, 'w') as f:
    json.dump(manifest, f, indent=4, separators=(',', ': '))
