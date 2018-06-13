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
