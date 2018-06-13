import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 JackAnalyzer.py path/file.jack\nor...\
        \nUsage: python3 JackAnalyzer.py path/dir")
        sys.exit(1)

    path = sys.argv[1]
