import argparse
import os
import random
import string
import shutil

def wipe_and_delete_file(path, rounds=3):
    try:
        with open(path, "rb+") as file:
            file_size = os.path.getsize(path)
            file.truncate(0)  # Clear the file content

            for _ in range(rounds):
                random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=file_size))
                file.write(random_data.encode())

        os.remove(path)
        print(f"File '{path}' has been wiped, overwritten {rounds} times, and deleted.")
    except Exception as e:
        print(f"Error: {str(e)}")


def wipe_and_delete_path(path, rounds=3):
    """
    - path (str): The file or directory to be wiped and deleted.
    - rounds (int): Number of overwrite rounds (default: 3).
    """
    try:
        if os.path.isfile(path):
            wipe_and_delete_file(path, rounds)
        elif os.path.isdir(path):
            # If it's a directory, wipe recursively and then delete it
            for root, _, files in os.walk(path):
                for file in files:
                    wipe_and_delete_file(os.path.join(root, file), rounds)
            shutil.rmtree(path)
        else:
            print(f"Path '{path}' does not exist or is not a valid file or directory.")

        print(f"Path '{path}' has been wiped, overwritten {rounds} times, and deleted.")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Wipe and delete file by overwriting it with random data.')
    parser.add_argument('path', type=str, help='File or directory to be wiped and deleted')
    parser.add_argument('--rounds', type=int, default=3, help='Number of overwrite rounds (default: 3)')

    args = parser.parse_args()

    # Call the wipe_and_delete_file function with the specified filename and rounds
    wipe_and_delete_file(args.path, args.rounds)

if __name__ == "__main__":
    main()
