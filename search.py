# This is a CLI tool for keyword search of .md files in the current directory structure.
# TODOs:
# 1) Add option to pass subdirectory as argument - done
# 2) Track total matches and matches per file - in progress
# 3) Allow for multiple keyword arguments - done
# 3) Show context lines
from pathlib import Path
import sys
import subprocess

# print(sys.argv)
# path = sys.argv[1] # expect path as first argument
# keyword = sys.argv[2] # expect keyword as secont argument

# parses the command line arguments, detects if argument 1 is an existing path, capture keywords in a list.
# assumes if path exists in commmand line argument, it will always be argument 1.
def parse_args(check_path: str) -> tuple[str,list]:
    check_path = Path(sys.argv[1])
    if check_path.is_dir():
        path = check_path
        start_indice = 2
    else:
        path = './'
        start_indice = 1

    keywords = []
    for i in range(start_indice,len(sys.argv)):
        keyword = sys.argv[i]
        keywords.append(keyword)

    return path,keywords


def find_md(path: str) -> str:
    # call bash command to open directory contents,
    # looking for .md files
    output = subprocess.run(['find',path,'-type','f','-name','*.md'],capture_output = True, text = True)
    return output.stdout

# search every line of the find command results for the keyword
def find_keyword(keywords: list,files_split: list) -> dict:

    returned_lines_dict = {}
    for i in files_split:
        returned_lines_dict[i] = {} # populate dictionary with top-level filename keys

        for j in keywords:
            search_response = subprocess.run(['grep','-n','-i',j,i],capture_output = True, text = True) # get keyword matches
            returned_lines_dict[i][j] = search_response.stdout.splitlines() # add list of keyword matches to sub-dictionary
    
    return returned_lines_dict

# print the found lines along with match counts to the terminal
# TODO: Update function to support new matches data structure
def display_matches(matches: dict) -> None:
    total_files = len(matches)
    total_matches = 0
    for i in matches:
        split_lines = matches[i].splitlines() # extract each line from the block
        print(f'{i}:')
        for j in split_lines:
            print(j)
        print(f'{len(split_lines)} matches in {i}\n')
        total_matches += len(split_lines)
    print(f'{total_matches} matches found across {total_files} files.')

def main():
    
    check_path = Path(sys.argv[1])
    path,keywords = parse_args(check_path)
    # print(path)
    # print(keywords)
    files_concatenated = find_md(path)
    files_split = files_concatenated.splitlines()
    # print(files_concatenated)
    # print(files_split)
    # print(keywords)
    matches = find_keyword(keywords,files_split)
    # display_matches(matches)

if __name__ == '__main__':
    main()

