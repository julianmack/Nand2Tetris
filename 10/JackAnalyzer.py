"""Usage: python JackAnalyzer.py path/file.vm
    Output: will produce xml parse tree of .jack program
"""

import sys
import os
from JackTokenizer import JackTokenizer
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 JackAnalyzer.py path/file.jack\nor...\
        \nUsage: python3 JackAnalyzer.py path/dir")
        sys.exit(1)

    #check path is valid
    #and return list of in_path(s)
    in_f_paths = check_path_type()


    #Generate Tokens...
    for fp in in_f_paths:
        #setup outpath:
        token_fp = setup_token_out(fp)
        with open(token_fp, 'w') as f:
            f.write("<tokens>\n")
            #create Tokenizer
            tokenizer = JackTokenizer(fp)
            while tokenizer.hasMoreTokens():
                crnt_tkn, type = tokenizer.advance()
                if crnt_tkn:
                    out_string = "<{}> {} </{}>\n".format(type, crnt_tkn, type)
                    f.write(out_string)
            f.write("</tokens>\n")



def check_path_type():
    path = sys.argv[1]
    path = os.path.join(sys.path[0], path)

    #1) if file:
    if os.path.isfile(path):
        if not path.endswith(".jack"):
            print("Usage: python3 JackAnalyzer.py path/file.vm\nfile other than 'xxx.jack' provided")
            sys.exit(1)
        else:
            in_f_paths = [path]
    #2) if directory:
    elif os.path.isdir(path_in): #directory
        in_files = os.listdir(path)
        jack_files = list(filter(lambda x : ".jack" in x, in_files))
        in_f_paths = list(map(lambda x : os.path.join(path, x), jack_files))
    #3) if neither
    else:
        print("Usage: python3 JackAnalyzer.py path/file.jack\nor...\
        \nUsage: python3 JackAnalyzer.py path/dir")
        sys.exit(1)
    return in_f_paths

def setup_token_out(fp):
    token_out_str = "{}Tokens.xml".format(fp.replace(".jack", ""))
    token_fp = os.path.join(sys.path[0], token_out_str)
    return token_fp

def path_out(path_in):
    #create output file path
    return path_in.replace(".jack", ".xml")

if __name__ == "__main__":
    main()
