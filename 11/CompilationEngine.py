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
VAR    = "var"
THIS   = "this"
THAT   = "that"
CLASS  = "class"
SUBROUTINE = "subroutine"


statementTypes = ["let", "if", "while", "do", "return"]
operators = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
unaryOperators = ["-", "~"]
keywordConstants = ["true", "false", "null", "this"]
from lxml import etree

import sys

from helpers import prettify
from SymbolTable import SymbolTable

class CompilationEngine():
    def __init__(self, fp_in, fp_out):
        tree = etree.parse(fp_in)
        self.tokens = tree.getroot()
        self.num = 0  #current node in tree
        self.total = len(self.tokens)
        self.out_root = etree.Element("class") # root for output
        self.crnt_elem = self.out_root
        self.symClass = SymbolTable()#create class symbol table
        self.symSub   = SymbolTable()#create subroutine symbol table
        self.compileClass()
        self.__write_file(fp_out)


    def compileClass(self):
        """Class Grammar:
        class className { classVarDec* subroutineDec* }"""
        #add each tkn in turn whilst checking
        #to see if program is valid

        self.check_and_add(KEYWORD, "class")
        class_name = self.get()  #classname
        self.className = class_name.text
        self.addToXmlTree(class_name)
        self.check_and_add(SYMBOL, "{")
        while self.check_texts(KEYWORD, ["static", "field"]):
            self.compileClassVarDec()
        while self.check_texts(KEYWORD, ["constructor", "function", "method"]):
            self.compileSubroutineDec()
        self.check_and_add(SYMBOL, "}")
        print("class: ")
        self.symClass.print_table()

    def compileClassVarDec(self):
        """ClassVarDec Grammar:
        (static|field) type VarName ("," VarName)* ";" """
        self.addXMLSubElem("classVarDec")
        kind_t, type_t, name_t= self.get_mult(3)
        self.symClass.define(name_t.text, type_t.text, kind_t.text)
        self.addMultXML([kind_t, type_t, name_t])
        while self.check_texts(SYMBOL, ","): #another VarName
            comma, name_t = self.get_mult(2)
            self.symClass.define(name_t.text, type_t.text, kind_t.text)
            self.addMultXML([comma, name_t])
        self.check_and_add(SYMBOL, ";") #end-VarDec
        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()


    def compileSubroutineDec(self):
        """ClassVarDec Grammar:
        (constructor|function|method)
        ("void"| type) subroutineName
        "(" ParameterList ")" SubroutineBody """
        self.addXMLSubElem("subroutineDec")
        self.symSub.startSubroutine() #wipe previous sub_vars from Symbol Table
        tkns = self.get_mult(4)  #constructor|function|method
        [sub_type, ret_type, sub_name, parenth] = tkns
        if sub_type.text == "method":
            self.symSub.define(THIS, self.className, ARG)
        self.addMultXML(tkns)
        self.compileParameterList()
        self.check_and_add(SYMBOL, ")") #leave this
        self.compileSubroutineBody()
        print("sub: ")
        self.symSub.print_table()
        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()

    def compileParameterList(self):
        """ParameterList Grammar:
        (type varName) ("," type varName)
         """
        self.addXMLSubElem("parameterList")

        if self.check_texts(KEYWORD):  #if parameter present
            type, name = self.get_mult(2)
            self.symSub.define(name.text, type.text, ARG)
            self.addMultXML([type, name]) #varname
        while self.check_texts(SYMBOL, ","): #another VarName
            comma, type, name = self.get_mult(3)
            self.symSub.define(name.text, type.text, ARG)
            self.addMultXML([comma, type, name]) #varname

        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()

    def compileSubroutineBody(self):
        """subroutineBody Grammar:
        "{" varDec* statements "}"
        "(" ParameterList ")" SubroutineBody """
        self.addXMLSubElem("subroutineBody")
        self.check_and_add(SYMBOL, "{")
        while self.check_texts(KEYWORD, "var"): #check for VarDec
            self.compileVarDec()
        self.compileStatements()
        self.check_and_add(SYMBOL, "}")

        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()

    def compileVarDec(self):
        """ Grammar:
        "var" type varName ("," varName)* ";" """
        self.addXMLSubElem("varDec")
        self.check_and_add(KEYWORD, "var")
        type, name = self.get_mult(2)
        self.symSub.define(name.text, type.text, VAR)
        self.addMultXML([type, name])
        while self.check_texts(SYMBOL, ","): #another VarName
            comma, name = self.get_mult(2)
            self.symSub.define(name.text, type.text, VAR)
            self.addMultXML([comma, name])
        self.check_and_add(SYMBOL, ";")
        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()

    def compileStatements(self):
        """ Grammar:
        let|if|while|do|return
        """
        self.addXMLSubElem("statements")
        tkn = self.get(False)
        while self.check_texts(KEYWORD, statementTypes):
            tkn = self.get(False)
            type = tkn.text
            if type == "let":
                self.compileLet()
            elif type == "if":
                self.compileIf()
            elif type == "while":
                self.compileWhile()
            elif type == "do":
                self.compileDo()        #restore parent node
            elif type == "return":
                self.compileReturn()
            else:
                self.fault()
        self.crnt_elem = self.crnt_elem.getparent()

    def compileLet(self):
        """ Grammar:
        "let" varName ("[" expression "]")?
        "=" expression ";" """
        self.addXMLSubElem("letStatement")
        self.addToXmlTree(self.get()) #let
        self.check_and_add(IDENTIFIER) #varName
        #kind=KindOf(varName)
        #index = indexOf(varName)
        #use these for vmLet()
        if self.check_texts(SYMBOL, "["): #nested expression
            self.addToXmlTree(self.get())  #"["
            self.compileExpression()
            self.check_and_add(SYMBOL, "]")
        self.check_and_add(SYMBOL, "=")
        self.compileExpression()
        self.check_and_add(SYMBOL, ";")
        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()
    def compileIf(self):
        """ Grammar:
        "if" "(" expression ")" "{" statements"}"
        ("else"  "{" statements"}" )? """
        self.addXMLSubElem("ifStatement")
        self.addToXmlTree(self.get()) #if
        self.check_and_add(SYMBOL, "(")
        self.compileExpression()
        self.check_and_add(SYMBOL, ")")
        self.check_and_add(SYMBOL, "{")
        self.compileStatements()
        self.check_and_add(SYMBOL, "}")
        if self.check_texts(KEYWORD, "else"): #nested expression
            self.addToXmlTree(self.get())  #"else"
            self.check_and_add(SYMBOL, "{")
            self.compileStatements()
            self.check_and_add(SYMBOL, "}")
        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()

    def compileWhile(self):
        """ Grammar:
        "while" "(" expression ")" "{" statements"}" """
        self.addXMLSubElem("whileStatement")
        self.addToXmlTree(self.get()) #while
        self.check_and_add(SYMBOL, "(")
        self.compileExpression()
        self.check_and_add(SYMBOL, ")")
        self.check_and_add(SYMBOL, "{")
        self.compileStatements()
        self.check_and_add(SYMBOL, "}")
        self.crnt_elem = self.crnt_elem.getparent()

    def compileDo(self):
        """ Grammar:
        "do" subroutineCall ";" """
        self.addXMLSubElem("doStatement")
        self.addToXmlTree(self.get()) #do
        self.compileTerm()
        self.check_and_add(SYMBOL, ";")
        self.crnt_elem = self.crnt_elem.getparent()

    def compileReturn(self):
        """ Grammar:
        "return" expression? ";" """
        self.addXMLSubElem("returnStatement")
        self.addToXmlTree(self.get()) #return
        if not self.check_texts(SYMBOL, ";"):
            self.compileExpression()
        self.check_and_add(SYMBOL, ";")
        self.crnt_elem = self.crnt_elem.getparent()

    def compileExpression(self):
        """ Grammar:
        term (op term)* """
        self.addXMLSubElem("expression")
        self.compileTerm()
        if self.check_texts(SYMBOL, operators): #op present
            self.addToXmlTree(self.get())
            self.compileTerm()
        self.crnt_elem = self.crnt_elem.getparent()

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
        self.addXMLSubElem("term")
        tkn = self.get(False) #don't increment
        tag = tkn.tag
        #print("before: ", tkn.tag, tkn.text)
        if tag in [INT_CONST, STRING_CONST]: #integerConstant | stringConstant
            self.addToXmlTree(tkn, True)
        elif self.check_texts(KEYWORD, keywordConstants): #keywordConstant
            self.addToXmlTree(tkn, True)
        elif self.check_texts(SYMBOL, unaryOperators): #unaryOp
            self.addToXmlTree(tkn, True)
            self.compileTerm()
        elif self.check_texts(SYMBOL, "("): # "(" expression ")"
            self.addToXmlTree(tkn, True)
            self.compileExpression()
            self.check_and_add(SYMBOL, ")")
        elif self.check_texts(IDENTIFIER):
            self.addToXmlTree(tkn, True) #i.e. now test next tkn
            if self.check_texts(SYMBOL, "["): #array
                #access info from symbol table
                self.addToXmlTree(self.get()) #varname "[" expression "]"
                self.compileExpression()
                self.check_and_add(SYMBOL, "]")
            elif self.check_texts(SYMBOL, "("): #function call
                self.addToXmlTree(self.get()) #subroutineName "(" expressionList ")"
                self.compileExpressionList()
                self.check_and_add(SYMBOL, ")")
            elif self.check_texts(SYMBOL, "."): #method call
                self.addToXmlTree(self.get())  #(className|varName) "." subroutineName"(" expressionList ")"
                self.check_and_add(IDENTIFIER) #subroutineName
                self.check_and_add(SYMBOL, "(")
                self.compileExpressionList()
                self.check_and_add(SYMBOL, ")")
        else:
            #self.quit()
            #print("after: ", tkn.tag, tkn.text)
            self.fault()
        self.crnt_elem = self.crnt_elem.getparent()

    def compileExpressionList(self):
        """Grammar:
        (expression ("," expression)* )?
        """
        self.addXMLSubElem("expressionList")
        if not self.check_texts(SYMBOL, ")"):
            self.compileExpression()
        while self.check_texts(SYMBOL, ","):
            self.addToXmlTree(self.get())
            self.compileExpression()
        self.crnt_elem = self.crnt_elem.getparent()

    def check_and_add(self, tag, text=None):
        self.addToXmlTree(self.check_next(tag, text))

    def check_texts(self, tag, texts=None, increment=False):
        tkn = self.get(increment)
        if tkn is not None:
            text = tkn.text
            if tkn.tag == tag: #texts could be array of strings or string
                if (not texts) or \
                    (type(texts) is str and text == texts) or \
                    (type(texts) is list and text in texts):
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

    def addToXmlTree(self, tkn, increment=False):
        parent = self.crnt_elem
        child = etree.SubElement(parent, tkn.tag)
        child.text = tkn.text
        if increment:
            self.num +=1
    def addMultXML(self, xs):
        for x in xs:
            self.addToXmlTree(x)
    def addXMLSubElem(self, name):
        """Adds new sub-elem to tree"""
        NewChild = etree.SubElement(self.crnt_elem, name)
        self.crnt_elem = NewChild

    def get(self, increment = True):
        """returns next token"""
        if self.num < self.total:
            tkn = self.tokens[self.num]
            tkn.text = tkn.text.strip()
            self.tkn = tkn
            if increment:
                self.num +=1
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
        print("Invalid program")
        #close any open files
        sys.exit(1)

    def quit(self):
        print(prettify(self.out_root))
        print("quiting...")
        sys.exit(1)

    def __write_file(self, fp_out):
        with open(fp_out, 'w') as f:
            rem = "<?xml version=\"1.0\" ?>"
            out_text = prettify(self.out_root).replace(rem, "")
            f.write(out_text)


if __name__ == "__main__":
    #tests
    compiler = CompilationEngine("../10/square/mainT.xml", "hi")
