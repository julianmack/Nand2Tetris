#!/bin/env python3
import sys
import command_types
from ramloc import ram_ptr_locs
from helpers import remove_comment

command_map = ["push", "pop", "add", "sub",
                "neg", "eq", "gt", "lt",
                "and", "or", "not"]

class TypeAnalyser():
    """USAGE: this is passed a command (and file name)
    and when instance.generate() is called, it will return
    a object which is a subclass of Command.
    """
    def __init__(self, command, filename):
        self.filename = filename
        args = remove_comment(command).split(' ') #split command into constituent parts
        #remove args equal to '':
        parsed_args = list(filter(lambda x : x != '', args))
        self.args = parsed_args
        if len(parsed_args) is 0:
            self.type = None
            return

        #determine type
        if parsed_args[0] in command_map:
            self.type = parsed_args[0]
        else:
            self.type = None

    def generate(self):
        type = self.type
        if type == "push" or type == "pop":
            return PushOrPop(self.args, self.filename)
        elif type == "add":
            return Add()
        elif type == "sub":
            return Subtract()
        elif type == "neg":
            return Negate()
        elif type == "eq":
            return Equal()
        elif type == "gt":
            return GreaterThan()
        elif type == "lt":
            return LessThan()
        elif type == "and":
            return And()
        elif type == "or":
            return Or()
        elif type == "not":
            return Not()
        else: #no valid type - includes comment lines
            return None


class Command():
    """Never create instances of this class
     - just used to hold methods common to all
     subclasses"""

class Arithmetic():
    """Never create instances of this class
     - just used to hold variables common to all
     subclasses"""
    sp_inc = "@SP\nM=M+1\n"
    sp_dec = "@SP\nM=M-1\n"
    sp_acc = "@SP\nA=M\n"

    #get two numbers from stack:
    #store first in D and second in M:
    get_two = "{}A=M\nD=M\n{}A=M\n".format(sp_dec,sp_dec)

    comparison = "{}D=M-D\n".format(get_two)


class Add(Arithmetic):
    def translate(self):
        return "{}M=D+M\n{}".format(self.get_two, self.sp_inc)

class Subtract(Arithmetic):
    def translate(self):
        return "{}M=M-D\n{}".format(self.get_two, self.sp_inc)

class Negate(Arithmetic):
    def translate(self):
        return "{}A=M\nM=-M\n{}".format(self.sp_dec, self.sp_inc)

class Not(Arithmetic):
    def translate(self):
        return "{}A=M\nM=!M\n{}".format(self.sp_dec, self.sp_inc)

class And(Arithmetic):
    def translate(self):
        return "{}M=D&M\n{}".format(self.get_two, self.sp_inc)

class Or(Arithmetic):
    def translate(self):
        return "{}M=D|M\n{}".format(self.get_two, self.sp_inc)

comp_label = 0 #global counter to keep jump labels separate
class Comparison(Arithmetic):
    def __init__(self):
        global comp_label  #access global counter to increment
        comp_label +=1
        self.label_ctr = comp_label
    def comp_trans(self, asm_jump):
        first = "{}@EQTRUE{}\nD;{}\n".format(self.comparison, self.label_ctr, asm_jump)
        false = "{}M=0\n@EQEND{}\n0;JMP\n".format(self.sp_acc, self.label_ctr)
        #note - in hack True = -1:
        true = "(EQTRUE{})\n{}M=-1\n(EQEND{})\n{}".format(self.label_ctr, self.sp_acc, self.label_ctr, self.sp_inc)
        return "{}{}{}".format(first,false,true)

class Equal(Comparison):
    def translate(self):
        return self.comp_trans("JEQ")

class GreaterThan(Comparison):
    def translate(self):
        return self.comp_trans("JGT")

class LessThan(Comparison):
    def translate(self):
        return self.comp_trans("JLT")


class PushOrPop(Command):
    """Usage: instances only created from
    within Typeinstance.generate()"""
    def __init__(self, args, filename=None):
        self.filename = filename
        self.type = args[0]
        self.seg = args[1]
        self.loc = args[2]
        self.ram_loc, self.ptr = self.__find_RAM_loc()


    def __find_RAM_loc(self):
        """Returns memory location and Boolean if it is a pointer"""
        seg = self.seg
        loc = self.loc
        if seg == "constant":
            return None, False #i.e. no need for address
        elif seg == "static":
            return "{}{}".format(self.filename, loc), False
        elif seg == "temp": #returns @R5
            return "R{}".format(5 + int(loc)), False
        elif seg == "pointer":
            return "R{}".format(3 + int(loc)), False
        elif seg in ram_ptr_locs:
            return ram_ptr_locs[seg], True
        else:
            print ("invalid segment provided")
            sys.exit(1)



    def translate(self):
        if self.type == "push":
            return self.__translate_push()
        elif self.type == "pop":
            return self.__translate_pop()
        else:
            print ("must provide type push or pop")
            sys.exit(1)


    def __translate_push(self):
        ram_loc = self.ram_loc
        if self.ptr: #have to access memory - THIS, THAT, arg, local
            str = "@{}\nD=M\n@{}\nA=D+A\nD=M\n".format(ram_loc, self.loc)
        elif ram_loc: #static,temp, pointer
            str = "@{}\nD=M\n".format(ram_loc)
        else: #accessing constant
            str = "@{}\nD=A\n".format(self.loc)
        return "{}@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str)


    def __translate_pop(self):
        ram_loc = self.ram_loc
        if self.ptr: #have to access memory - pointer, THIS, THAT, arg, local
            return "@{}\nD=M\n@{}\nD=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n".format(ram_loc, self.loc)
        elif ram_loc: #static,temp
            return "@SP\nM=M-1\nA=M\nD=M\n@{}\nM=D\n".format(ram_loc)
        else: #pop constant
            print ("can't 'pop' a constant")
            sys.exit(1)


"""
a = Equal().translate()
b = Equal().translate()
print(a)
print(b)


x = PushOrPop(["push", "constant", "12"], "filename").translate()

y = PushOrPop(["push", "temp", "2"], "filename").translate()
##p = PushOrPop("pop constant 2", "pop").translate()

print(x)
print("")
print(y)
print("")
#print(z)
"""

"""
class Pop(Command):
class Arithmetic(Command):
class Add(Arithmetic):
class Sub(Arithmetic):
class Neg(Arithmetic):
class Eq(Arithmetic):
class Gt(Arithmetic):
class Lt(Arithmetic):
class And(Command):
class Or(Command):
class Not(Command):
"""

"""        #first deal with comments
        if '//' in line:    #comment present
            if line[0:2] == '//':    #full-line comment
                return None
            else: #inline
                self.command, comment = self.command.split("//", 1)
                determine_type(self.command)

        #determine type:
        """
