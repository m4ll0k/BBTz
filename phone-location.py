#!/usr/bin/python

import requests
import json
import sys

if len(sys.argv) == 1:
	print('Usage:')
	print('\t%s +[country code]number'%(sys.argv[0]))
	print('\tExample: %s +390000000000\n'%(sys.argv[0]))
	sys.exit(0)

content = requests.get('https://www.phone-location.info/socialcheck/phone?provider=phone&path=%s'%(sys.argv[1])).content
jsoned = json.loads(content,'utf-8')

if jsoned['result']:
	r = jsoned['result']
	if r['uid']:
		print('Number: '+r['uid'])
	l = jsoned['location']
	if l['city']:
		print('City: '+l['city'])
	if l['country']:
		print('Country: '+l['country'])
	if l['region']:
		print('Region: '+l['region'])
	if l['district']:
		print('District: '+l['district'])
	if l['operator_fullname']:
		print('Operator: %s - %s'%(l['operator'],l['operator_fullname']))
	g = l['geo_city']
	if g['latitude'] and g['longitude']:
		print('Geo City: lat(%s)-log(%s)'%(g['latitude'],g['longitude']))
