import os,json
from urllib.request import urlopen

def fileReplace(file, old_str, new_str):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)

workdir = os.getcwd()
cfwdir = workdir + os.sep + 'bucket' + os.sep + 'clash-for-windows.json'

with open(cfwdir, 'r') as f:
	manifest = json.load(f)

with urlopen('https://github.com/Fndroid/clash_for_windows_pkg/releases/download/' + manifest['version'] + '/sha256sum') as response:
	sha256sum = response.read().decode('utf-8')
	cfw_hash = sha256sum.split('7z: ')[1].split('\n')[0].lower()

if cfw_hash != manifest['hash']:
    fileReplace(cfwdir, manifest['hash'], cfw_hash)

