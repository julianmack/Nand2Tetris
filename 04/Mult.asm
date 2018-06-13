// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

//setup total and iteration variables
      @total  //to store result of multiplication
      M=0     //total=0
      @i      //for iteration
      M=1     //set i=0

  (LOOP)
      //check if loop should end
      @i
      D=M     //D=i
      @R0    //A-> RAM[0], M=first_num
      D=M-D   //1st_num - i
      @STOP
      D; JLT  //end if 1st_num - i < 0 (i.e. 1st_num < i)

      //Add to total
      @total
      D=M
      @R1
      D=D+M  //D=total + 2nd_num
      @total
      M=D    //Store new total in @total

      //increment i
      @i
      M=M+1

      //Jump back to start of loop
      @LOOP
      0;JMP

  (STOP)
      @total
      D=M      //D=total
      @R2      //M=RAM[2]
      M=D      //final_total stored in RAM[2]

  (END)
      @END
      0;JMP
