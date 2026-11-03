"""Command-line entry points; each keeps the arguments of the former script of the same name."""
import argparse
import json
import pathlib
import re
import sys

from aes_env_crypt.aes_crypt_json import aesCryptJson

_ASSIGNMENT = re.compile('([a-zA-Z0-9_]*)=(.*)')


def _parser(description, write=False):
	parser = argparse.ArgumentParser(description=description)
	help_file = '.aes filename to write (".aes" is appended)' if write else '.aes filename to read encrypted data'
	parser.add_argument("-f", "--filename", action='store', type=str, required=True, help=help_file)
	parser.add_argument("-p", "--password", action='store', type=str, required=True, help="aes password for open")
	return parser


def args_to_aes_file(argv=None):
	"""Encrypt ``VAR=value`` arguments into ``<filename>.aes``; exits 1 on a malformed argument."""
	parser = _parser('Encrypt VAR=value pairs into an .aes file', write=True)
	parser.add_argument("-d", "--dict", nargs='*', type=str, required=True, help="dict like space seperated values to crypt")
	args = parser.parse_args(argv)

	secrets = {}
	print('The value to encrypt:')
	for item in args.dict:
		match = _ASSIGNMENT.fullmatch(item)
		if match is None:
			print(f'Error: arguments must be of pattern VAR=value. Received {item}')
			sys.exit(1)
		var, val = match.groups()
		print(var)
		secrets[var] = val

	aesCryptJson(f'{args.filename}.aes', args.password).encrypt(secrets)
	print('Credentials file: %s.aes' % args.filename)


def env_from_aes_file(argv=None):
	"""Print ``export NAME="value"`` lines for ``eval`` in Bash; names are upper-cased."""
	args = _parser('Print the secrets of an .aes file as Bash exports').parse_args(argv)
	for name, value in aesCryptJson(args.filename, args.password).decrypt().items():
		# Escape symbols commonly used by Bash.
		value = value.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
		print('export {}="{}"'.format(name.upper(), value))


def json_from_aes_file(argv=None):
	"""Decrypt ``<name>.aes`` to plain-text ``<name>.json`` next to it (indent 3)."""
	args = _parser('Decrypt an .aes file to a .json file next to it').parse_args(argv)
	secrets = aesCryptJson(args.filename, args.password).decrypt()
	with open(pathlib.Path(args.filename).with_suffix(".json"), 'w') as out_file:
		json.dump(secrets, out_file, indent=3)
