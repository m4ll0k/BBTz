#!/usr/bin/python

# m4ll0k - github.com/m4ll0k
# Get shared credentials for your bug bounty targets or for anything else

import requests 
import sys 
from lxml import html

def getFromBugMenot(target):
    try:
        return requests.get(
            'http://bugmenot.com/view/{}'.format(
                target
            )
        )
    except Exception as e:
        sys.exit(
            print(e)
        )

def main(target):
    print('[ + ] Get shared credentials for.. '+str(target))
    r = getFromBugMenot(target)
    if r.status_code == 200:
        print('[ + ] Showing credentials...\n')
        tree = html.fromstring(r.content)
        tree_xpath = tree.xpath('//article[@class="account"]')
        if tree_xpath != []:
            for account_len in range(len(tree_xpath)):
                # process
                cols = []
                vals = []
                for subroot in tree_xpath[account_len].xpath('//dl'):
                    cols = subroot.xpath('//dt/text()')
                    for n in cols:
                        if n == 'Stats:':
                            cols.pop(cols.index(n))
                    vals = subroot.xpath('//dd/kbd/text()')
                for credentials in zip(cols,vals):
                    print('\t{}\t{}'.format(
                        credentials[0].split(':')[0] if len(credentials[0]) > 6 else credentials[0].split(':')[0]+"\t",credentials[1]
                        ))
                    print("\t"+('-'*50))
                print('')
                break
    else:
        print('Not found anything for '+str(target))
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('\nUsage:\n\tpython3 bugmenot.py <target>\n\tpython3 bugmenot.py <target1> <target2> ..\n')
        print('Coded by m4ll0k (@m4ll0k2) github.com/m4ll0k\n')
        sys.exit()
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) > 2:
        for i in sys.argv[1:]:
            main(i)
