import os
from common_config import SkipFolders, Extensions, MaxFileSize


def enumerate_folders_and_files(path, skip_unwritable, max_filename_length):
    print(f"Enumerating folders and files in: {path}\n")

    for root, dirs, files in os.walk(path):
        if any(folder_to_skip in root.split('\\') for folder_to_skip in SkipFolders):
            continue
        print(f"\nCurrent directory: {root}")
        print("Folders:")
        for dir_name in dirs:
            print(os.path.join(root, dir_name))
        print("\nFiles:")
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)

            try:
                if skip_unwritable and not os.access(file_path, os.W_OK):
                    continue

                if any(len(part) > max_filename_length for part in file_name.split('.')):
                    continue

                if file_size <= MaxFileSize and any(file_name.endswith(ext) for ext in Extensions):
                    print(f"{file_path} (Size: {file_size} bytes)")
            except Exception as e:
                print(f"Error: {str(e)}")
                continue
        print("-" * 40)

def main():
    path = input("Enter the directory path to enumerate (e.g., /path/to/directory): ")
    skip_unwritable = True
    max_filename_length = 75  # encoded files have lenght 80

    if os.path.exists(path):
        enumerate_folders_and_files(path, skip_unwritable, max_filename_length)
    else:
        print(f"The specified path '{path}' does not exist.")

if __name__ == "__main__":
    main()

