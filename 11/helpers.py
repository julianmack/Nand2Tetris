import string


"""Should seperate this into
file helpers and string helpers"""

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
    return str(char) in punct

def is_numeric(char):
    return char.isnumeric()

keywords = ["class", "constructor", "function", "method", "field", "static",
"var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
"do", "if", "else", "while", "return"]

jack_sample = "class Main {function void main() {var Array a;"

"""FILE HELPERS:"""
import os
import sys

def change_fp_name(fp, old_str, new_str):
    """Accepts fp and replaces old extension old_str
    with new_str"""
    out_str = fp.replace(old_str, new_str)
    out_fp = os.path.join(sys.path[0], out_str)
    return out_fp

"""XML helpers:"""

from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def remove_special_xml(sym):
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



if __name__ == "__main__":
    #tests
    is_symbol(3)
