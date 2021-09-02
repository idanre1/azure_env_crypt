import argparse
import os
from aes_crypt_json import aesCryptJson

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", action='store', type=str, required=True, help=".aes filename to read encrypted data")
parser.add_argument("-p", "--password", action='store', type=str, required=True, help="aes password for open")
args = parser.parse_args()

aes=aesCryptJson(args.filename, args.password)
secret_data = aes.decrypt()
for name, value in secret_data.items():
	# Escape symbols commonly used by Bash.
	value = value.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')

	print('export {}="{}"'.format(
            name.upper(),
            value
        ))
