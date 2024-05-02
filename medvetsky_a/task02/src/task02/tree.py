import os
import argparse
from colorama import init, Fore

def scan_directory(directory: str, max_level: int, level: int = 1):
    tree = []
    directories_number, files_number = 0, 0

    tree.append((os.path.basename(os.path.abspath(directory))))
    if level > max_level:
        return tree, directories_number, files_number

    items_list = os.listdir(directory)
    for item in items_list:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            item, sub_directories_number, sub_files_number = scan_directory(item_path, max_level, level + 1)
            directories_number += sub_directories_number + 1
            files_number += sub_files_number
            tree.insert(1, item)
        else:
            files_number += 1
            tree.append(item)
    return tree, directories_number, files_number

def print_tree(tree: list, decor_prefix: str = ""):
    tree_end = "└── "
    tree_left = "│   "
    tree_right = "├── "
    tree_space = "    "
    print(f"{Fore.BLUE}{tree.pop(0)}")
    for index, item in enumerate(tree, 1):
        if index == len(tree):
            print(f"{Fore.WHITE}{decor_prefix}{tree_end}", end='')
            decor_plus = tree_space
        else:
            print(f"{Fore.WHITE}{decor_prefix}{tree_right}", end='')
            decor_plus = tree_left

        if isinstance(item, list) and len(item) == 1:
            print(f"{Fore.BLUE}{item[0]}")
        elif isinstance(item, list):
            print_tree(item, decor_prefix + decor_plus)
        else:
            print(f"{Fore.GREEN}{item}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prints the directory structure as a tree with a given level")
    parser.add_argument("-L", "--level", type=int, default=1, help="Level to display")
    parser.add_argument("directory", type=str, default=os.getcwd(), help="Path to the directory")
    args = parser.parse_args()
    tree, directories_count, files_count = scan_directory(args.directory, args.level)
    init()
    print_tree(tree)
    print(f"\n{Fore.WHITE}Found {directories_count} directories and {files_count} files")