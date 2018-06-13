def remove_comment(line):
    """determines if comment present in code line and removes it"""
    if '//' in line:        #comment present
        if line[0:2] != '//':    #inline comment
            [clean_line, comment] = line.split('//', 1) #i.e. 1 so that it only splits at the first
            return clean_line.strip()
        else:
            return '' #full-line comment
    else:
        return line
