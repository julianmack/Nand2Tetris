#Token Types:
SYMBOL = "symbol"
KEYWORD = "keyword"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"

statementTypes = ["let", "if", "while", "do", "return"]

#vm_translation of operators
operators = {"+": "add", "-": "sub", "*": None, \
            "/": None, "&": "and", "|": "or", \
            "<": "lt", ">": "gt", "=": "eq"}

unaryOperators = {"-": "neg", "~": "not"}
keywordConstants = ["true", "false", "null", "this"]


#Symbol Table keywords
KIND = "kind"
TYPE = "type"
INDEX = "index"
SCOPE = "scope"


#Memory (and variable) Types
CONSTANT = "constant"
STATIC = "static"
FIELD  = "field" #this is not a hack memory segment
ARG    = "argument"
LCL    = "local"
THIS   = "this"
THAT   = "that"
POINTER = "pointer"
TEMP = "temp"

CLASS  = "class"
SUBROUTINE = "subroutine"
