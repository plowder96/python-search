# This is a CLI tool for keyword search of .md files in the current directory structure.
# TODO:
# 1) Add option to pass subdirectory as argument - done
# 2) Track total matches and matches per file - done
# 3) Allow for multiple keyword arguments - done
# 3) Show context lines - done
# 4) Update count convention - In progress
#       Keywords are tracked per word per file.
from pathlib import Path
import sys
import subprocess

# parses the command line arguments, detects if argument 1 is an existing path, capture keywords in a list.
# assumes if path exists in commmand line argument, it will always be argument 1.
def parse_args() -> tuple[str,list]:
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
            search_response = subprocess.run(['grep','-C1','-n','-i',j,i],capture_output = True, text = True) # get keyword matches
            returned_lines_dict[i][j] = search_response.stdout.splitlines() # add list of keyword matches to sub-dictionary
    
    return returned_lines_dict

# print the found lines along with match counts to the terminal
def display_matches(matches: dict[str, dict[str, list[str]]]) -> None:
    # Counts for all files
    files_found = 0
    total_lines_returned = 0

    for i in matches:
        # Counts per files
        file_matches = 0
        context_lines = 0
        file_lines_returned = 0
        matched_lines = 0
        files_found += 1
        file_keywords_list = list(matches[i].keys())
        keyword_match_count = {}
        for j in file_keywords_list:
            if not matches[i][j]: # no matches for keyword in file
                continue
            else: # matches found, track counts and display matches
                keyword_match_count[j] = 0
                print(f'---------------------------------------------------------------\n{i}:')
                for k in matches[i][j]:
                    print(k) # print all lines returned
                    if k == '--': # skip delimiter lines added by 'grep'
                        continue
                    keyword_match_count[j] += 1
                    print(keyword_match_count)
                    total_lines_returned += 1 # initialized before loop structure
                    
                    if j.lower() in k.lower():
                        file_matches += 1 # initialized at the start of next outermost loop, only increments when line actually contains keyword
                        file_lines_returned += 1
                    else:
                        context_lines += 1
                        file_lines_returned += 1
        matched_lines = file_lines_returned - context_lines
        # files_found += 1

        print(f'{context_lines} context lines returned\n{matched_lines} match lines returned\n')

    print(f'{total_lines_returned} lines returned across {files_found} files')

def main():
    
    path,keywords = parse_args()
    files_concatenated = find_md(path)
    files_split = files_concatenated.splitlines()
    matches = find_keyword(keywords,files_split)
    # print(matches)
    display_matches(matches)

if __name__ == '__main__':
    main()

