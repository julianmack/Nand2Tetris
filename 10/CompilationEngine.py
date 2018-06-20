#Token Types:
SYMBOL = "symbol"
KEYWORD = "keyword"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"

statementTypes = ["let", "if", "while", "do", "return"]
operators = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
unaryOperators = ["-", "~"]
keywordConstants = ["true", "false", "null", "this"]
from lxml import etree

import sys

from helpers import prettify


class CompilationEngine():
    def __init__(self, fp_in, fp_out):
        tree = etree.parse(fp_in)
        self.tokens = tree.getroot()
        self.num = 0  #current node in tree
        self.total = len(self.tokens)
        self.out_root = etree.Element("class") # root for output
        self.crnt_elem = self.out_root
        self.compileClass()
        self.__write_file(fp_out)
        #self.quit()

    def __write_file(self, fp_out):
        with open(fp_out, 'w') as f:
            rem = "<?xml version=\"1.0\" ?>"
            out_text = prettify(self.out_root).replace(rem, "")
            f.write(out_text)


    def compileClass(self):
        """Class Grammar:
        class className { classVarDec* subroutineDec* }"""
        #add each tkn in turn whilst checking
        #to see if program is valid
        self.check_and_add(KEYWORD, "class")
        self.check_and_add(IDENTIFIER)
        self.check_and_add(SYMBOL, "{")
        while self.isVarDecNext():
            self.compileClassVarDec()
        while self.isSubroutineDecNext():
            self.compileSubroutineDec()
        self.check_and_add(SYMBOL, "}")

    def isVarDecNext(self):
        """VarDec begins with "static"|"field" """
        return self.check_texts(KEYWORD, ["static", "field"], False)

    def isSubroutineDecNext(self):
        """Subroutine Declaration begins with one of:
        constructor | function | method """
        return self.check_texts(KEYWORD, ["constructor", "function", "method"], False)

    def compileClassVarDec(self):
        """ClassVarDec Grammar:
        (static|field) type VarName ("," VarName)* ";" """
        self.addXMLSubElem("classVarDec")
        self.addToXmlTree(self.get())   #static|field
        self.addToXmlTree(self.get())   #type
        self.addToXmlTree(self.get())   #VarName
        while self.check_texts(SYMBOL, ","): #another VarName
            self.addToXmlTree(self.get()) # ","
            self.check_and_add(IDENTIFIER) #VarName(s)
        self.check_and_add(SYMBOL, ";") #end-VarDec

        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()

    def compileSubroutineDec(self):
        """SubroutineDec Grammar:
        (constructor|function|method)
        ("void"| type) subroutineName
        "(" ParameterList ")" SubroutineBody """
        self.addXMLSubElem("subroutineDec")

        self.addToXmlTree(self.get())   #constructor|function|method
        self.addToXmlTree(self.get())     #"void"| type
        self.check_and_add(IDENTIFIER)  #subroutineName
        self.check_and_add(SYMBOL, "(")
        self.compileParameterList()
        self.check_and_add(SYMBOL, ")")
        self.compileSubroutineBody()
        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()

    def compileParameterList(self):
        """ParameterList Grammar:
        (type varName) ("," type varName)
        """
        self.addXMLSubElem("parameterList")

        if self.check_texts(KEYWORD):  #if parameter present
            self.addToXmlTree(self.get()) #type
            self.check_and_add(IDENTIFIER) #varname
        while self.check_texts(SYMBOL, ","): #another VarName
            self.check_and_add(SYMBOL, ",")
            self.addToXmlTree(self.get()) #type
            self.check_and_add(IDENTIFIER) #VarName(s)

        #restore parent node
        self.crnt_elem = self.crnt_elem.getparent()

    def compileSubroutineBody(self):
        """subroutineBody Grammar:
        "{" varDec* statements "}"
        """
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
        self.addToXmlTree(self.get()) #type
        self.check_and_add(IDENTIFIER) #varname
        while self.check_texts(SYMBOL, ","): #another VarName
            self.check_and_add(SYMBOL, ",")
            self.check_and_add(IDENTIFIER) #VarName(s)
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
        self.check_and_add(IDENTIFIER) #varname
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
            if self.check_texts(SYMBOL, "["): #varname "[" expression "]"
                self.addToXmlTree(self.get()) #"["
                self.compileExpression()
                self.check_and_add(SYMBOL, "]")
            elif self.check_texts(SYMBOL, "("): #subroutineName "(" expressionList ")"
                self.addToXmlTree(self.get())
                self.compileExpressionList()
                self.check_and_add(SYMBOL, ")")
            elif self.check_texts(SYMBOL, "."): #(className|varName) "." subroutineName"(" expressionList ")"
                self.addToXmlTree(self.get())
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


    def get_2(self):
        """returns next two tokens. With single increment.
        """
        tkn1 = get(True)
        tkn2 = get(False) #i.e. will test this one
        return tkn1, tkn2


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



if __name__ == "__main__":
    #tests
    #compiler = CompilationEngine("arraytest/mainTokens.xml", "hi")
    compiler = CompilationEngine("expressionlessSquare/mainT.xml", "hi")
