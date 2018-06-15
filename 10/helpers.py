import string

def is_alpha(char):
    """Takes char and returns boolean
    if it is alphanumeric or underscore"""
    if char.isalpha() or char == "_":
        return True
    else:
        return False

def is_symbol(char):
    punct = string.punctuation.translate(
    string.punctuation.maketrans("", "", "@!#$£%^_`:?\'\""))
    return char in punct

def is_numeric(char):
    return char.isnumeric()

keywords = ["class", "constructor", "function",
            "method", "field", "static", "var",
            "int", "char", "boolean", "void",
            "true", "false", "null", "this",
            "let", "do", "if", "else", "while",
            "return"]

jack_sample = "class Main {function void main() {var Array a;"
