# 
# Enigma2023_public

### What is Enigma2023? 
### It is a collection of Python scripts that simulate how ransomware behaves. 
#### I've created this project for educational purposes in the field of cybersecurity. 
#### Additionally, my deep interest in understanding the mechanics behind ransomware has driven me to develop this repository.
#
# gen_keys.py
![Generate keys](./images/gen_keys.jpg)
### Generates the public and private keys for the RSA asymmetric encryption algorithm.
# prerequisites
pip install rsa
# 
#### RSA Key Pair Generation Script
#### This script allows you to generate RSA key pairs with customizable key sizes 
#### (512,4096 or other value bits) and save them to specified files.

# Execution information
``` r
python gen_keys.py --generate-keys (generates keys with default values)
python gen_keys.py --generate-keys --key-value <key_size>
python gen_keys.py --generate-keys --public-key  public.pem  --private-key private.pem --key-value 512
```
Options:
``` r
  --generate-keys    Generate new RSA keys.
  --key-value        Key size in bits (512 or 4096). Default is 512.
  --public-key       Public key file path. Default is "public_key.pem".
  --private-key      Private key file path. Default is "private_key.pem".
```
#
#
#