"""Usage: python JackAnalyzer.py path/file.vm
    Output: will produce xml parse tree of .jack program
"""

import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 JackAnalyzer.py path/file.jack\nor...\
        \nUsage: python3 JackAnalyzer.py path/dir")
        sys.exit(1)

    path = sys.argv[1]
    path = os.path.join(sys.path[0], path)

    #head is parent directory
    #tail is either directory name or file name
    head, tail = os.path.split(path) #split path to output directory and filename

    #1) if file:
    if os.path.isfile(path):
        if not file_name.endswith(".jack"):
            print("Usage: python3 JackAnalyzer.py path/file.vm\nfile other than 'xxx.jack' provided")
            sys.exit(1)
        else:
            inf_paths = [path]
    #2) if directory:
    elif os.path.isdir(path_in): #directory
        in_files = os.listdir(path)
        jack_files = list(filter(lambda x : ".jack" in x, in_files))
        inf_paths = list(map(lambda x : os.path.join(path, x), jack_files))
    #3) if neither
    else:
        print("Usage: python3 JackAnalyzer.py path/file.jack\nor...\
        \nUsage: python3 JackAnalyzer.py path/dir")
        sys.exit(1)

    #create output file path
     
