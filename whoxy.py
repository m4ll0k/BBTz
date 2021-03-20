#!/usr/bin/python

# github.com/m4ll0k (@m4ll0k2) 
# Bug Bounty Toolz - whoxy.py
# whoxy.py - Whoxy Reverse Whois 


import sys
import requests
import json


API_KEY = ""

if API_KEY is "":
	sys.exit(print('Please set whoxy api_key!!'))

def getWhoxyContent(keyword):
	try:
		req = requests.get(
			'http://api.whoxy.com/?key={API_KEY}&reverse=whois&name={keyword}&mode=mini'.format(
				keyword = keyword,API_KEY = API_KEY
				)
			)
		return json.loads(req.content.decode('utf-8'))
	except Exception as _except:
		print('[ + ] %s'%str(_except))

def __usage__(_=True):
	print('\nUsage:\n')
	print('\tpython3 %s <keyword_1;keyword_2;..>'%(sys.argv[0]))
	print('\tcat keywords.txt | python3 %s'%sys.argv[0])
	if _:
		sys.exit(0)

def __main__(keyword):
	jsoned = getWhoxyContent(keyword)
	if jsoned.get('search_result'):
		for i in range(len(jsoned.get('search_result'))):
			domain = jsoned.get('search_result')[i]['domain_name']
			print(domain)

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
