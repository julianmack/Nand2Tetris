class VMWriter():
    def __init__(self, fp_out):
        self.out = open(fp_out, 'w')
    def close(self):
        self.out.close()
    def writePush(self, seg, index):
        self.out.write("push {} {}\n".format(seg, index))
    def writePop(self, seg, index):
        self.out.write("pop {} {}\n".format(seg, index))
    def writeArithmetic(self, command):
        self.out.write("{}\n".format(command))
    def writeLabel(self, label):
        self.out.write("label {}\n".format(label))
    def writeGoto(self, label):
        self.out.write("goto {}\n".format(label))
    def writeIf(self, label):
        self.out.write("if-goto {}\n".format(label))
    def writeCall(self, name, nArgs):
        self.out.write("call {} {}\n".format(name, nArgs))
    def writeFunction(self, name, nLocals):
        self.out.write("function {} {}\n".format(name, nLocals))
    def writeReturn(self):
        self.out.write("return\n")
    def writeMessage(self):
        self.out.write("debug\n")
