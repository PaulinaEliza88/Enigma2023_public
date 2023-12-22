import rsa
import argparse

def main():
    parser = argparse.ArgumentParser(description="RSA key pair generation with flags.")
    parser.add_argument('--generate-keys', action='store_true', help="Generate new RSA keys")
    parser.add_argument('--public-key', default="public_key.pem", help="Public key file path")
    parser.add_argument('--private-key', default="private_key.pem", help="Private key file path")
    parser.add_argument('--key-value', default=512, type=int, help="Key value (512, 4096 or any value bits)")
    args = parser.parse_args()

    if args.generate_keys:
        # Generate new keys
        public_key, private_key = rsa.newkeys(args.key_value)

        with open(args.public_key, "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))

        with open(args.private_key, "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))

        print("RSA key pair generated successfully.")
    else:
        print("No action specified. Use --generate-keys to generate RSA keys.")

if __name__ == "__main__":
    main()
