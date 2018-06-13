#!/bin/env python3
import sys
import os

from Command import TypeAnalyser
"""Usage: python vmtranslator.py path/file.vm
    Output: will produce assembly lan file_name
    of form file.asm in original location
"""
def main():
    #check input args
    if len(sys.argv) != 2:
        print("Usage: python3 vmtranslator.py path/file.vm")
        sys.exit(1)

    #file path
    file_path = sys.argv[1]
    if not file_path.endswith(".vm"):
        print("Usage: python3 vmtranslator.py path/file.vm\n'.vm' file not provided")
        sys.exit(1)

    #create read and write paths
    path_in = os.path.join(sys.path[0], file_path)

    #create output file path
    path_array = file_path.split('/')
    file_name = path_array.pop().replace(".vm", "")  #i.e. remove file name from path_array
    path_out_string = "{}/{}.asm".format("/".join(path_array), file_name)
    path_out = os.path.join(sys.path[0], path_out_string)

    #open file
    program = [] #varible to store .vm program
    with open(path_in, 'r') as f:
        for line in f:
            program.append(line.strip().lower())

    with open(path_out, 'w') as f:
        for line in program:
            #create object of correct type:
            command = TypeAnalyser(line, file_name).generate()
            if command: #no command returned if line is comment (or illegal)
                #every type has method translate() and will return .asm str:
                asm_output = command.translate() #returns string
                #write comment to file:
                f.write("// {}\n".format(line))
                #write code_line to file:
                f.write("{}\n".format(asm_output))

if __name__ == "__main__":
    main()
