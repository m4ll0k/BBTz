import requests
import json
import sys

if len(sys.argv) < 2 or len(sys.argv) > 4:
	print '%s [domain] [output]'%sys.argv[0]
	sys.exit(0)

all_links = []

domain = sys.argv[1]
try:
	filename = sys.argv[2]
except IndexError:
	filename = None

import urlparse 

parse = urlparse.urlparse(domain)
if parse.netloc:
	domain = parse.netloc
elif parse.path != '' and parse.netloc == '':
	domain = parse.path
else: domain = domain

def archive():
	content = requests.get('http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=json&collapse=urlkey'%domain).content
	c = json.loads(content)
	for i in c:
		for b in i:
			if domain in b and b.startswith('http'):
				if b not in all_links:
					all_links.append(b)

##
## http://index.commoncrawl.org/CC-MAIN-2018-22-index?url=*.rezserver.com/*&output=json
##
archive()

if filename != None:
	file = open(filename,'w+')

for i in all_links:
	if filename:
		i = i.replace('\u3000','')
		i = i.replace(r'\u','')
		file.write('%s\n'%i.encode('ascii', 'ignore').decode('ascii'))
	else:
		print i
if filename:
	file.close()
