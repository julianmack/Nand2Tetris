//initialise
@256
D=A
@SP
M=D
//push return address to stack
@sys.init$ret.0
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
@sys.init
0;JMP
(sys.init$ret.0)
//function main.fibonacci 0
(main.fibonacci)
//push argument 0
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
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt                     // checks if n<2
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE1
D;JLT
@SP
A=M
M=0
@EQEND1
0;JMP
(EQTRUE1)
@SP
A=M
M=-1
(EQEND1)
@SP
M=M+1
//if-goto if_true
@SP
M=M-1
A=M
D=M
@main.fibonacci$if_true
D;JNE
//goto if_false
@main.fibonacci$if_false
0;JMP
//label if_true          // if n<2, return n
(main.fibonacci$if_true)
//push argument 0
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
//return
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
//Get return value for caller
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
//reset SP
@ARG
D=M+1
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
//go-to return address
@retAddr
A=M
0;JMP
//label if_false         // if n>=2, returns fib(n-2)+fib(n-1)
(main.fibonacci$if_false)
//push argument 0
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
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
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
//call main.fibonacci 1  // computes fib(n-2)
//push return address to stack
@main.fibonacci$ret.1
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
@main.fibonacci
0;JMP
(main.fibonacci$ret.1)
//push argument 0
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
//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
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
//call main.fibonacci 1  // computes fib(n-1)
//push return address to stack
@main.fibonacci$ret.2
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
@main.fibonacci
0;JMP
(main.fibonacci$ret.2)
//add                    // returns fib(n-1) + fib(n-2)
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
//return
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
//Get return value for caller
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
//reset SP
@ARG
D=M+1
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
//go-to return address
@retAddr
A=M
0;JMP
//function sys.init 0
(sys.init)
//push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
//call main.fibonacci 1   // computes the 4'th fibonacci element
//push return address to stack
@main.fibonacci$ret.3
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
@main.fibonacci
0;JMP
(main.fibonacci$ret.3)
//label while
(sys.init$while)
//goto while              // loops infinitely
@sys.init$while
0;JMP
