#!/usr/bin/python

# github.com/m4ll0k (@m4ll0k2) 
# Bug Bounty Toolz - jefst.py
# jefst.py - json extractor from script tag


import sys
import lxml.html as html
import requests
import json
import urllib.parse as parse

def getContent(domain):
	try:
		req = requests.get(
			'{domain}'.format(
				domain = domain
				)
			)
		return req
	except Exception as _except:
		print('[ + ] %s'%str(_except))

def __usage__(_=True):
	print('\nUsage:\n')
	print('\tpython3 %s <http://www.example.com;https://www.example2.com>'%(sys.argv[0]))
	print('\tcat sites.txt | python3 %s'%sys.argv[0])
	if _:
		sys.exit(0)

def __main__(site):
	parse_ = parse.urlparse(site)
	if parse_.scheme == '':
		# print('[ ! ] Missing scheme or not supported for %s! Skip target..'%(site))
		return
	# print('[ + ] '+site)
	content = getContent(site)
	from_str = html.fromstring(content.content)
	xpath = from_str.xpath('//script[@type="application/json"]/text()')
	for i in range(len(xpath)):
		i = json.dumps(json.loads(str(xpath[i]).encode('utf-8')))
		print(i)


stdin = False
if __name__ == "__main__":
	if len(sys.argv) > 1 and len(sys.argv) < 3:
		for keyword in sys.argv[1].split(';'):
			__main__(keyword)
	else:
		for line in sys.stdin.readlines():
			stdin = True
			line = line.strip()
			if line == '\n':
				__usage__()
			__main__(line)

	if len(sys.argv) == 1 and stdin is False:
		__usage__()
