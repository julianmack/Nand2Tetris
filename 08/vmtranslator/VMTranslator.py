#!/bin/env python3
import sys
import os

from Parser import Parser
from Command import Code_write
"""Usage: python vmtranslator.py path/file.vm
    Output: will produce assembly lan file_name
    of form file.asm in original location
"""
def main():
    #check input args
    if len(sys.argv) != 2:
        print("Usage: python3 vmtranslator.py path/file.vm\nor...\
        \nUsage: python3 vmtranslator.py path/dir")
        sys.exit(1)

    path = sys.argv[1]

    #call parser - returns out_paths - not sure this counts as "parsing"
    path_out, path_in, vm_paths = Parser(path) # vm_paths(=None if it is a single file)

    #write code to file
    Code_write(path_out, path_in, vm_paths)



if __name__ == "__main__":
    main()
