import sys,html
from urllib import parse
from html import unescape 

# gau target.com | python3 getPaths.py

allLinks = []

def main(url):
	url = url.replace(':80','')
	parts = parse.urlparse(unescape(parse.unquote(url)))
	final_url = parts.path + ('?' + parts.query if parts.query != '' else '') + ('#' + parts.fragment if parts.fragment != '' else '')
	print(final_url)

for i in sys.stdin.readlines():
	i = i.strip()
	main(i)
