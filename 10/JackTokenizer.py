#Token Types:
SYMBOL = "SYMBOL"
KEYWORD = "KEYWORD"
IDENTIFIER = "IDENTIFIER"
INT_CONST = "INT_CONST"
STRING_CONST = "STRING_CONST"


from helpers import is_alpha
from helpers import is_symbol
from helpers import is_numeric

class JackTokenizer():
    def __init__(self, fp):
        self.fp = fp
        self.file = open(fp, 'r')
        self.crnt_pos = 0
        self.data = self.__remove_comments()
        self.crnt_pos = 0 # ptr to current position
        self.final_pos = len(self.data) - 1

    def advance(self):
        """Reads from data one char at at time.
        Finds token and returns it.
        Also returns type of token
        updates self.crnt_tkn to this txt

        NOTE: if it returns self.crnt_tkn_type
         - can change this to "type" as just in fn"""
        fst_c = self.__cur_char()
        if fst_c == "\"": #String
            tkn = self.__read_string()
            self.crnt_tkn_type = STRING_CONST
        elif is_symbol(fst_c): #Symbol
            tkn = self.__read_sym(fst_c)
            self.crnt_tkn_type = SYMBOL
        elif fst_c.isnumeric(): #Int
            tkn = self.__read_int(fst_c)
            self.crnt_tkn_type = INT_CONST
        elif is_alpha(fst_c): #Identifier or keyword
            tkn = self.__read_alpha(fst_c)
            if tkn in keywords:
                self.crnt_tkn_type = KEYWORD
            else:
                self.crnt_tkn_type = IDENTIFIER
        elif fst_c == " " or fst_c == "\n":
            self.crnt_pos += 1
        else:
            pass #invalid char - throw error
        return tkn, self.crnt_tkn_type

    def __read_sym(self, sym):
        if sym == "<":
            return "&lt;"
        elif sym == ">":
            return "&gt;"
        elif sym == "\"":
            return "&quot;"
        elif sym == "&":
            return "&amp;"
        else:
            return sym

    def __read_token(self, first_char, fn):
        tkn = first_char
        self.crnt_pos += 1
        exit = False
        while exit:
            char = self.__cur_char()
            if fn(char):
                tkn.append(char)
                self.crnt_pos +=1
            else:
                exit = True
        return tkn

    def __read_string(self):
        fn = lambda x : x != "\""
        tkn = self.__read_token("", fn)
        self.crnt_pos +=1 # to avoid closing `"`
        return tkn

    def __read_int(self, first_char):
        return self.__read_token(first_char, is_numeric)

    def __read_alpha(self, first_char):
        fn = lambda x : is_numeric(x) or is_alpha(x)
        return self.__read_token(first_char, fn)

    def __cur_char(self):
        return self.data[self.data_pos]


    def __remove_comments(self):
        lines = []
        comment = False
        for line in self.file.readlines():
            if comment == True:
                if "\*" in line: #comment ended
                    comment = False
                else:
                    continue #ignore line
            elif "/*" in line: #comment begun
                comment = True
                continue
            elif "//" in line: #inline comment
                head, tail = line.split("//", 1)
                lines.append(head.strip())
            else:
                lines.append(line.strip())
        return "".join(lines)


    def hasMoreTokens(self):
        next = self.crnt_pos + 1
        if next <= self.final_pos:
            return True
        else:
            self.file.close()
            return False
