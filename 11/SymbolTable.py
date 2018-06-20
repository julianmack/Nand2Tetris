#dictionary keywords
KIND = "kind"
TYPE = "type"
INDEX = "index"
SCOPE = "scope"

ARG    = "argument"
LCL    = "local"
STATIC = "static"
FIELD  = "field"
CONSTANT = "constant"

class SymbolTable():
    """Symbols are held in nested dictionary of the form:
    {(var_name): {kind: "...", type: "...", index: "..."}}
    e.g: {x: {kind: "static", type: "int", index: "0"}, ...}
    """
    def __init__(self):
        self.classVars = {}
        self.subVars = {}

    def startSubroutine(self):
        """Wipe all entries from table"""
        self.subVars = {}

    def define(self, name, type, kind):
        index = self.varCount(kind)
        #add to dict - use name as key
        if kind in [STATIC, FIELD]:
            self.classVars[name] = {KIND: kind, TYPE: type, INDEX: index}
            self.print_table(self.classVars)
        elif kind in [ARG, LCL]:
            self.subVars[name] = {KIND: kind, TYPE: type, INDEX: index}
            self.print_table(self.subVars)
    def get(self, name):
        try:
            row = self.symbols[name]
        except KeyError:
            row = None

        if row:
            type = row[TYPE]
            kind = row[KIND]
            index = row[INDEX]
            return type, kind, index
        else:
            return None, None, None

    def varCount(self, kind):
        return self.__lp(kind, self.subVars) + \
                self.__lp(kind, self.classVars)

    def __lp(self, kind, dict):
        count = 0
        for entry in dict.values():
            if entry[KIND] == kind:
                count +=1
        return count

    def KindOf(self, name):
        return self.__search(name, KIND)

    def TypeOf(self, name):
        return self.__search(name, TYPE)

    def IndexOf(self, name):
        return self.__search(name, INDEX)

    def __search(self, name, key):
        try:
            value = self.subVars[name][key]
        except KeyError:
            try:
                value = self.classVars[name][key]
            except KeyError:
                print("{} undefined w. key: {}".format(name, key))
                value = None
        return value


    def print_table(self, dict):
        for key, value in dict.items():
            print(key, ": ", value)
