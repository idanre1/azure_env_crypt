# pip install pyAesCrypt
import pyAesCrypt
import json
import io
import os
class aesCryptJson():

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
			encFileSize = os.stat(self.encFilename).st_size
			# decrypt file stream
			pyAesCrypt.decryptStream(fIn, fOut, self.password, self.bufferSize, encFileSize)
			return json.loads(fOut.getvalue().decode('utf-8'))

if __name__ == "__main__":
    # Simple testing
	filename="testAesCrypt.aes"
	password="1234"
	aes=aesCryptJson(filename, password)
	
	# test
	d = {'test_aes_name': 'foo', 'test_aes_family': 'bar'}
	print('Golden:')
	print(d)

	# encrypt
	aes.encrypt(d)

	print('Encrypted file content:')
	with open(filename, 'rb') as f:
		encFileSize = os.stat(filename).st_size
		chrString = f.read(encFileSize)
		print(chrString)

	# decrypt
	j = aes.decrypt()
	print('Decrypted file content:')
	print(j)
