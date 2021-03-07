# jsmonitor.py - javascript files monitor 
# m4ll0k - github.com/m4ll0k

import requests
import argparse
import urllib3
import hashlib
import sys,os
import json

from multiprocessing.pool import ThreadPool

G = "\033[1;32m"
E = "\033[0m"
R = "\033[1;31m"

# usage
# cat alive_js_file | python3 jsmonitor.py


'''db.json struct
{
	'url':'hash',
	'url1':'hash2'
	....
}

'''
DBPath = '/'.join(
	# split and join
	os.path.abspath(__file__).split('/')[:-1]
	) + '/db.json'

urllib3.disable_warnings(
	urllib3.exceptions.InsecureRequestWarning
)

def writefile(content:str)->None:
	'''
	db.json - write in to 
	'''
	with open(DBPath,'w') as _0x1:
		_0x1.write(f'{content}\n')
		_0x1.close()

def readfile()->{}:
	'''
	db.json - read from db.json (default file name)
	'''
	if os.path.exists(DBPath):
		return  json.loads(''.join(
			[
				X.strip()for X in open(f'{DBPath}')
			]
		).replace("'",'"'))
	else:
		writefile(r'{}')
		return {}

db  = readfile()
tmp_db = db 

def urlinDB(url:str)->bool:
	return not 0 if db.get(url) else not 1

def gethashfromdb(url:str)->str:
	return db.get(url)

def gethash(string:str)->str:
	return hashlib.md5(string).hexdigest()

def comparator(url):
	if urlinDB(url):
		act_hash = gethash(http(url).content)
		db_hash = gethashfromdb(url)
		if act_hash != db_hash:
			print(f'{R}[Change Detected]:{E} {G}{url}{E}')
	else:
		# update db with new url
		print(f'{G}[Not in DB.. added]{E} {url}')
		tmp_db.update({
				f"{url}":f"{gethash(http(url).content)}"
			})

def http(url):
	try:return requests.get(url)
	except Exception as r:
		print(f'{r}')
		return {
		'content':None
		}

def main(urls:list)->[]or{}:
	# threads 10
	workers = []
	t_pool = ThreadPool(args.threads)
	for url in urls:
		w = t_pool.apply_async(
			comparator, (
				url,
			)
		)
		workers.append(w)
	for w in workers:
		w.get()
	t_pool.close()
	t_pool.join()
	# write new db
	writefile(f'{str(tmp_db)}')

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('url',action="store",nargs="?",default=(None if sys.stdin.isatty() else sys.stdin),help="read urls from stdin")
	parser.add_argument('-t','--threads',type=int,help="Number concurrent threads to use, default = 10",default=10,action="store")
	args = parser.parse_args()

	if args.url:
		urls = []
		for url in args.url.readlines():
			url = url.strip()
			if url != '\n' and url not in urls:
				urls.append(url)
		main(urls)
