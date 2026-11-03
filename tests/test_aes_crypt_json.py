import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

from aes_env_crypt import aesCryptJson
from aes_env_crypt import cli


class AesCryptJsonTests(unittest.TestCase):
    def test_round_trip_and_incorrect_password(self):
        data = {'AZURE_STORAGE_SAS_TOKEN': 'dummy-token', 'OTHER': 'x$"`'}
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / 'dummy.aes')
            encrypted = aesCryptJson(filename, 'test-only-password')
            encrypted.encrypt(data)
            self.assertEqual(Path(filename).read_bytes()[:3], b'AES')
            self.assertEqual(encrypted.decrypt(), data)
            with self.assertRaises(ValueError):
                aesCryptJson(filename, 'wrong-password').decrypt()

    def test_import_does_not_require_azure_cli(self):
        self.assertNotIn('azure.cli.core', sys.modules)


class CliTests(unittest.TestCase):
    def run_cli(self, func, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            func(list(argv))
        return out.getvalue()

    def test_args_env_and_json_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            base = str(Path(folder) / 'creds')
            self.run_cli(cli.args_to_aes_file, '-f', base, '-p', 'pw', '-d', 'token=a=b$c', 'NAME="x"')
            self.assertEqual(aesCryptJson(base + '.aes', 'pw').decrypt(), {'token': 'a=b$c', 'NAME': '"x"'})
            exports = self.run_cli(cli.env_from_aes_file, '-f', base + '.aes', '-p', 'pw')
            self.assertEqual(exports.splitlines(), ['export TOKEN="a=b\\$c"', 'export NAME="\\"x\\""'])
            self.run_cli(cli.json_from_aes_file, '-f', base + '.aes', '-p', 'pw')
            self.assertEqual(json.loads(Path(base + '.json').read_text()), {'token': 'a=b$c', 'NAME': '"x"'})

    def test_malformed_assignment_exits_nonzero_without_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            base = str(Path(folder) / 'creds')
            with self.assertRaises(SystemExit) as raised:
                self.run_cli(cli.args_to_aes_file, '-f', base, '-p', 'pw', '-d', 'no-equals-sign')
            self.assertEqual(raised.exception.code, 1)
            self.assertFalse(Path(base + '.aes').exists())


if __name__ == '__main__':
    unittest.main()
