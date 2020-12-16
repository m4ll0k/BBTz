# linkfinder output collector

# example:

# $ cat uber_js.txt | xargs -I @ bash -c 'python3 linkfinder.py -i @ -o cli'| python3 collector.py uber/output
# $ cd uber/output 
# $ ls 
# js.txt params.txt urls.txt paths.txt ...

import sys,html
from urllib import parse
from html import unescape
import re
import os

try:
	outputdir = sys.argv[1]
	if os.path.exists(outputdir) and os.path.isdir(outputdir):
		pass
	elif os.path.exists(outputdir) and os.path.isdir(outputdir) is False:
		sys.exit(print('not a directory!'))
	else:
		os.mkdir(outputdir)
except IndexError:
	print('missing "output" directory! example: paypal/output')
	sys.exit()

jsWrite = open('%s/js.txt'%outputdir,'w')
urlWrite = open('%s/urls.txt'%outputdir,'w')
fileWrite = open('%s/files.txt'%outputdir,'w')
pathsWrite = open('%s/paths.txt'%outputdir,'w')
queriesWrite = open('%s/params.txt'%outputdir,'w')

blacklist = [
r'^application/\w+',
r'^audio/\w+',
r'^text/\w+',
r'^image/\w+',
r'^\./',
r'^\.\./',
r'^chemical/\w+',
r'^conference/\w+',
r'^message/\w+',
r'^model/\w+',
r'\.jpg|\.jpeg|\.gif|\.css|\.tif|\.tiff|\.png|\.ttf|\.woff|\.woff2|\.ico|\.pdf|\.svg'
]

def isurl(path):
	if re.search(r'^http[s]://|^//',path,re.I):
		return True
	return False

def isfile(path):
	k = r'\.asp|\.aspx|\.bat|\.json|\.cfm|\.cgi|\.com|\.dll|\.exe|\.htm|\.html|\.inc|\.jhtml|\.jsa|\.jsp|\.log|\.mdb|\.nsf|\.pcap|\.php|\.php2|\.php3|\.php4|\.php5|\.php6|\.php7|\.phps|\.pht|\.phtml|\.pl|\.reg|\.sh|\.shtml|\.sql|\.swf|\.txt|\.xml'
	if re.search(k,path,re.I):
		return True 
	return False

def isjs(path):
	if re.search(r'\.js',path,re.I):
		return True
	return False

def getParams(path):
	k = parse.urlparse(path).query 
	return list(set(re.findall(r'([a-zA-Z0-9_\-\%\(\)\[\]\;\:\.]+)=',k,re.I)))

def main(url):
	url = unescape(parse.unquote(url))
	if isurl(url):
		urlWrite.write('%s\n'%url) 
	elif isfile(url):
		fileWrite.write('%s\n'%url)
	elif isjs(url):
		jsWrite.write('%s\n'%url)
	elif not re.search('|'.join(blacklist),url,re.I):
		pathsWrite.write('%s\n'%url)
		for i in getParams(url):
			queriesWrite.write('%s\n'%i)

for i in sys.stdin.readlines():
	i = i.strip()
	main(i)

urlWrite.close()
fileWrite.close()
jsWrite.close()
pathsWrite.close()
queriesWrite.close()
