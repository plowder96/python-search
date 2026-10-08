# This is a CLI tool for keyword search of .md files in the current directory structure.
# TODO:
# 1) Add option to pass subdirectory as argument - done
# 2) Track total matches and matches per file - done
# 3) Allow for multiple keyword arguments - done
# 3) Show context lines - done
# 4) Update count convention - done
#       Keywords are tracked per word per file.
# 5) And/Or functionality at the line level - open
# 6) Replace grep subprocess with Python - open
# 7) Argparse - open
# 8) Ranking - open
# 9) Markdown-aware search

from pathlib import Path
import sys
import subprocess
import re

# If user passes a mode option, this function determines if mode value is valid and returns.
def determine_mode(option: str) -> str:
    option_map = [
        'and'
    ]
    if option in option_map:
        return option
    else:
        print(f'unknown option detected - {option} - ending script.')
        sys.exit(1)

# parses the command line arguments, detects if argument 1 is an existing path, capture keywords in a list.
# assumes if path exists in commmand line argument, it will always be argument 1.
# TODO: Build logic to determine and return a 'search mode' - and/or at the line level are only modes in current scope.
def parse_args() -> tuple[str,list,str]:
    check_path_mode = Path(sys.argv[1])
    if check_path_mode.is_dir(): # directory passed - set path with it and default mode to 'or'
        print(f'directory found: {check_path_mode}')
        path = check_path_mode
        start_indice = 2
        mode = 'or'
    elif re.search('^--',str(check_path_mode)): # mode option passed - check value and set mode, default path to './' if path not found in arguments
        print('mode option found!')
        path = './'
        start_indice = 2
        mode = determine_mode(str(check_path_mode)[2:])
        if Path(sys.argv[2]).is_dir(): # path was passed after mode
            print('path found as well!')
            path = Path(sys.argv[2])
            start_indice = 3
    else: # only keyword(s) passed - default path to './' and mode to 'or'
        print('No directory or mode option passed - default path to \'./\'')
        path = './'
        start_indice = 1
        mode = 'or'

    keywords = []
    for i in range(start_indice,len(sys.argv)):
        keyword = sys.argv[i]
        keywords.append(keyword)

    return path,keywords,mode

def find_md(path: str) -> str:
    # call bash command to open directory contents,
    # looking for .md files
    output = subprocess.run(['find',path,'-type','f','-name','*.md'],capture_output = True, text = True)
    return output.stdout

# search every line of the find command results for the keyword
# TODO: Refactor to accept a 'search mode' that dictates how keywords are found - and/or at the line level are only modes in current scope.
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
        # Counts per file
        file_has_match = False
        file_keywords_list = list(matches[i].keys())
        # dict for tracking keyword match counts
        keyword_match_count = {}
        
        for j in file_keywords_list:
            
            # Counts per keyword
            lines_context = 0
            
            if not matches[i][j]: # no matches for keyword in file
                continue
            else: # matches found, track counts and display matches
                keyword_match_count[j] = 0 # initialize keyword count
                file_has_match = True
                print(f'----------------------\n{i}:')
                
                for k in matches[i][j]:
                    
                    if k == '--': # skip delimiter lines added by 'grep' but still print line
                        print(k)
                        continue

                    total_lines_returned += 1 # initialized before loop structure
                    
                    if re.search(r'^\d+-',k): # search for regex of grep-returned context line: ##-
                        lines_context += 1
                        print(f'{k}(context)')

                    else:
                        keyword_match_count[j] += 1 # add to keyword count
                        print(k)

            print(f'----------------------\n----------------------\nCounts for file: {i}\n{keyword_match_count[j]} matches found for keyword: {j}')
            print(f'{lines_context} context lines returned\n---------------------------------------------------------------')
    
        if file_has_match: # increment keyword found in file
            files_found += 1
    
    print(f'{total_lines_returned} lines returned across {files_found} files')

def main():
    
    path,keywords = parse_args()
    # files_concatenated = find_md(path)
    # files_split = files_concatenated.splitlines()
    # matches = find_keyword(keywords,files_split)
    # display_matches(matches)

if __name__ == '__main__':
    main()

