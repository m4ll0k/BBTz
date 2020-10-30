#!/usr/bin/python

import sys
import json
import argparse 

def readfile(file):
	return [x.strip() for x in open(file,"r")]

def process(content):
	_all = []
	for i in content:
		_all.append((i,"" if a.payload == "" else a.payload))
	k = {}
	for i in _all:
		k.update({i[0]:i[1]})
	print(json.loads(json.dumps(str(k))).replace("'",'"').replace(' ',''))

p = argparse.ArgumentParser()
p.add_argument('-f','--file',help="set this flag if your input is file",default=False,
	action="store_true")
p.add_argument('-i','--input',help="input your string (str1;str2;) or file",default="",required=True,
	action="store")
p.add_argument('-p','--payload',help="payload for inject in json values",default="",required=False,
	action="store")
a = p.parse_args()

if a.input == "":
	sys.exit(print('[ + ] help'))
else:
	_all = []
	if a.file is False:
		for i in a.input.split(';'):
			_all.append(i)
	else:
		for i in readfile(a.input):
			_all.append(i)
	process(_all)
