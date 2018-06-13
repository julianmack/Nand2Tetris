#!/bin/env python3
import sys
import os


class Parser():
    def __new__(cls, path):
        #create read and write paths
        path_in = os.path.join(sys.path[0], path)
        dir_out, file_name = os.path.split(path_in) #split path to output directory and filename

        #check for legal files or directories
        if os.path.isfile(path_in):
            if not file_name.endswith(".vm"):
                print("Usage: python3 vmtranslator.py path/file.vm\nfile other than 'xxx.vm' provided")
                sys.exit(1)
            else:
                file_name = file_name.replace(".vm", "")  #i.e. remove .vm
                vm_paths = None
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
        else:
            print("Usage: python3 vmtranslator.py path/file.vm\nor...\n\
            Usage: python3 vmtranslator.py path/dir")
            sys.exit(1)

        #create output file path
        path_out_string = "{}/{}.asm".format(dir_out, file_name)
        path_out = os.path.join(sys.path[0], path_out_string)
        #path_out, path_in, vm_paths(=None if it is a file)
        return path_out, path_in, vm_paths
