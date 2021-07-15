#!/usr/bin/env python
# by @m4ll0k - github.com/m4ll0k
# strtool.py  (beta v1) - strings percentage filter (filter wordlist,payloads,..etc)
# - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -- - - - 

'''
- Purpose:

Many times, the bug hunters,hackers,..etc are found to have very long wordlist with non-sense string
take for example this list of subdomains:

_dkdks-_akdkd345233822893992.cnp.345
02020220202202-34958303093-239448449
4939343833883838299292aaaabbb9399393


that 99% of the time such a subdomains does not exist, so filtering the list, you can save a lot of unnecessary requests and waste of time!


- Usage:


$ cat a.txt

malloc
m4ll0k
malloc_1234
_2334_-fm@kd


$ cat a.txt|python3 strtool.py --print "N = 0" # print where % of numbers (12345...) equal to zero, (< or = or >)
$ cat a.txt|python3 strtool.py --print "S = 0" # print where % of specials chars (_-@#...) equal to zero, (< or = or >)
$ cat a.txt|python3 strtool.py --print "C = 0" # print where % of chars (abcdef...) equal to zero, (< or = or >)

filter multiple options with AND (&&)

$ cat a.txt|python3 strtool.py --print "N = 0 && S = 0" # print where % of numbers and special chars equal to zero, (< or = or >)
$ cat a.txt|python3 strtool.py --print "N < 10 && S < 10" # print where % of numbers and special chars less than 10 (%), (< or = or >)



# input by stdin:

$ cat wordlist.txt | python3 strtool.py ... 

# input by file

$ python3 strtool.py wordlist.txt ... 

# input by string 

$ python3 strtool.py "testme" ...
 



'''

import sys 
import string
import os 
import re
import argparse
from argparse import RawTextHelpFormatter

NUMBERS  = string.digits
CHARS    = string.ascii_letters
SPECIALS = string.punctuation

def _p(STR):
	LENs = len(STR)
	PERC = lambda x:x/LENs * 100
	len_number = 0 
	len_chars  = 0 
	len_specials = 0 
	for i in STR:
		if i in NUMBERS:
			len_number += 1 
		if i in  CHARS:
			len_chars += 1 
		if i in SPECIALS:
			len_specials += 1 
	return {'L':f'{PERC(LENs):.2f}% ({LENs})',
			'N':f'{PERC(len_number):.2f}% ({len_number})',
			'S':f'{PERC(len_specials):.2f}% ({len_specials})',
			'C':f'{PERC(len_chars):.2f}% ({len_chars})'}


def par(S,STR,args):
	S = S.replace(' ','').replace(" ","").replace('=','==')
	action = re.findall(r'(<|>|==)',S,re.I) or None
	opera = re.findall(r'(\&\&)',S,re.I) or None
	if opera:
		S = S.split(opera[0])
		len_opera = len(opera) + 1
		true_list = [] 
		for i in range(len_opera):
			F,K =S[i].split(action[i])
			A = action[i].replace(" ","").replace(' ','')
			F = F.replace(" ","").replace(' ','')
			K = K.replace(" ","").replace(' ','')
			r = _p(STR)
			if eval(f'{r.get(F).split(".")[0]} {A} {K}') and args.print != "":
				true_list.append(True)
			else:
				true_list.append(False)
		if all(true_list) and len(true_list) == len_opera:
			if args.silent:
				print(STR)
			else:
				str_ = f'{STR}'
				for i in r:
					str_ += f' {i}:{r[i]}'
				print(str_)

	elif action:
		F,S = S.split(action[0])
		A = action[0].replace(" ","").replace(' ','')
		F = F.replace(" ","").replace(' ','')
		S = S.replace(" ","").replace(' ','')
		r = _p(STR)
		if eval(f'{r.get(F).split(".")[0]} {A} {S}') and args.print != "":
			if args.silent:
				print(STR)
			else:
				str_=f'{STR}'
				for i in r:
					str_ += f' {i}:{r[i]}'
				print(str_)
	return

def main():
	_w = []
	parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
	parser.add_argument("input",nargs="?",default=(None if sys.stdin.isatty() else sys.stdin),help="Input: <stdin> OR <file> OR <string>")
	parser.add_argument("-s","--silent",help="do not print additional information (silent mode) (default: false)", default = False, action="store_true")
	parser.add_argument("-p", "--print",help='''PRINT IF:\n\nN (numbers)  [> or < or =] number (percent) e.g: N > 20\
		\nS (specials) [> or < or =] number (percent) e.g: S < 1\
		\nC (chars)    [> or < or =] number (percent) e.g: C > 80\
		\n\nor (multiple choice, "AND" only! ):\n\nN (numbers)  [> or < or =] number (percent) && ... e.g: N > 20 && C > 20 && S < 2\
		\n\nE.g:\n\n--print "N < 10" or --print "N < 10 && C > 80"\n\n\n
		''',required=False, default="",action="store")
	args = parser.parse_args()

	if args.input is None:
		sys.exit(
			parser.print_usage()
		) 
	elif sys.stdin.isatty() is False:
		for inputs in args.input.readlines():
			inputs = inputs.strip()
			if inputs != '\n' and inputs not in _w:
				_w.append(inputs)
	elif sys.stdin.isatty() is True and os.path.exists(args.input) and os.path.isfile(args.input):
		for inputs in [x.strip() for x in open(args.input)]:
			if inputs not in _w:
				_w.append(inputs)
	else:
		_w.append(args.input)

	if args.print == "":
		sys.exit(parser.print_usage())
	
	for word in _w:
		par(args.print,word,args)
main()



