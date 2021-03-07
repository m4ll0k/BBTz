#!/usr/bin/python

# by m4ll0k - @m4ll0k

import sys
try:
	import requests
	import tldextract
except Exception as err:
	sys.exit(print(f'{err}',))
import json

t_gre  = "\033[1;32m" 
t_red  = "\033[1;31m"
t_end  = "\033[0m"

def getContent(domain,tld):
	try:
		r = requests.get(
			f'https://registration.domain.com/domains/search/{domain}?propertyID=47&searchTerm={domain}&tlds={tld}'
			)
		contentType = r.headers.get('Content-Type') if r.headers.get('Content-Type') else r.headers.get('content-type') 
		if 'json' in contentType:
			return json.loads(r.content)
		return {}
	except Exception as err:
		sys.exit(print(f"[ERROR]: {err}"))

def extractTLD(target):
	tld =  tldextract.extract(target)
	target = tld.domain + '.' + tld.suffix
	tld = tld.suffix
	return (target,tld)

def main(target,tld):
	_json = getContent(target,tld)
	if _json not in [{},"{}"]:
		if _json.get('results'):
			if _json.get('results')[0].get('domainInfo'):
				availability = _json.get('results')[0].get('domainInfo').get('availability')
				domain       = _json.get('results')[0].get('domainInfo').get('domain')
				if availability:
					availability = "available"
					print(f'{t_gre}{availability}{t_end} - {domain}')
					return not 1
				availability = "unavailable"
				print(f'{t_red}{availability}{t_end} - {domain}')
				return not 0

try:
	targets = []  
	for lines in sys.stdin.readlines():
		liness = lines.strip()
		if lines == '\n': sys.exit(print('cat urls.txt | python3 {Name}'.format(Name=sys.argv[0])))
		t = extractTLD(liness)
		# remove duplicates
		if t not in targets:
			targets.append(t)
	for target in targets:
		main(target[0],target[1])
except Exception as e:
	raise
