import io
import json

import pyAesCrypt


class aesCryptJson():
	"""JSON dict of string secrets stored in a pyAesCrypt (AES-256) encrypted file.

	Parameters
	----------
	encFilename : str
		Path of the encrypted file. ``encrypt`` overwrites it.
	password : str
		AES password. ``decrypt`` raises ``ValueError`` when it is wrong or the file is corrupt.
	"""

	def __init__(self, encFilename, password):
		# Encrypted filename
		self.encFilename = encFilename
		self.password    = password

		# AES config
		self.bufferSize = 64 * 1024

	def encrypt(self, dictObj):
		jsonObj=json.dumps(dictObj)
		fIn = io.BytesIO(bytes(jsonObj,'utf-8'))
		with open(self.encFilename, "wb") as fOut:
			# enrypt file stream
			pyAesCrypt.encryptStream(fIn, fOut, self.password, self.bufferSize)

	def decrypt(self):
		with open(self.encFilename, "rb") as fIn:
			fOut = io.BytesIO()
			# decrypt file stream
			pyAesCrypt.decryptStream(fIn, fOut, self.password, self.bufferSize)
			return json.loads(fOut.getvalue().decode('utf-8'))
