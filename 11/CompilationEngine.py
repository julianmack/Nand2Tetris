#Token Types:
SYMBOL = "symbol"
KEYWORD = "keyword"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"

#Identifier Types
STATIC = "static"
FIELD  = "field"
ARG    = "argument"
LCL    = "local"
THIS   = "this"
THAT   = "that"
CLASS  = "class"
SUBROUTINE = "subroutine"

statementTypes = ["let", "if", "while", "do", "return"]
#vm_translation of operators
operators = {"+": "add", "-": "sub", "*": None, \
            "/": None, "&": "and", "|": "or", \
            "<": "lt", ">": "gt", "=": "eq"}

unaryOperators = {"-": "neg", "~": "not"}
keywordConstants = ["true", "false", "null", "this"]
import sys

from helpers import prettify
from SymbolTable import SymbolTable
from VMWriter import VMWriter
from Token import Token

class CompilationEngine():
    def __init__(self, tokens, fp_out):
        self.tokens = tokens
        self.num = 0  #current node in tree
        self.total = len(tokens)
        self.crnt_elem = self.tokens[0]
        self.symbols = SymbolTable()#create symbol table(s)
        #possibly should call compileclass from outside
        self.VM = VMWriter(fp_out)
        self.labels = {} #to create unique labels

    def compileClass(self):
        """Class Grammar:
        class className { classVarDec* subroutineDec* }"""

        self.check_next(KEYWORD, "class")
        class_name = self.get()  #classname tkn
        self.className = class_name.text
        self.check_next(SYMBOL, "{")
        while self.check_texts(KEYWORD, ["static", "field"]):
            self.compileClassVarDec()
        while self.check_texts(KEYWORD, ["constructor", "function", "method"]):
            self.compileSubroutineDec()
        self.check_next(SYMBOL, "}")
        self.VM.close()

    def compileClassVarDec(self):
        """ClassVarDec Grammar:
        (static|field) type VarName ("," VarName)* ";" """
        kind_t, type_t, name_t= self.get_mult(3)
        self.symbols.define(name_t.text, type_t.text, kind_t.text)
        while self.check_texts(SYMBOL, ",", True): #another VarName
            name_t = self.get() #VarName
            self.symbols.define(name_t.text, type_t.text, kind_t.text)
        self.check_next(SYMBOL, ";") #end-VarDec


    def compileSubroutineDec(self):
        """SubroutineDec Grammar:
        (constructor|function|method) ("void"| type)
        subroutineName "(" ParameterList ")" SubroutineBody """
        self.symbols.startSubroutine() #wipe previous sub_vars from Symbol Table
        sub_type, ret_type, sub_name, _ = self.get_mult(4)
        if sub_type.text == "method":
            self.symbols.define(THIS, self.className, ARG)
        self.compileParameterList()
        self.check_next(SYMBOL, ")")
        self.compileSubroutineBody()
        self.symbols.startSubroutine() #wipe vars from Symbol Table

    def compileParameterList(self):
        """ParameterList Grammar:
        (type varName) ("," type varName)
         """
        if self.check_texts(KEYWORD):  #if parameter present
            type, name = self.get_mult(2)
            self.symbols.define(name.text, type.text, ARG)
        while self.check_texts(SYMBOL, ",", True): #another VarName
            type, name = self.get_mult(2)
            self.symbols.define(name.text, type.text, ARG)

    def compileSubroutineBody(self):
        """subroutineBody Grammar:
        "{" varDec* statements "}""""
        self.check_next(SYMBOL, "{")
        while self.check_texts(KEYWORD, "var", True): #check for VarDec
            self.compileVarDec()
        self.compileStatements()
        self.check_next(SYMBOL, "}")

    def compileVarDec(self):
        """ Grammar:
        "var" type varName ("," varName)* ";" """
        type, name = self.get_mult(2)
        self.symbols.define(name.text, type.text, LCL)
        while self.check_texts(SYMBOL, ",", True): #another VarName
            name = self.get()
            self.symbols.define(name.text, type.text, LCL)
        self.check_next(SYMBOL, ";")

    def compileStatements(self):
        """ Grammar:
        let|if|while|do|return
        """
        while self.check_texts(KEYWORD, statementTypes):
            type = self.get().text
            if type == "let":           self.compileLet()
            elif type == "if":          self.compileIf()
            elif type == "while":       self.compileWhile()
            elif type == "do":          self.compileDo()        #restore parent node
            elif type == "return":      self.compileReturn()
            else:                       self.fault()

    def compileLet(self):
        """ Grammar: e.g: let x = 4
        "let" varName ("[" expression "]")?
        "=" expression ";" """
        varName = self.get().text
        type, kind, index = self.symbols.get(varName)
        if self.check_texts(SYMBOL, "[", True): #Array
            self.compileExpression()
            self.check_next(SYMBOL, "]")
        #TODO - deal with Array
        self.check_next(SYMBOL, "=")
        self.compileExpression()
        self.check_next(SYMBOL, ";")
        #add to variable:
        self.VM.writePop(kind, index)

    def compileIf(self):
        """ Grammar:
        "if" "(" expression ")" "{" statements"}"
        ("else"  "{" statements"}" )? """
        label_1 = "L1.{}".format(self.get_label(1))
        label_2 = "L2.{}".format(self.get_label(2))
        self.check_next(SYMBOL, "(")
        self.compileExpression()
        self.VM.writeArithmetic("not")
        self.VM.writeIf(label_1)
        self.get_mult(2)            #")" "{"
        self.compileStatements()
        self.get()
        self.VM.writeGoto(label_2)                 #"}"
        self.VM.writeLabel(label_1)
        if self.check_texts(KEYWORD, "else", True): #nested expression
            self.check_next(SYMBOL, "{")
            self.compileStatements()
            self.check_next(SYMBOL, "}")
        self.VM.writeLabel(label_2)

    def compileWhile(self):
        """ Grammar:
        "while" "(" expression ")" "{" statements"}" """
        label_3 = "L3.{}".format(self.get_label(3))
        label_4 = "L4.{}".format(self.get_label(4))
        self.check_next(SYMBOL, "(")
        self.VM.writeLabel(label_4)
        self.compileExpression()
        self.VM.writeArithmetic("not")
        self.VM.writeIf(label_3)
        self.get_mult(2)
        self.compileStatements()
        self.VM.writeGoto(label_4)
        self.check_next(SYMBOL, "}")
        self.VM.writeLabel(label_3)

    def compileDo(self):
        """ Grammar:
        "do" subroutineCall ";" """
        #TODO - work out what this statement is for
        self.compileTerm()
        self.check_next(SYMBOL, ";")

    def compileReturn(self):
        """ Grammar:
        "return" expression? ";" """
        if not self.check_texts(SYMBOL, ";"):
            self.compileExpression()
        self.check_next(SYMBOL, ";")
        #TODO - push const 0 if there is no expression

    def compileExpression(self):
        """ Grammar:
        term (op term)* """
        self.compileTerm()
        if self.check_texts(SYMBOL, operators): #op present
            operator = self.get().text
            op_vm = operators[operator]
            if op_vm:
                self.compileTerm()
                self.VM.writeArithmetic(op_vm)
            elif operator == "*":
                self.VM.writeCall("Math.multiply", 2)
            elif operator == "/":
                self.VM.writeCall("Math.divide", 2)

    def compileTerm(self):
        """Grammar:
        integerConstant | stringConstant | keywordConstant |
        varName | varname "[" expression "]" |
        subroutineCall | "(" expression ")" |
        unaryOp term

        subroutineCall Grammar:
        subroutineName "(" expressionList ")" |
        (className|varName) "." subroutineName
        "(" expressionList ")"
        """
        tkn = self.get(False) #don't increment
        tag = tkn.tag
        #debug:
        #print("before: ", tkn.tag, tkn.text)
        if tag == INT_CONST: #integerConstant
            int = self.get().text
            self.VM.writePush("constant", int)
        elif tag == STRING_CONST: #stringConstant
            string = self.get().text
            self.VM.writePush("constant", len(string))
            self.VM.writeCall("String.new", 1)
            for char in string:
                self.VM.writePush("constant", ord(char))
                self.VM.writeCall("String.appendChar", 2)
        elif self.check_texts(KEYWORD, keywordConstants): #keywordConstant
            keyword = self.get().text
            if keyword == "false" or keyword == "null":
                self.VM.writePush("constant", 0)
            elif keyword == "true":
                self.VM.writePush("constant", 1)
                self.VM.writeArithmetic("neg")
            elif keyword == "void":
                #TODO - must set flag?
                #need to pop returned value
        elif self.check_texts(SYMBOL, unaryOperators): #unaryOp
            un_op = self.get().text
            un_op_vm = unaryOperators[un_op]
            self.compileTerm()
            self.VM.writeArithmetic(un_op_vm)
        elif self.check_texts(SYMBOL, "(", True): # "(" expression ")"
            self.compileExpression()
            self.check_next(SYMBOL, ")")
        elif self.check_texts(IDENTIFIER):
            identifier = self.get().text
            if self.check_texts(SYMBOL, "[", True):
                #ARRAY: varname "[" expression "]"
                self.compileExpression()
                self.check_next(SYMBOL, "]")
                #TODO
            elif self.check_texts(SYMBOL, "(", True):
                #FUNCTION_CALL: subroutineName "(" expressionList ")"
                self.compileExpressionList()
                self.check_next(SYMBOL, ")")
                #TODO
                #determine number of arguments nArgs and then:
                self.VM.writeCall(identifier, nArgs)
            elif self.check_texts(SYMBOL, ".", True):
                #METHOD CALL: (className|varName) "." subroutineName"(" expressionList ")"
                #TODO - push THIS onto stack. (i.e. identifier is obj)
                sub_name = self.get() #subroutineName
                self.check_next(SYMBOL, "(")
                self.compileExpressionList()
                self.check_next(SYMBOL, ")")
                #TODO - call the method
            else: #variable
                type, kind, index = self.VM.get(identifier)
                self.VM.writePush(kind, index)
        else:
            #print("after: ", tkn.tag, tkn.text)
            self.fault()

    def compileExpressionList(self):
        """Grammar:
        (expression ("," expression)* )?
        """
        if not self.check_texts(SYMBOL, ")"):
            self.compileExpression()
        while self.check_texts(SYMBOL, ",", True):
            self.compileExpression()

    def check_texts(self, tag, texts=None, increment=False):
        """ONLY INCREMENTS IF TRUE"""
        tkn = self.get(False)
        if tkn is not None:
            text = tkn.text
            if tkn.tag == tag: #texts could be array of strings or string
                if (not texts) or \
                    (type(texts) is str and text == texts) or \
                    (type(texts) is list and text in texts):
                    if increment:
                        self.num +=1
                    return True
        return False

    def check_next(self, tag, texts=None, increment=True):
        """get next token and checks that it has correct text
        and tag.
        Set increment =false when you would like to check next
        value w/o updating current tkn. This is useful when
        you aren't sure what next routine is"""

        tkn = self.get(increment)
        text = tkn.text
        #print(tag, tkn.tag, tkn.text)
        if tkn.tag == tag: #texts could be array of strings or string
            if (not texts) or \
                (type(texts) is str and text == texts) or \
                (type(texts) is list and text in texts):
                return tkn
        else:
            print("Invalid program (or end of program)")
            print(tkn.tag, tkn.text)
            self.quit()


    def get(self, increment = True):
        """returns next token"""
        if self.num < self.total:
            tkn = self.tokens[self.num]
            self.tkn = tkn
            if increment:
                self.num +=1
            #debug:
            #print(tkn.tag, tkn.text)
            return tkn
        else:
            return None

    def get_mult(self, n):
        tkns = []
        for i in range(n):
            tkns.append(self.get())
        return tkns

    def fault(self):
        """called if incorrect program provided
        make this error message more expressive"""
        print("Invalid program. Quitting...")
        #close any open files
        sys.exit(1)

    def quit(self):
        print("quiting...")
        sys.exit(1)

    def get_label(self, key):
        """Accesses value from dictionary.
        Creates entry if none exists"""
        try:
            val = self.labels[key]
            self.labels[key] = val + 1
        except KeyError:
            #create entry
            val = 0
            self.labels[key] = 1
        return val



if __name__ == "__main__":
    #tests
    pass
