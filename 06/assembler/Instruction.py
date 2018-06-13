#!/bin/env python3
from codes import comp_codes
from codes import dest_codes
from codes import jump_codes

class Instruction():
    """Hack language instruction"""

    def __init__(self, instruction):
        self.instruction = instruction

class A(Instruction):
    def __init__(self, instruction, symbol_table, n):
        variable = instruction.replace("@", "")
        if variable.isdigit():
            value = int(variable)
            self.n = False
        else:
            try: # if var in symbols
                value = symbol_table[variable] #then return stored value
                self.n = False
            except KeyError: #else add to symbols
                symbol_table[variable] = n
                value = n
                self.n = n
        self.value = value


    def to_hack(self):
        return '{0:016b}'.format(self.value)


class C(Instruction):
    def __init__(self, instruction):
        #C of form dest=comp;jump

        try: #get dest
            dest, ins = instruction.split('=') #ins2 is rest of instruction
        except ValueError: #i.e. no '=' sign
            dest, ins = 'null', instruction
        try: #get comp
            comp, jump = ins.split(';')
            if jump == '':
                jump = 'null'
        except ValueError: #i.e. no jump present
            comp, jump = ins, 'null'
        self.dest = dest
        self.comp = comp
        self.jump = jump

    def to_hack(self):
        return '111{}{}{}'.format(comp_codes[self.comp],
                                dest_codes[self.dest],
                                jump_codes[self.jump])




"""
#debug:
symbols = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4,
'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9,
'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13,
'R14': 14, 'R15': 15, 'SCREEN': 16384,
'KBD': 24576, 'SP': 0, 'LCL': 1, 'ARG': 2,
'THIS': 3, 'THAT': 4}

v = A("@KBD", symbols)
x = A("@hello", symbols)
y = A("@hello", symbols)
z = A("@9", symbols)
p = A("@harry", symbols)
print(v.value)
print (x.value)
print (y.value)
print(z.value)
print(p.value)
print(symbols)

a= C("AM=M-1").to_hack()
b= C("M=D+1").to_hack()
c = C("0;JMP").to_hack()
print (a, b, c)
"""
