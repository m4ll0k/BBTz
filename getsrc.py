#!/usr/bin/python

# github.com/m4ll0k (@m4ll0k2) 
# Bug Bounty Toolz - getSrc.py
# getsrc.py - get script tag src (extract links)


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
				),headers={
			'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
			'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Connection': 'close'
			}
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
	from_str.make_links_absolute(site)
	for i in from_str.xpath('//script'):
		if i.get('src') is not None:
			print(i.get('src'))


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
