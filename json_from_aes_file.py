import argparse
import pathlib
from aes_crypt_json import aesCryptJson
import json

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", action='store', type=str, required=True, help=".aes filename to read encrypted data")
parser.add_argument("-p", "--password", action='store', type=str, required=True, help="aes password for open")
args = parser.parse_args()

aes=aesCryptJson(args.filename, args.password)
secret_data = aes.decrypt()

dump=pathlib.Path(args.filename)
with open(dump.with_suffix(".json"), 'w') as out_file:
    json.dump(secret_data,out_file, indent =3)