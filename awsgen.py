#!/usr/bin/python

# ---------------------------
# -- by m4ll0k --
# -- github.com/m4ll0k --
# -- awsgen.py: is a simple tool for generates permutations, alterations and mutations of AWS S3 Buckets Names
# ---------------------------

'''
Example:

m4ll0k@m4ll0k tools: python3 awsgen.py my-domain-hosted-in-aws.example.com

my-domain-hosted-in-awsexample.s3.amazonaws.com
my-domain-hosted-in-aws-example.s3.amazonaws.com
my-domain-hosted-in-aws.example.com.s3.amazonaws.com
my-domain-hosted-in-aws_example.s3.amazonaws.com
my-domain-hosted-in-aws-example-com.s3.amazonaws.com
my-domain-hosted-in-aws_example_com.s3.amazonaws.com
my-domain-hosted-in-awsexamplecom.s3.amazonaws.com
my-domain-hosted-in-aws.example.s3.amazonaws.com
com-example-my-domain-hosted-in-aws.s3.amazonaws.com
example-my-domain-hosted-in-aws.s3.amazonaws.com
com_example_my-domain-hosted-in-aws.s3.amazonaws.com
example_my-domain-hosted-in-aws.s3.amazonaws.com
comexamplemy-domain-hosted-in-aws.s3.amazonaws.com
my-domain-hosted-in-aws.s3.amazonaws.com
example.s3.amazonaws.com
com.s3.amazonaws.com
examplemy-domain-hosted-in-aws.s3.amazonaws.com
my-domain-hosted-in-aws.com.s3.amazonaws.com
my-domain-hosted-in-aws-com.s3.amazonaws.com
my-domain-hosted-in-aws_com.s3.amazonaws.com
my-domain-hosted-in-awscom.s3.amazonaws.com
com-my-domain-hosted-in-aws.s3.amazonaws.com
com_my-domain-hosted-in-aws.s3.amazonaws.com
commy-domain-hosted-in-aws.s3.amazonaws.com
example.com.s3.amazonaws.com
example-com.s3.amazonaws.com
example_com.s3.amazonaws.com
examplecom.s3.amazonaws.com
com-example.s3.amazonaws.com
com_example.s3.amazonaws.com
comexample.s3.amazonaws.com
'''

import itertools
import sys 

def _1(t: str) -> str:
	t=t.split('.')[:-1]
	return "".join(t)

def _2(t: str) -> str:
	return t

def _3(t: str) -> str:
	t = t.split('.')[:-1]
	return "-".join(t)

def _4(t: str) -> str:
	t = t.split('.')[:-1]
	return "_".join(t)

def _5(t: str) -> str:
	return t.replace('.','-')

def _6(t: str) -> str:
	return t.replace('.','_')

def _7(t: str) -> str:
	return "".join(t.split('.'))

def _8(t: str) -> str:
	t = t.split('.')[:-1]
	return "-".join(t)

def _9(t: str) -> str:
	t = t.split('.')[:-1]
	return "_".join(t)

def _10(t: str) -> str:
	t = t.split('.')[:-1]
	return "-".join(t)

def _11(t: str) -> str:
	t = t.split('.')[:-1]
	return ".".join(t)

def _12(t: str) -> str:
	t = t.split('.')
	t.reverse()
	return "-".join(t)

def _13(t: str) -> str:
	t = t.split('.')[:-1]
	t.reverse()
	return "-".join(t)

def _14(t: str) -> str:
	t = t.split('.')
	t.reverse()
	return "_".join(t)

def _15(t: str) -> str:
	t = t.split('.')[:-1]
	t.reverse()
	return "_".join(t)

def _16(t: str) -> str:
	t = t.split('.')
	t.reverse()
	return "".join(t)

def _17(t: str) -> list:
	tt = []
	t = t.split('.')
	for a,b in enumerate(itertools.chain.from_iterable(itertools.combinations(t,r) for r in range(len(t)+1))):
		for i in [_1,_3,_2,_4,_5,_6,_7,_8,_9,_10,_11,_12,_13,_14,_15,_16]:
			r = i(".".join(b))
			if r not in tt:
				tt.append(r)
	return tt

def main() -> None:
	tt = []
	t = sys.argv[1]
	for i in [_1,_3,_2,_4,_5,_6,_7,_8,_9,_10,_11,_12,_13,_14,_15,_16,_17]:
		target = i(t)
		if target:
			if type(target) == str:
				if target not in tt:
					tt.append(target)
			elif type(target == list):
				for k in target:
					if k not in tt:
						tt.append(k)
	for t in tt:
		if t != '':
			print("%s.s3.amazonaws.com"%(t))
if __name__ == "__main__":
	if len(sys.argv) < 2 or len(sys.argv) >= 3:
		sys.exit(print('\n$ python3 %s <target>\nExample: python3 %s www.uber.com\n'%(sys.argv[0],sys.argv[0])))
	else:
		main()
