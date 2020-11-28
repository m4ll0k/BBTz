# antiburl - advanced anti-burl tool 
# https://github.com/tomnomnom/hacks/blob/master/anti-burl/readme.md
# m4ll0k - github.com/m4ll0k

# usage:
# cat myurls.txt | python3 antiburl.py -A -X 400,404,403,401 -H 'header:value' 'header2:value2' -N -C "mycookies=10" -T 50 

import requests
import concurrent.futures 
import threading 
import argparse
import urllib3
import sys


t_l = threading.local()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

default_headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
}


def Session():
    if not hasattr(t_l, "session"):
        t_l.session = requests.Session()
    return t_l.session

def http(url):
	exclude = []
	if args.exclude != "":
		exclude = args.exclude.split(',')
	headers = {}
	if args.cookie != "":
		headers.update({'Cookie':args.cookie})
	if args.headers != []:
		for h in args.headers:
			headers.update({h.split(':')[0]:h.split(':')[0]})
	headers.update(default_headers)
	try:
		session = Session()
		resp = session.get(url,
			headers=headers,
			allow_redirects=False if args.allowRedirect is False else True,
			verify = False
		)
		if resp.status_code:
			code = str(resp.status_code)
			if code not in exclude:
				print(code+"\t"+resp.url)
	except (requests.exceptions,Exception) as err:
		pass

def main(urls):
	if args.nobanner is False:
		print('Code\tURL')
	with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
		executor.map(http,urls)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-C','--cookie',help="set cookies,-C \"test=10..\"",action="store",default="")
	parser.add_argument('-H','--headers',help="add headers, -H \"header:value\" \"header2:value2\"",action="store",nargs="+",default=[])
	parser.add_argument('-X','--exclude',help="exclude http code, -X 403,302,301",action="store",default="")
	parser.add_argument('-A','--allowRedirect',help="allow http redirect, default=false",action="store_true",default=False)
	parser.add_argument('-T','--threads',type=int,default=10,help="set threads, default=10")
	parser.add_argument('-N','--nobanner',default=False,action="store_true",help="No banner (code and url)")
	parser.add_argument('url',action="store",nargs="?",default=(None if sys.stdin.isatty() else sys.stdin),help="read urls from stdin")
	args = parser.parse_args()

	if args.url:
		urls = []
		for url in args.url.readlines():
			url = url.strip()
			if url != '\n':
				urls.append(url)
		if urls[0] == '':
			sys.exit(parser.print_usage())
		main(urls)
