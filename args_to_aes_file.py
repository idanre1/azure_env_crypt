import os
import re
import argparse
from aes_crypt_json import aesCryptJson

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", action='store', type=str, required=True, help=".aes filename to read encrypted data")
parser.add_argument("-p", "--password", action='store', type=str, required=True, help="aes password for open")
parser.add_argument("-d", "--dict", nargs='*', type=str, required=True, help="dict like space seperated values to crypt")
args = parser.parse_args()

d={}

print('The value to encrypt:')
r = re.compile('([a-zA-Z0-9_]*)=(.*)')
for i in args.dict:
	try:
		(var, val) = r.findall(i)[0]
		print(var)
		d[var]=val
	except:
		print(f'Error: arguments must be of pattern VAR=value. Received {i}')
		quit()	

aes=aesCryptJson(f'{args.filename}.aes', args.password)
aes.encrypt(d)
print('Credentials file: %s.aes' % args.filename)
