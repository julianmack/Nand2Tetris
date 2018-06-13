#!/bin/env python3
import sys
import os

from Command import Write
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

    #create read and write paths
    path = sys.argv[1]
    path_in = os.path.join(sys.path[0], path)
    dir_out, file_name = os.path.split(path_in) #split path to output directory and filename

    #check for legal files or directories
    if os.path.isfile(path_in):
        if not file_name.endswith(".vm"):
            print("Usage: python3 vmtranslator.py path/file.vm\nfile other than 'xxx.vm' provided")
            sys.exit(1)
        else:
            file_name = file_name.replace(".vm", "")  #i.e. remove .vm
            is_directory = False
    elif os.path.isdir(path_in): #directory
        files = os.listdir(path_in)
        vm_files = list(filter(lambda x : ".vm" in x, files))
        """
        #if vm_files doesn't contain Main.vm, terminate:
        if not "Main.vm" in vm_files:
            print("Target directory must include 'Main.vm' file")
            sys.exit(1)"""
        vm_paths = list(map(lambda x : os.path.join(path_in, x), vm_files))
        dir_out = path_in
        is_directory = True
    else:
        print("Usage: python3 vmtranslator.py path/file.vm\nor...\n\
        Usage: python3 vmtranslator.py path/dir")
        sys.exit(1)

    #create output file path
    path_out_string = "{}/{}.asm".format(dir_out, file_name)
    path_out = os.path.join(sys.path[0], path_out_string)

    #open file
    program = [] #variable to store .vm program
    if not is_directory: #i.e. file present
        with open(path_in, 'r') as f:
            for line in f:
                program.append(line.strip().lower())
    else:
        #write_init - initialises file
        program.append("initialise")
        #iterates through every path in vm_paths and write to file
        for fn in vm_paths:
            with open(fn, 'r') as f:
                for line in f:
                    program.append(line.strip().lower())

    Write(program, path_out, file_name)


if __name__ == "__main__":
    main()
