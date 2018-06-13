// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


    @colour  //variable holding current colour of screen
    M = 0    //white

    @8192      //Stores # of words in screen
    D=A
    @endscreen
    M=D

    //Infinite LOOP to check for keyboard pressed?
    (KEYBOARDLOOP)
        @KBD
        D=M

        //IF keyboard  pressed (i.e. if D!=0)

        @ELSE //jump to ELSE if not pressed
        D; JEQ

        //THEN - i.e. if pressed
        @colour
        D = M   //D=colour
        @PAINTSCREEN
        D; JEQ  //D < 0 (i.e. colour = -1)
        //if no change required
        @KEYBOARDLOOP
        0; JMP  //Jumps to start of KEYBOARDLOOP

        (ELSE)  //not pressed
          @colour
          D = M   //D=colour
          @PAINTSCREEN  //(if colour is black)
          D; JLT
          //if no change required
          @KEYBOARDLOOP
          0; JMP  //Jumps to start of KEYBOARDLOOP



    (PAINTSCREEN)
    //Paint Screen other colour
    @colour
    D = !M
    M = D  //change to other colour

    //setup iterator
    @index
    M=0

    //loop until screen has changed colour
    (PAINTLOOP)
        //loop termination condition
        @index
        D=M             //D=index
        @endscreen      //M=8192
        D=D-M           //i - 8192
        @STOPPAINTLOOP
        D;JGT          //end if i - 8192 = 0 (i.e. i == 8192)

        //Paint Word
        @index          //get array index
        D=M             //D=index
        @SCREEN         //A = 16384, M=0 or -1 depending on colour.
                        //i.e. start index of screen is (16384)
        D=D+A           //Current address of word on screen

        //set new colour
        @address        //temp address
        M=D             //Store address in memory
        @colour
        D=M
        @address        //retrieve address
        A=M             //set A to stored address
        M=D

        //N.B - seven lines above are equivalent to the line below - wanted to practice pointers
        //M=!M            //Switch colour


        //update index
        @index
        M=M+1

        //Go to start of LOOP
        @PAINTLOOP
        0;JMP

    (STOPPAINTLOOP)
        @KEYBOARDLOOP
        0; JMP
