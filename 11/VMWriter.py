class VMWriter():
    def __init__(self, fp_out):
        self.out = open(fp_out, 'w')
    def close(self):
        self.out.close()
    def writePush(self, seg, index):
        self.out.write("push {} {}".format(seg, index))
    def writePop(self, seg, index):
        self.out.write("pop {} {}".format(seg, index))
    def writeArithmetic(self, command):
        self.out.write(command)
    def writeLabel(self, label):
        self.out.write("label {}".format(label))
    def writeGoto(self, label):
        self.out.write("goto {}".format(label))
    def writeIf(self, label):
        self.out.write("if-goto {}".format(label))
    def writeCall(self, name, nArgs):
        self.out.write("call {} {}".format(name, nArgs))
    def writeFunction(self, name, nLocals):
        self.out.write("function {} {}".format(name, nLocals))
    def writeReturn(self):
        self.out.write("return")
