#Token Types:
SYMBOL = "symbol"
KEYWORD = "keyword"
IDENTIFIER = "identifier"
INT_CONST = "integerConst"
STRING_CONST = "stringConstant"


from helpers import is_alpha, is_symbol, is_numeric, keywords, jack_sample



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
        """
        fst_c = self.__cur_char()
        if fst_c == "\"": #String
            tkn = self.__read_string()
            type = STRING_CONST
        elif is_symbol(fst_c): #Symbol
            tkn = self.__read_sym(fst_c)
            type = SYMBOL
        elif fst_c.isnumeric(): #Int
            tkn = self.__read_int(fst_c)
            type = INT_CONST
        elif is_alpha(fst_c): #Identifier or keyword
            tkn = self.__read_alpha(fst_c)
            if tkn in keywords:
                type = KEYWORD
            else:
                type = IDENTIFIER
        elif fst_c == " " or fst_c == "\n":
            self.crnt_pos += 1
            return None, None
        else:
            pass #invalid char - throw error
        print (self.crnt_pos)
        #print(type)
        return tkn, type

    def __read_sym(self, sym):
        self.crnt_pos += 1
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
        loop = True
        while loop:
            char = self.__cur_char()
            if fn(char):
                tkn = tkn + char
                self.crnt_pos +=1
            else:
                loop = False
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
        return self.data[self.crnt_pos]


    def __remove_comments(self):
        lines = []
        comment = False
        for line in self.file.readlines():
            if comment == True and "\*" in line: #comment ended
                comment = False
            elif "/*" in line: #comment begun
                comment = True
            elif "//" in line: #inline comment
                head, tail = line.split("//", 1)
                lines.append(head.strip())
            else:
                lines.append(line.strip())
        #print ("".join(lines))
        return "".join(lines)


    def hasMoreTokens(self):
        next = self.crnt_pos + 1
        if next <= self.final_pos:
            return True
        else:
            self.file.close()
            return False

if __name__ == "__main__":
    #tests
    def wrap(fn):
        return fn("*")
    print (wrap(lambda x : is_numeric(x) or is_alpha(x)))


    tokenizer = JackTokenizer("arraytest/main.jack")
    tokenizer.data = jack_sample
    tokenizer.final_pos = len(jack_sample)
    print (tokenizer.read_alpha("c"))
