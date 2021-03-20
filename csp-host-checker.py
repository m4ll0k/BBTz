#!/usr/bin/python

# by m4ll0k (@m4ll0k)
# github.com/m4ll0k 
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy

import sys 
import requests 
import re 
import argparse 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


_csp_directive_ = [
"base-uri",
"block-all-mixed-content",
"child-src",
"connect-src",
"default-src",
"font-src",
"form-action",
"frame-ancestors",
"frame-src",
"img-src",
"manifest-src",
"media-src",
"navigate-to",
"object-src",
"plugin-types",
"prefetch-src",
"referrer",
"report-sample",
"report-to",
"report-uri",
"require-sri-for",
"sandbox",
"script-src",
"script-src-attr",
"script-src-elem",
"strict-dynamic",
"style-src",
"style-src-attr",
"style-src-elem",
"trusted-types",
"unsafe-hashes",
"upgrade-insecure-requests",
"worker-src"
]

_csp_source_ = [
"'none'",
"'self'",
"'unsafe-inline'",
"'unsafe-eval'",
"'sha",
"'nonce",
"'strict-dynamic'",
"'unsafe-hashes'"
]

def main(url):
	response = request(url)
	original_csp = None
	for _csp in ['Content-Security-Policy','Content-Security-Policy-Report-Only','content-security-policy-report-only','content-security-policy','X-Content-Security-Policy','x-content-security-policy','x-webkit-csp','X-Webkit-CSP']:
		if response.headers.get(_csp):
			original_csp = response.headers.get(_csp)
			break
	if original_csp is None: return 
	domains = parseCSP(original_csp)
	if args.check:
		for url in domains:
			url = normalizeUrl(url)
			resp = request(url)
			if resp.status_code in range(100,599):
				print('[ %s ] URL: %s'%(resp.status_code,url))
	if args.subs != "":
		for domain in domains:
			root = "." + args.subs
			if root in domain:
				print('%s'%(domain))

def normalizeUrl(url):
	if re.search(r'http[s]://',url,re.I):
		return url 
	if url.startswith('://'):
		return 'http://' + url 
	return 'http://' + url

def request(url):
	try:
		req = requests.session()
		req = req.request(
			method='GET',
			url = url,
			headers = {
				'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
				'Accept'     : 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
				'Connection' : 'close'
			},
			verify=False,
			allow_redirects = True
			)
		return req
	except Exception as err:
		print('[ ! ] %s'%err)

def normalizeCSP(csp):
	__csp = []
	for _csp in csp.split(';'):
		if _csp.startswith(' '):
			_csp = _csp[1:]
		if _csp not in __csp:
			__csp.append(_csp)
	return __csp

def parseCSP(csp):
	csp = normalizeCSP(csp)
	orgin_csp = csp 
	domains = []
	for _csp in csp:
		for __csp in _csp.split(' '):
			if __csp not in _csp_directive_ and __csp not in _csp_source_ and not __csp.startswith("'"):
				domains.append(__csp)
	return domains

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-d','--domains',help="targets, e.g: target1,target2",action="store",default="")
	parser.add_argument('-c','--check',help="retrieve the http code for all urls founded in CSP, default",action="store_true",default=True)
	parser.add_argument('-s','--subs',help="enumerate all subdomains, e.g: -s/--subs \"uber.com\"",action="store",default="")
	parser.add_argument('-S','--stdin',help="targets from stdin",action="store_true",default=False)
	args = parser.parse_args()

	if args.subs != "":
		args.check = False

	if args.domains == "" and args.stdin is False:
		sys.exit(parser.print_help())

	if args.domains != "":
		if args.check is False and args.subs == "":
			exit(parser.print_help())
		for url in args.domains.split(','):
			main(url)
	
	elif args.stdin is True:
		if args.check is False and args.subs == "":
			exit(parser.print_help())
		for url in sys.stdin.readlines():
			url = url.strip()
			if url == '\n':
				sys.exit(parser.print_help())
			main(normalizeUrl(url))
	else:
		sys.exit(parser.print_help())

