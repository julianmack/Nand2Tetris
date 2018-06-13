#!/bin/env python3
import sys
import command_types
from ramloc import ram_ptr_locs

command_map = ["push", "pop", "add", "sub",
                "neg", "eq", "gt", "lt",
                "and", "or", "not"]

class Type():
    def __init__(self, com_obj):
        self.type == com_obj.get_type()

    def determine(self):
        if self.type == "push" or self.type == "pop":
            return PushOrPop(com_obj.command, self.type)
        #other types
        else:
            return None #or raise exception


class Command():
    def __init__(self, command, filename=None):
        self.command = command
        self.type = self.determine_type()

    def determine_type(self):
        args = self.command.split(' ')
        if args[0] in command_map:
            return args[0]
        else:
            return None

    def get_type(self):
        return self.type

    def translate(self): #comments and whitespace will be of class Command
        return self.command #override this in every subclass

    def comment_remove(self): #determines if comment present and removes it
        if '//' in self.command:        #comment present
            if self.command[0:2] != '//':    #inline comment
                [self.command, comment] = line.split('//', 1) #i.e. 1 so that it only splits at the first
                return self.command
            else:
                return None #full-line comment
        else:
            return self.command


class PushOrPop(Command):
    def __init__(self, command, type, filename=None):
        self.command = command
        self.type = type
        #this is unsafe due to multi-space "hi  there". also .strip words
        [com, seg, loc] = command.split(' ')
        self.seg = seg
        self.loc = Command(loc).comment_remove()
        #^invariant: no full_line comments passed to comment_remove() above

    def __find_RAM_loc(self):
        seg = self.seg
        loc = self.loc
        if seg == "constant":
            return None #i.e. no need for address
        elif seg == "static":
            return "{}.vm".format(filename)
        elif seg == "temp":
            return "R{}".format(5 + int(loc))
        elif seg == "pointer":
            return "R{}".format(3 + int(loc))
        elif seg in ram_ptr_locs:
            return ram_ptr_locs[seg]
        else:
            print ("invalid segment provided")
            sys.exit(1)

    def translate(self):
        ram_loc = self.__find_RAM_loc()
        if self.type is "push":
            return self.__translate_push(ram_loc)
        elif self.type is "pop":
            return self.__translate_pop(ram_loc)
        else:
            raise "must provide type push or pop"


    def __translate_push(self,ram_loc):
        if ram_loc:
            str = "@{}\nD=M".format(ram_loc)
        else: #accessing constant
            str = "@{}\nD=A".format(self.loc)
            return "{}@SP\nA=M\nM=D\n@SP\nM=M+1".format(str)


    def __translate_pop(self, ram_loc):
        if ram_loc:
            return "@SP\nM=M-1\nA=M\nD=M\n@{}\nM=D".format(ram_loc)
        else: #accessing constant
            print ("can't 'pop' a constant")
            sys.exit(1)




x = PushOrPop("push constant 6", "push").translate()
y = PushOrPop("push static 2", "push").translate()
z = PushOrPop("pop temp 2", "pop").translate()
#p = PushOrPop("pop constant 2", "pop").translate()

print(x)
print("")
print(y)
print("")
print(z)
#print(p)

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
