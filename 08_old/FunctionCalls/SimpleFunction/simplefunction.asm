// function simplefunction.test 2
(simplefunction.simplefunction.test$simplefunction.simplefunction.test)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 1
@LCL
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1

// not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1

// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1

// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1

// return
//save endframe in temp variable
@LCL
D=M
@endFrame
M=D
//get return address
@5
D=A
@endFrame
D=M-D
A=D
D=M
@retAddr
M=D
@ARG
D=M
@0
D=D+A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
//reset SP
@1
D=A
@ARG
D=D+M
@SP
M=D
//restore THAT
@endFrame
D=M
@1
A=D-A
D=M
@THAT
M=D
//restore THIS
@endFrame
D=M
@2
A=D-A
D=M
@THIS
M=D
//restore ARG
@endFrame
D=M
@3
A=D-A
D=M
@ARG
M=D
//restore LCL
@endFrame
D=M
@4
A=D-A
D=M
@LCL
M=D
@retAddr
A=M
0;JMP

