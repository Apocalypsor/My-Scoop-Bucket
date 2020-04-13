import os,json
from urllib.request import urlopen

workdir = os.getcwd()
cfwdir = workdir + os.sep + 'bucket' + os.sep + 'clash-for-windows.json'

with open(cfwdir, 'r') as f:
	manifest = json.load(f)

with urlopen('https://github.com/Fndroid/clash_for_windows_pkg/releases/download/' + manifest['version'] + '/sha256sum') as response:
	sha256sum = response.read().decode('utf-8')
	cfw_hash = sha256sum.split('7z: ')[1].split('\n')[0].lower()

if cfw_hash != manifest['hash']:
	with open(cfwdir, 'r+') as f:
		d = f.read()
		t = d.replace(manifest['hash'], cfw_hash)
		f.seek(0, 0)
		f.write(t)


