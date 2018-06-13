from Command import TypeAnalyser

class Write():
    def __init__(self, program, path_out, file_name):
        with open(path_out, 'w') as f:
            for line in program:
                #create object of correct type:
                command = TypeAnalyser(line, file_name).generate()
                if command: #no command returned if line is comment (or illegal)
                    #every type has method translate() and will return .asm str:
                    asm_output = command.translate() #returns string
                    #write comment to file:
                    f.write("// {}\n".format(line))
                    #write code_line to file:
                    f.write("{}\n".format(asm_output))
