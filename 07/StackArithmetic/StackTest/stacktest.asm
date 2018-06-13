// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE1
D;JEQ
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

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE2
D;JEQ
@SP
A=M
M=0
@EQEND2
0;JMP
(EQTRUE2)
@SP
A=M
M=-1
(EQEND2)
@SP
M=M+1

// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE3
D;JEQ
@SP
A=M
M=0
@EQEND3
0;JMP
(EQTRUE3)
@SP
A=M
M=-1
(EQEND3)
@SP
M=M+1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE4
D;JLT
@SP
A=M
M=0
@EQEND4
0;JMP
(EQTRUE4)
@SP
A=M
M=-1
(EQEND4)
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE5
D;JLT
@SP
A=M
M=0
@EQEND5
0;JMP
(EQTRUE5)
@SP
A=M
M=-1
(EQEND5)
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE6
D;JLT
@SP
A=M
M=0
@EQEND6
0;JMP
(EQTRUE6)
@SP
A=M
M=-1
(EQEND6)
@SP
M=M+1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE7
D;JGT
@SP
A=M
M=0
@EQEND7
0;JMP
(EQTRUE7)
@SP
A=M
M=-1
(EQEND7)
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE8
D;JGT
@SP
A=M
M=0
@EQEND8
0;JMP
(EQTRUE8)
@SP
A=M
M=-1
(EQEND8)
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQTRUE9
D;JGT
@SP
A=M
M=0
@EQEND9
0;JMP
(EQTRUE9)
@SP
A=M
M=-1
(EQEND9)
@SP
M=M+1

// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 53
@53
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

// push constant 112
@112
D=A
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

// neg
@SP
M=M-1
A=M
M=-M
@SP
M=M+1

// and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D&M
@SP
M=M+1

// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

// or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D|M
@SP
M=M+1

// not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1

