#!/usr/bin/env python
# myaltdns - my altdns implementation 
# by @m4ll0k - github.com/m4ll0k

# Credit: 
# https://github.com/infosec-au/altdns | @infosec-au


'''Usage:

<stdin>

$ cat targets.txt         | python3 altdns.py -w wordlist.txt 
$ echo "www.google.com"   | python3 altdns.py -w wordlist.txt 

<file>
$ python3 altdns.py -w wordlist.txt mytargets.txt 

<domain string>
$ python3 altdns.py -w wordlist.txt www.google.com

<wordlist like words>
$ python3 altdns.py -w "stg,dev,01,test,staging,aws" www.google.com

<increase and decrease numbers (if found in subdomain)>
$ python3 altdns.py -w "stg,dev" www10.google.com -i 5 -d 5 # increase 5 = www11. ... www15.  decrease 5 = www10. ... www5.

<threads>
$ python3 altdns.py -w "stg,dev" mytargets.txt -t 100

<add number suffix>
$ python3 altdns.py -w "stg,dev" www.google.com -n

<output>
$ python3 altdns.py -w "stg,dev" www.google.com -n > outputfile.txt 

<pipe with other tools like massdns,dnsx,..etc>

$ python3 altdns.py -w "stg,dev" mytargets.txt -n  -i 5 -d 5 | massdns -r resolvers.txt -t A -o S -w output.txt 


'''


import sys 
import tldextract
import argparse
import re
import os

from multiprocessing.pool import ThreadPool


def get_alteration_words(wordlist_fname):
    with open(wordlist_fname, "r") as f:
        return [x.strip() for x in f.readlines()]

def insert_0(domain,word):
    ext = tldextract.extract(domain)
    current_sub = ext.subdomain.split(".")
    '''
    www.google.com -> word.www.google.com 
    '''
    for index in range(0,len(current_sub)):
        current_sub.insert(index,word)
        actual_sub = ".".join(current_sub)
        full_url = f'{actual_sub}.{ext.domain}.{ext.suffix}'
        print(full_url)
    ''' 
    www.google.com -> www.word.google.com
    ''' 
    current_sub = ext.subdomain.split(".")
    current_sub.append(word)
    actual_sub = ".".join(current_sub)
    full_url = f'{actual_sub}.{ext.domain}.{ext.suffix}'
    print(full_url)

def insert_1(domain,word):
    ext = tldextract.extract(domain)
    current_sub = ext.subdomain.split(".")
    for word in range(0,10):
        for index,value in enumerate(current_sub):
            '''
            www.google.com -> www-1.google.com
            '''
            original_sub = current_sub[index]
            current_sub[index] = current_sub[index] + "-" + str(word)
            actual_sub = ".".join(current_sub)
            full_url = f'{actual_sub}.{ext.domain}.{ext.suffix}'
            print(full_url)
            '''
            www.google.com -> www1.google.com
            '''
            current_sub[index] = original_sub
            original_sub = current_sub[index]
            current_sub[index] = current_sub[index] + str(word)
            actual_sub = ".".join(current_sub)
            full_url= f'{actual_sub}.{ext.domain}.{ext.suffix}'
            print(full_url)
            '''
            www.google.com -> 1-www.google.com
            '''
            current_sub[index] = original_sub
            original_sub = current_sub[index]
            current_sub[index] = str(word) + '-' + current_sub[index] 
            actual_sub = ".".join(current_sub)
            full_url= f'{actual_sub}.{ext.domain}.{ext.suffix}'
            print(full_url)
            '''
            www.google.com -> 1www.google.com
            '''
            current_sub[index] = original_sub
            original_sub = current_sub[index]
            current_sub[index] = str(word) + current_sub[index]
            actual_sub = ".".join(current_sub)
            full_url= f'{actual_sub}.{ext.domain}.{ext.suffix}'
            print(full_url)
            current_sub[index] = original_sub


def insert_3(domain,word):
    ext = tldextract.extract(domain)
    current_sub = ext.subdomain.split('.')
    if re.search(r'\d+',ext.subdomain,re.I):
        for index,value in enumerate(current_sub):
            '''
            www1.google.com  -> www2.google.com ... www10.google.com
            www10.google.com -> www9.google.com ... www0.google.com
            '''
            digits = re.findall(r'\d{1,3}',current_sub[index],re.I)
            original_sub = current_sub[index]
            for digit in digits:
                cur_digit = digit
                for i in range(DECREASE,INCREASE):
                    digit = int(cur_digit) + int(i)
                    if digit < 0:
                        continue 
                    current_sub[index] = current_sub[index].replace(str(cur_digit),str(digit))
                    actual_sub = ".".join(current_sub)
                    full_url= f'{actual_sub}.{ext.domain}.{ext.suffix}'
                    print(full_url)
                    current_sub[index] = original_sub

def insert_2(domain,word):
    ext = tldextract.extract(domain)
    current_sub = ext.subdomain.split(".")
    for index,value in enumerate(current_sub):
        '''
        www.google.com -> www-word.google.com
        '''
        original_sub = current_sub[index]
        current_sub[index] = current_sub[index] + "-" + word
        actual_sub = ".".join(current_sub)
        full_url= f'{actual_sub}.{ext.domain}.{ext.suffix}'
        print(full_url)
        '''
        www.google.com -> word-www.google.com
        '''
        current_sub[index] = original_sub
        current_sub[index] = word + '-' + current_sub[index]
        actual_sub = ".".join(current_sub)
        full_url= f'{actual_sub}.{ext.domain}.{ext.suffix}'
        print(full_url)
        '''
        www.google.com -> WORDwww.google.com
        '''
        current_sub[index] = original_sub
        current_sub[index] = word + current_sub[index]
        actual_sub = ".".join(current_sub)
        full_url= f'{actual_sub}.{ext.domain}.{ext.suffix}'
        print(full_url)
        '''
        www.google.com -> wwwWORD.google.com
        '''
        current_sub[index] = original_sub
        current_sub[index] = current_sub[index]+word
        actual_sub = ".".join(current_sub)
        full_url= f'{actual_sub}.{ext.domain}.{ext.suffix}'
        print(full_url)
        current_sub[index] = original_sub


def alter(domain,word,number):
    if number:
        for funct in [insert_0,insert_1,insert_2,insert_3]:
            funct(domain,word)
    else:
        for funct in [insert_0,insert_2,insert_3]:
            funct(domain,word)

def isDomain(string):
    ext = tldextract.extract(string)
    if ext.suffix  != '':
        return True 
    return False

def main():
    global INCREASE
    global DECREASE

    parser = argparse.ArgumentParser()
    parser.add_argument("input",nargs="?",default=(None if sys.stdin.isatty() else sys.stdin),help="Input: <stdin> OR <file> OR <domain string>")
    parser.add_argument("-w", "--wordlist",help="Wordlist OR list of words like argument, e.g: \"word,word1,word2..\"",required=False, default="",action="store")
    parser.add_argument("-t", "--threads",help="Amount of threads to run simultaneously, default = 50", default=50, type=int)
    parser.add_argument("-n","--number",help="Add number suffix to every domain (0-9), default = False",default=False,action="store_true")
    parser.add_argument("-i","--increase",help="Add number to increase, if number is found in subdomain, default = 0",default=0,type=int)
    parser.add_argument("-d","--decrease",help="Add number to decrease, if number is found in subdomain, defualt = 0",default=-0,type=int)
    args = parser.parse_args()
    
    if args.wordlist == "":
        sys.exit(
            parser.print_usage()
        )
    alteration_words = []
    if os.path.exists(args.wordlist) and os.path.isfile(args.wordlist):
        alteration_words = get_alteration_words(args.wordlist)
    else:
        for word in args.wordlist.split(','):
            if word not in alteration_words:
                alteration_words.append(word)
    # --
    INCREASE = args.increase
    DECREASE = -args.decrease if args.decrease > 0 else args.decrease 
    # --
    targets  =  []
    if args.input is None:
        sys.exit(
            parser.print_usage()
        )
    elif sys.stdin.isatty() is False:
        for target in args.input.readlines():
            target = target.strip()
            if target != '\n' and target not in targets:
                targets.append(target)
    elif sys.stdin.isatty() is True and os.path.exists(args.input) and os.path.isfile(args.input):
        for target in get_alteration_words(args.input):
            if target not in  targets:
                targets.append(target)
    elif isDomain(args.input):
        targets.append(args.input)
    else:
        sys.exit(
            parser.print_usage()
        )
    # --
    t_pool = ThreadPool(args.threads)
    for target in targets:
        for word in alteration_words:
            w = t_pool.apply_async(
                alter,(target,word,args.number)
            )
            w.get()
    t_pool.close()
    t_pool.join()

if __name__ == "__main__":
    main()
