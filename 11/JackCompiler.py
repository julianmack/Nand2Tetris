"""Usage: python JackAnalyzer.py path/file.vm
    Output: will produce xml parse tree of .jack program
"""

import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine as Compiler
from helpers import change_fp_name
from Token import Token
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 JackAnalyzer.py path/file.jack\nor...\
        \nUsage: python3 JackAnalyzer.py path/dir")
        sys.exit(1)

    #check path is valid
    #and return list of in_path(s)
    in_f_paths = check_path_type()

    #Generate Tokens...
    token_xml_files = []
    for fp in in_f_paths:
        tokenizer = JackTokenizer(fp)
        tokens = []
        while tokenizer.hasMoreTokens():
            text, tag = tokenizer.advance()
            if tag:
                tokens.append(Token(text, tag))
        #setup outpath:
        out_fp = change_fp_name(fp, ".jack", ".vm")
        compiler = Compiler(tokens, out_fp)
        compiler.compileClass()


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
    elif os.path.isdir(path): #directory
        in_files = os.listdir(path)
        jack_files = list(filter(lambda x : ".jack" in x, in_files))
        in_f_paths = list(map(lambda x : os.path.join(path, x), jack_files))
    #3) if neither
    else:
        print("Usage: python3 JackAnalyzer.py path/file.jack\nor...\
        \nUsage: python3 JackAnalyzer.py path/dir")
        sys.exit(1)
    return in_f_paths




def path_out(path_in):
    #create output file path
    return path_in.replace(".jack", ".xml")

if __name__ == "__main__":
    main()
