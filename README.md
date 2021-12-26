# azure-env-crypt
Enhance AZ CLI to store service principal credentials in AES formats
1. Using service principal you can provide access to specific path inside a storage container
2. Using AES you can store the credentials encrypted and only upon run setup them to env variables for access the container
3. Since the credentails are stored in aes encrypted file, it can be versioned control on github (non-public repos...)

# Usage
The script allows creation of RBAC and encryption on same action
### RBAC creation
python az_register_container.py -r <Resource_group> -a <storage_account> -n <container> -p <.aes file's password you are supposed to remember>
### Setting up env variables from .aes file
source ~/azure-env-crypt/env_from_aes_file.sh <credentials_filename.aes>
  Then you will be prompted to provide the password (hiddenly prompt)

# Setup
pip install -r requirements.txt

