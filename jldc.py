#!/usr/bin/python

# github.com/m4ll0k (@m4ll0k2) 
# Bug Bounty Toolz - jldc.py
# subdomain enum with jldc.me


import sys
import requests
import json


def getJldcContent(domain):
	try:
		req = requests.get(
			'https://jldc.me/anubis/subdomains/{domain}'.format(
				domain = domain
				)
			)
		return json.loads(req.content.decode('utf-8'))
	except Exception as _except:
		print('[ + ] %s'%str(_except))

def __usage__(_=True):
	print('\nUsage:\n')
	print('\tpython3 %s <domain1;domain2;..>'%(sys.argv[0]))
	print('\tcat domains.txt | python3 %s'%sys.argv[0])
	if _:
		sys.exit(0)

def __main__(keyword):
	jsoned = getJldcContent(keyword)
	for subdomain in jsoned:
		print(subdomain)

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
