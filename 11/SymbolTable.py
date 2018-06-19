#dictionary keywords
KIND = "kind"
TYPE = "type"
INDEX = "index"
SCOPE = "scope"


class SymbolTable():
    """Symbols are held in nested dictionary of the form:
    {(var_name): {kind: "...", type: "...", index: "..."}}
    e.g: {x: {kind: "static", type: "int", index: "0"}, ...}
    """
    def __init__(self):
        self.symbols = {}

    def define(self, name, type, kind):
        index = self.varCount(kind)
        #add to dict - use name as key
        self.symbols[name] = {KIND: kind, TYPE: type, INDEX: index}

    def varCount(self, kind):
        count = 0
        for entry in self.symbols.values():
            if entry[KIND] == kind:
                count +=1
        return count

    def KindOf(self, name):
        return self.symbols[name][KIND]
    def TypeOf(self, name):
        return self.symbols[name][TYPE]
    def IndexOf(self, name):
        return self.symbols[name][INDEX]

    def startSubroutine(self):
        """Wipe all entries from table"""
        self.symbols = {}

    def print_table(self):
        for key, value in self.symbols.items():
            print(key, ": ", value)
