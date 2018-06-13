// initialise
@256
D=A
@SP
M=D
//push return address to stack
@nestedcall.sys.init$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL to stack
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//push ARG to stack
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//push THIS to stack
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//push THAT to stack
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
//set new ARG
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
//Set New LCL
@SP
D=M
@LCL
M=D
@nestedcall.sys.init
0;JMP
(nestedcall.sys.init$ret.0)
// function sys.init 0
(nestedcall.sys.init)
// push constant 4000	// test this and that context save
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@R3
M=D
// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@R4
M=D
// call sys.main 0
//push return address to stack
@nestedcall.sys.init$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL to stack
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//push ARG to stack
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//push THIS to stack
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//push THAT to stack
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
//set new ARG
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
//Set New LCL
@SP
D=M
@LCL
M=D
@nestedcall.sys.main
0;JMP
(nestedcall.sys.init$ret.1)
// pop temp 1
@SP
M=M-1
A=M
D=M
@R6
M=D
// label loop
(loop.nestedcall$sys.init)
// goto loop
@loop.nestedcall$sys.init
0;JMP
// function sys.main 5
(nestedcall.sys.main)
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
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@R3
M=D
// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@R4
M=D
// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 1
@LCL
D=M
@1
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
// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 2
@LCL
D=M
@2
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
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 3
@LCL
D=M
@3
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
// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// call sys.add12 1
//push return address to stack
@nestedcall.sys.main$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL to stack
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//push ARG to stack
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//push THIS to stack
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//push THAT to stack
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
//set new ARG
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
//Set New LCL
@SP
D=M
@LCL
M=D
@nestedcall.sys.add12
0;JMP
(nestedcall.sys.main$ret.2)
// pop temp 0
@SP
M=M-1
A=M
D=M
@R5
M=D
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
// push local 2
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 3
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 4
@LCL
D=M
@4
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
// function sys.add12 0
(nestedcall.sys.add12)
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@R3
M=D
// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@R4
M=D
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
// push constant 12
@12
D=A
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
