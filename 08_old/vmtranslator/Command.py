#!/bin/env python3
import sys
import command_types
from ramloc import ram_ptr_locs
from helpers import remove_comment
from Arithmetic import Arithmetic, Add, Subtract, Negate, Equal, GreaterThan, LessThan, And, Or, Not

#GLOBAL VARS:
command_map = ["push", "pop", "add", "sub",
                "neg", "eq", "gt", "lt",
                "and", "or", "not", "goto",
                "if-goto", "label", "call",
                "function", "return", "initialise"]
call_label = 0 #global counter to keep call labels separate
current_fn = None #keep track of current function

class Write():
    def __init__(self, program, path_out, file_name):
        with open(path_out, 'w') as f:
            for line in program:
                #create object of correct type:
                global current_fn
                command = TypeAnalyser(line, file_name, current_fn).generate()
                if command: #no command returned if line is comment (or illegal)
                    #every type has method translate() and will return .asm str:
                    asm_output = command.translate() #returns string
                    #write comment to file:
                    f.write("// {}\n".format(line))
                    #write code_line to file:
                    f.write("{}".format(asm_output))

class TypeAnalyser():
    """USAGE: this is passed a command (and file name)
    and when instance.generate() is called, it will return
    a object which is a subclass of Command.
    """
    def __init__(self, command, filename, function_name):
        self.filename = filename
        self.function_name = function_name
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
        elif type == "goto":
            return GoTo(self.args[1], self.filename, self.function_name)
        elif type == "if-goto":
            return IfGoTo(self.args[1], self.filename, self.function_name)
        elif type == "label":
            return Label(self.args[1], self.filename, self.function_name)
        elif type == "call":
            return Call(self.args, self.filename, self.function_name)
        elif type == "function":
            return Function(self.args, self.filename)
        elif type == "return":
            return Return(self.filename, self.function_name)
        elif type == "initialise":
            return Init(self.filename)
        else: #no valid type - includes comment lines
            return None

class Branching(Arithmetic):
    def __init__(self, filename, function_name, label):
        self.label = "{}.{}${}".format(filename, function_name, label)

class Label(Branching):
    def translate(self):
        return "({})\n".format(self.label)

class GoTo(Branching):
    def translate(self):
        return "@{}\n0;JMP\n".format(self.label)

class IfGoTo(Branching):
    def translate(self):
        return "{}A=M\nD=M\n@{}\nD;JGT\n".format(self.sp_dec, self.label)

class Fn():
    """To hold common methods"""
    def use_vm_command(self, phrase, file_name=None, fn_name=None):
        if not file_name:
            file_name = self.file_name
        if not fn_name:
            fn_name = self.function_name
        return TypeAnalyser(phrase, file_name, fn_name).generate().translate()


class Call(Fn):
    def __init__(self, args, file, fn_name):
        self.n_args = int(args[2])
        self.current_fn_name = fn_name
        self.function_name = args[1]
        self.file_name = file
        global call_label  #access global counter to increment
        self.label_count = call_label
        call_label +=1
        self.ret_label = "{}.{}$ret.{}".format(file, self.current_fn_name, self.label_count)

    def translate(self):
        #will join these:
        commands = [self.__push_return_address(),
        self.__push_stack("LCL"),
        self.__push_stack("ARG"),
        self.__push_stack("THIS"),
        self.__push_stack("THAT"),
        self.__set_new_ARG(),
        self.__set_new_LCL(),
        #goto the new function:
        self.__goto_new_fn(),
        #give label as return address:
        self.__declare_return_address()]
        return "".join(commands)

    def __push_return_address(self):
        return  "//push return address to stack\n@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(self.ret_label)

    def __push_stack(self, address):
        return  "//push {} to stack\n@{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(address, address)

    def __set_new_ARG(self):
        return "//set new ARG\n@SP\nD=M\n@5\nD=D-A\n@{}\nD=D-A\n@ARG\nM=D\n".format(self.n_args)

    def __set_new_LCL(self):
        return "//Set New LCL\n@SP\nD=M\n@LCL\nM=D\n"

    def __goto_new_fn(self):
        return "@{}.{}\n0;JMP\n".format(self.file_name, self.function_name)

    def __declare_return_address(self):
        return "({})\n".format(self.ret_label)

class Function(Fn):
    def __init__(self, args, file):
        self.n_vars = int(args[2])
        self.function_name = args[1]
        self.file_name = file
        global current_fn
        current_fn = self.function_name

    def translate(self):
        commands = ["({}.{})\n".format(self.file_name, self.function_name),
        self.__push_0_n_times(self.n_vars)]
        return "".join(commands)

    def __push_0_n_times(self, n):
        ans = []
        for i in range(n):
            ans.append(self.use_vm_command("push constant 0"))
        return "".join(ans)

class Return(Fn):
    def __init__(self, filename, fn_name):
        self.file_name = filename
        self.function_name = fn_name
        #decrement call_label
        global call_label  #access global counter to increment
        call_label -=1

    def translate(self):
        commands = [self.__end_frame(),
        self.__get_ret_Address(),
        self.use_vm_command("pop argument 0"),
        self.__reset_SP(),
        self.__restore_value("THAT", 1),
        self.__restore_value("THIS", 2),
        self.__restore_value("ARG", 3),
        self.__restore_value("LCL", 4),
        self.__goto_return_address()]
        return "".join(commands)
    def __end_frame(self):
        return  "//save endframe in temp variable\n@LCL\nD=M\n@endFrame\nM=D\n"

    def __get_ret_Address(self):
        return  "//get return address\n@5\nD=A\n@endFrame\nD=M-D\nA=D\nD=M\n@retAddr\nM=D\n"

    def __restore_value(self, loc, n):
        return "//restore {}\n@endFrame\nD=M\n@{}\nA=D-A\nD=M\n@{}\nM=D\n".format(loc, n, loc)

    def __reset_SP(self):
        return "//reset SP\n@1\nD=A\n@ARG\nD=D+M\n@SP\nM=D\n"

    def __goto_return_address(self):
        return "@retAddr\nA=M\n0;JMP\n"

class Init(Fn):
    def __init__(self, file_name):
        self.file_name = file_name
        self.function_name = "sys.init"
    def translate(self):
        first = "@256\nD=A\n@SP\nM=D\n"
        second = self.use_vm_command("call sys.init 0")
        return "{}{}".format(first, second)

class PushOrPop():
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
            return self.__translate_push(self.ptr)
        elif self.type == "pop":
            return self.__translate_pop(self.ptr)
        else:
            print ("must provide type push or pop")
            sys.exit(1)


    def __translate_push(self, ptr):
        ram_loc = self.ram_loc
        if ptr: #have to access memory - THIS, THAT, arg, local
            str = "@{}\nD=M\n@{}\nA=D+A\nD=M\n".format(ram_loc, self.loc)
        elif ram_loc: #static,temp, pointer
            str = "@{}\nD=M\n".format(ram_loc)
        else: #accessing constant
            str = "@{}\nD=A\n".format(self.loc)
        return "{}@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str)


    def __translate_pop(self,ptr):
        ram_loc = self.ram_loc
        if ptr: #have to access memory - pointer, THIS, THAT, arg, local
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
