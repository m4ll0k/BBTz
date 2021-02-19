#!/usr/bin/env python3
# by @m4ll0k - github.com/m4ll0k
# regex.rip - Check if a regex is vulnerabel to ReDoS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# https://blog.superhuman.com/how-to-eliminate-regular-expression-denial-of-service/

import sys 
import requests
import json

from colorama.ansi import Fore


def usage():
	sys.exit(
		print(f'python3 {sys.argv[0]} <regex> OR cat myregex.txt | python3 {sys.argv[0]}')
	)

def main(regex):
	try:
		req = requests.post(
			'https://go.regex.rip/check',json={'regexes':[regex]})
		if req.status_code == 200:
			j = json.loads(req.content)
			if j.get('results'):
				for i in j.get('results'):
					if i.get('result') == 'vulnerable':
						results = i.get('result')
						input_  = i.get('input')
						kleene  = i.get('kleene')
						print(f'{Fore.WHITE}{input_.replace(kleene,Fore.GREEN+kleene+Fore.RESET)} -> {Fore.RED}{results.upper()}{Fore.RESET}')
					if i.get('result') == 'ok':
						print(f'{Fore.WHITE}{i.get("input")}{Fore.RESET} -> {Fore.GREEN}{i.get("result").upper()}{Fore.RESET}')
	except Exception as err:
		sys.exit(
			print(f'{err}')
		)


if __name__ == "__main__":
	stdin = False
	if len(sys.argv) > 1 and len(sys.argv) < 3:
		regex = sys.argv[1]
		main(regex)
	else:
		for regex in sys.stdin.readlines():
			stdin = True
			regex = regex.strip()
			if regex == '\n':
				usage
			main(regex)

	if len(sys.argv) == 1 and stdin is False:
		usage()
