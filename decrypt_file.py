import os
import base58
import argparse
import rsa
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def sanitize_filename(filename):
    """Function to sanitize the filename.
    Function Removes characters that are not safe in filenames.
    """
    return re.sub(r'[/:*?"<>|]', '', filename)

def load_file(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
    return file_data

def decrypt_file(data, aes_key, iv):
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()
    return decrypted_data

def decrypt_aes_key(aes_key):
    with open("private_key.pem", "rb") as f:
        rsa_private_key = rsa.PrivateKey.load_pkcs1(f.read())
    decrypted_aes_key = rsa.decrypt(aes_key, rsa_private_key)
    return decrypted_aes_key

def decode_aes_key(encoded_key):
    alphabet = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    return base58.b58decode(encoded_key, alphabet)

def decrypt_file_main():
    parser = argparse.ArgumentParser(description='Decrypt a file previously encrypted using'
                                                 ' AES-256 and RSA with Base58 encoding.')
    parser.add_argument('input_file', type=str, help='Input file to be decrypted')
    args = parser.parse_args()

    try:
        # Read the encoded AES key from the input file
        file_name, aes_encoded_with_rsa, extension = args.input_file.split('.')

        # Convert the file name part with the AES key to the encrypted AES key
        aes_encrypted_with_rsa = decode_aes_key(aes_encoded_with_rsa)

        # Decrypt the encrypted AES key with the RSA private key
        aes_key = decrypt_aes_key(aes_encrypted_with_rsa)

        # Read encrypted data with IV from the file
        file_data_with_iv = load_file(args.input_file)

        iv, file_data = file_data_with_iv[:16], file_data_with_iv[16:]

        # Decrypt the file using AES-256
        decrypted_data = decrypt_file(file_data, aes_key, iv)

        # Build the output file name
        root, _ = os.path.splitext(file_name)
        output_file = f"{root}.{extension}"

        # Save the decrypted data to the output file
        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        print(f"File '{args.input_file}' decrypted and saved as '{output_file}'.")

    except (FileNotFoundError, FileExistsError) as e:
        print(f"Problem occured when reading/writing file. Details: {e}")
    except Exception as e:
        print(f"Other error occured: {str(e)}")

if __name__ == "__main__":
    decrypt_file_main()
