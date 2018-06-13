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
//function class1.set 0
(class1.set)
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
//pop static 0
@SP
M=M-1
A=M
D=M
@class10
M=D
//push argument 1
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
//pop static 1
@SP
M=M-1
A=M
D=M
@class11
M=D
//push constant 0
@0
D=A
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
//function class1.get 0
(class1.get)
//push static 0
@class10
D=M
@SP
A=M
M=D
@SP
M=M+1
//push static 1
@class11
D=M
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
//function class2.set 0
(class2.set)
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
//pop static 0
@SP
M=M-1
A=M
D=M
@class20
M=D
//push argument 1
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
//pop static 1
@SP
M=M-1
A=M
D=M
@class21
M=D
//push constant 0
@0
D=A
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
//function class2.get 0
(class2.get)
//push static 0
@class20
D=M
@SP
A=M
M=D
@SP
M=M+1
//push static 1
@class21
D=M
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
//push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
//call class1.set 2
//push return address to stack
@class1.set$ret.-3
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
@2
D=D-A
@ARG
M=D
//Set New LCL
@SP
D=M
@LCL
M=D
@class1.set
0;JMP
(class1.set$ret.-3)
//pop temp 0 // dumps the return value
@SP
M=M-1
A=M
D=M
@R5
M=D
//push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
//call class2.set 2
//push return address to stack
@class2.set$ret.-2
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
@2
D=D-A
@ARG
M=D
//Set New LCL
@SP
D=M
@LCL
M=D
@class2.set
0;JMP
(class2.set$ret.-2)
//pop temp 0 // dumps the return value
@SP
M=M-1
A=M
D=M
@R5
M=D
//call class1.get 0
//push return address to stack
@class1.get$ret.-1
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
@class1.get
0;JMP
(class1.get$ret.-1)
//call class2.get 0
//push return address to stack
@class2.get$ret.0
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
@class2.get
0;JMP
(class2.get$ret.0)
//label while
(sys.init$while)
//goto while
@sys.init$while
0;JMP
