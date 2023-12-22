import os
import base58
import argparse
import rsa
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def sanitize_filename(filename):
    """
    Function to sanitize the filename.
    Function Removes characters that are not safe in filenames.
    """
    return re.sub(r'[/:*?"<>|]', '', filename)


def load_file(file_path):
    """Load a file (any extension)"""
    with open(file_path, "rb") as file:
        file_data = file.read()
    return file_data


def generate_aes_key():
    """Generate an AES-256 symmetric key"""
    return os.urandom(32)


def encrypt_file(data, aes_key):
    """Encrypt the loaded file using AES-256"""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return iv, encrypted_data


def encrypt_aes_key(aes_key):
    """Load the RSA public key from a file"""
    with open("public_key.pem", "rb") as f:
        rsa_public_key = rsa.PublicKey.load_pkcs1(f.read())
    encrypted_aes_key = rsa.encrypt(aes_key, rsa_public_key)
    return encrypted_aes_key


def encode_aes_key(encrypted_key):
    alphabet = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    return base58.b58encode(encrypted_key, alphabet).decode()


def embed_encoded_key(file_path, encoded_key):
    root, extension = os.path.splitext(file_path)
    output_file_path = f"{root}.{encoded_key}{extension}"
    return output_file_path


def encrypt_file_main():
    parser = argparse.ArgumentParser(
        description='Encrypt a file using AES-256 encryption and RSA encryption of the AES key with Base58 encoding.')
    parser.add_argument('input_file', type=str, help='Input file to be encrypted')

    args = parser.parse_args()

    try:
        # Load the file
        file_data = load_file(args.input_file)

        # Generate an AES-256 symmetric key
        aes_key = generate_aes_key()

        # Encrypt the file using AES-256
        iv, encrypted_data = encrypt_file(file_data, aes_key)

        # Encrypt the AES-256 key using the RSA public key
        encrypted_aes_key = encrypt_aes_key(aes_key)

        # Encode the encrypted key using Base58
        encoded_aes_key = encode_aes_key(encrypted_aes_key)

        # Sanitize the input filename to avoid invalid characters
        input_filename = sanitize_filename(args.input_file)

        # Build the output filename with sanitized input filename
        output_file = embed_encoded_key(input_filename, encoded_aes_key)

        # Save the encrypted data to the new file
        with open(output_file, "wb") as file:
            file.write(iv + encrypted_data)

        print(f"File '{input_filename}' encrypted and saved as '{output_file}'.")

    except (FileNotFoundError, FileExistsError) as e:
        print(f"Problem occured when reading/writing file. Details: {e}")
    except Exception as e:
        print(f"Other error occured: {str(e)}")


if __name__ == "__main__":
    encrypt_file_main()
