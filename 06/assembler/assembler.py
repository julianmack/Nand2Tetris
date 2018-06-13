#!/bin/env python3
import sys
import os
from Instruction import C
from Instruction import A


"""Usage: python assembler.py path/file.asm
    Output: will produce assembled machine language
    file.hack in original location
"""
def main():
    #check input args
    if len(sys.argv) != 2:
        print("Usage: python3 assembler.py path/file.asm")
        sys.exit(1)

    #file path
    file_path = sys.argv[1]
    if not file_path.endswith(".asm"):
        print("Usage: python3 assembler.py path/file.asm\n'.asm' file not provided")
        sys.exit(1)

    #create read and write paths
    path_in = os.path.join(sys.path[0], file_path) #read

    #create output file path
    path_array = file_path.split('/')
    file_name = path_array.pop().replace(".asm", "")  #i.e. remove file name from path_array
    path_out_string = "{}/{}.hack".format("/".join(path_array), file_name)
    path_out = os.path.join(sys.path[0], path_out_string)

    #open file
    program = [] #varible to store .asm program
    with open(path_in, 'r') as f:
        for line in f:
            program.append(line)

    #initialise symbol_table:
    symbols = {}
    init_symbol_table(symbols)

    #parse program:
    p_program = parse(program) #string array
    #first_pass - remove (LABEL)s and update symbol table:
    sym_rem_prog = first_pass(p_program, symbols)

    #second_pass and output to .hack file
    second_pass(sym_rem_prog, path_out, symbols)



def first_pass(program, symbol_table):
    line_counter = 0
    new_prog = []
    for instruction in program:
        if instruction[0] is '(':
            label = instruction.replace("(", "").replace(")", "")
            symbol_table[label] = line_counter
        else:
            line_counter +=1
            new_prog.append(instruction) #i.e. only add instruction if not a label
    return new_prog

def second_pass(program, out_path, symbol_table):
    """
    Usage: takes legal parsed program with no symbols or labels and outputs to .hack file in Machine language
    Accepts: program string Array
    Assumes: valid asm program fully parsed with no symbols or labels
    """
    with open(out_path, 'w') as f:
        n = 16 #RAM position
        for instruction in program:
            if instruction[0] is "@":
                instr_obj = A(instruction, symbol_table, n)
                if instr_obj.n:  #this will be set to false if n hasn't been incremented
                    n +=1
            else:
                instr_obj = C(instruction)
            code_line = instr_obj.to_hack()
            f.write(code_line + '\n') #write code_line to file



def init_symbol_table(table):
    """Usage: no args required. Returns dict with symbols and values"""

    pre_def = {
        "SCREEN": 16384,
        "KBD": 24576,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4
    }

    for i in range(0,16):
        table["R{}".format(i)] = i

    table.update(pre_def)
    return


def parse(lines):
    """fn: list string-> list string
    removes all whitespace
    removes all .asm comments denoted by '//'
    """
    #helper function
    def remove_comment(line):
        if '//' in line:        #comment present
            if line[0:2] != '//':    #inline comment
                [parsed, comment] = line.split('//', 1) #i.e. 1 so that it only splits at the first
                return parsed
            else:        #full-line comment
                return None
        return line #returns line unchanged if no comment present

    #new function
    parsed_prog = []
    for line in lines:
        #remove " " and "\n" and comments:
        parsed_line = remove_comment(line.replace(" ", "").replace('\n', ""))
        if parsed_line: #i.e. not '' or None
            parsed_prog.append(parsed_line)
    return parsed_prog


if __name__ == "__main__":
    main()
