#/usr/bin/env python3 
# params combination finder
# example:
'''
$ echo "customer_id" | python3 paramsCFinder.py

Customer
Id
customer
id
CUSTOMER
ID
Customer_Id
customer_id
CUSTOMER_ID
CustomerId
customerid
CUSTOMERID
_CustomerId
_customerid
_CUSTOMERID
_Customer_Id
_customer_id
_CUSTOMER_ID
Customer_id
Customer_Id
customer_Id
customer_id
CUSTOMER_id
CUSTOMER_ID
CustomerID
CustomerId
customerId
customerid
CUSTOMERid
CUSTOMERID
_CustomerID
_CustomerId
_customerId
_customerid
_CUSTOMERid
_CUSTOMERID
_Customer_ID
_Customer_Id
_customer_Id
_customer_id
_CUSTOMER_id
_CUSTOMER_ID

# another example:
$ echo "customer_id" |python3 paramsCFinder.py|tr '\n' '='|sed 's/=/=\&/g' 

Customer=&Id=&customer=&id=&CUSTOMER=&ID=&....
'''



def _0x1_(Str:str)->str:return str(Str).capitalize()
def _0x2_(Str:str)->str:return str(Str).casefold()
def _0x3_(Str:str)->str:return str(Str).upper()
def _0x5_(Strs:list)->list:Strs[0] = _0x1_(Strs[0]);return Strs
def _0x6_(Strs:list)->list:Strs[-1] = _0x1_(Strs[-1]);return Strs
def _0x7_(Strs:list)->list:Strs[0] = _0x2_(Strs[0]);return Strs
def _0x8_(Strs:list)->list:Strs[-1] = _0x2_(Strs[-1]);return Strs
def _0x9_(Strs:list)->list:Strs[0] = _0x3_(Strs[0]);return Strs
def _0x10_(Strs:list)->list:Strs[-1] = _0x3_(Strs[-1]);return Strs

def _0x4_(Str:str)->None: 
	if '_' in Str:
		StR=Str.split('_')
		[print(_0x1_(_0x1))for _0x1 in StR]
		[print(_0x2_(_0x1))for _0x1 in StR]
		[print(_0x3_(_0x1))for _0x1 in StR]
		#
		print("_".join([_0x1_(_0x1)for _0x1 in StR]))
		print("_".join([_0x2_(_0x1)for _0x1 in StR]))
		print("_".join([_0x3_(_0x1)for _0x1 in StR]))
		#
		print("".join([_0x1_(_0x1)for _0x1 in StR]))
		print("".join([_0x2_(_0x1)for _0x1 in StR]))
		print("".join([_0x3_(_0x1)for _0x1 in StR]))
		#
		print("_"+"".join([_0x1_(_0x1)for _0x1 in StR]))
		print("_"+"".join([_0x2_(_0x1)for _0x1 in StR]))
		print("_"+"".join([_0x3_(_0x1)for _0x1 in StR]))
		#
		print("_"+"_".join([_0x1_(_0x1)for _0x1 in StR]))
		print("_"+"_".join([_0x2_(_0x1)for _0x1 in StR]))
		print("_"+"_".join([_0x3_(_0x1)for _0x1 in StR]))
		# 
		print("_".join(_0x5_(StR)))
		print("_".join(_0x6_(StR)))
		print("_".join(_0x7_(StR)))
		print("_".join(_0x8_(StR)))
		print("_".join(_0x9_(StR)))
		print("_".join(_0x10_(StR)))
		#
		print("".join(_0x5_(StR)))
		print("".join(_0x6_(StR)))
		print("".join(_0x7_(StR)))
		print("".join(_0x8_(StR)))
		print("".join(_0x9_(StR)))
		print("".join(_0x10_(StR)))
		#
		print("_"+"".join(_0x5_(StR)))
		print("_"+"".join(_0x6_(StR)))
		print("_"+"".join(_0x7_(StR)))
		print("_"+"".join(_0x8_(StR)))
		print("_"+"".join(_0x9_(StR)))
		print("_"+"".join(_0x10_(StR)))
		#
		print("_"+"_".join(_0x5_(StR)))
		print("_"+"_".join(_0x6_(StR)))
		print("_"+"_".join(_0x7_(StR)))
		print("_"+"_".join(_0x8_(StR)))
		print("_"+"_".join(_0x9_(StR)))
		print("_"+"_".join(_0x10_(StR)))

	elif '-' in Str:
		StR=Str.split('-')
		[print(_0x1_(_0x1))for _0x1 in StR]
		[print(_0x2_(_0x1))for _0x1 in StR]
		[print(_0x3_(_0x1))for _0x1 in StR]
		#
		print("-".join([_0x1_(_0x1)for _0x1 in StR]))
		print("-".join([_0x2_(_0x1)for _0x1 in StR]))
		print("-".join([_0x3_(_0x1)for _0x1 in StR]))
		#
		print("".join([_0x1_(_0x1)for _0x1 in StR]))
		print("".join([_0x2_(_0x1)for _0x1 in StR]))
		print("".join([_0x3_(_0x1)for _0x1 in StR]))
		#
		print("_"+"".join([_0x1_(_0x1)for _0x1 in StR]))
		print("_"+"".join([_0x2_(_0x1)for _0x1 in StR]))
		print("_"+"".join([_0x3_(_0x1)for _0x1 in StR]))
		#
		print("_"+"-".join([_0x1_(_0x1)for _0x1 in StR]))
		print("_"+"-".join([_0x2_(_0x1)for _0x1 in StR]))
		print("_"+"-".join([_0x3_(_0x1)for _0x1 in StR]))
		#
		print("-".join(_0x5_(StR)))
		print("-".join(_0x6_(StR)))
		print("-".join(_0x7_(StR)))
		print("-".join(_0x8_(StR)))
		print("-".join(_0x9_(StR)))
		print("-".join(_0x10_(StR)))
		#
		print("".join(_0x5_(StR)))
		print("".join(_0x6_(StR)))
		print("".join(_0x7_(StR)))
		print("".join(_0x8_(StR)))
		print("".join(_0x9_(StR)))
		print("".join(_0x10_(StR)))
		#
		print("_"+"".join(_0x5_(StR)))
		print("_"+"".join(_0x6_(StR)))
		print("_"+"".join(_0x7_(StR)))
		print("_"+"".join(_0x8_(StR)))
		print("_"+"".join(_0x9_(StR)))
		print("_"+"".join(_0x10_(StR)))
		#
		print("_"+"-".join(_0x5_(StR)))
		print("_"+"-".join(_0x6_(StR)))
		print("_"+"-".join(_0x7_(StR)))
		print("_"+"-".join(_0x8_(StR)))
		print("_"+"-".join(_0x9_(StR)))
		print("_"+"-".join(_0x10_(StR)))
	else:
		print(_0x1_(Str))
		print(_0x2_(Str))
		print(_0x3_(Str))
		print("_"+_0x1_(Str))
		print("_"+_0x2_(Str))
		print("_"+_0x3_(Str))
		print(_0x1_(Str)+"_")
		print(_0x2_(Str)+"_")
		print(_0x3_(Str)+"_")


try:
	import sys
	for lines in sys.stdin.readlines():
		liness = lines.strip()
		if lines == '\n': sys.exit(print('cat myparams.txt | python3 {Name}'.format(Name=sys.argv[0])))
		_0x4_(liness)
except Exception as e:
	raise
