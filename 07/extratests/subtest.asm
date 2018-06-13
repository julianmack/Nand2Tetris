// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// not
@SP
M=M-1
A=M
D=!M
M=D
@SP
M=M+1

