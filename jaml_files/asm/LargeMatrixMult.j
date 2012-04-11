.class LargeMatrixMult
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	ldc 1000			;Load constant numerical value 1000
	ldc 1000			;Load constant numerical value 1000
	multianewarray [[D 2		;Construct a new multidimensional array
	astore 1			;Store top of stack in 1 (A)
	ldc 0				;Load constant numerical value 0
	istore 2			;Store top of stack in 2 (i)
ForStart0:				;Create an initial label to return to for loop effect
	iload 2				;Load value stored in 2 (i)
	aload 1				;Load value stored in 1 (A)
	arraylength			;Get the array's length
	if_icmplt CompTrue0		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd0			;Jump to the end of the comparison
CompTrue0:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd0:				;Exit point for comparison if it is false
	ifeq ForEnd0			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	ldc 0				;Load constant numerical value 0
	istore 3			;Store top of stack in 3 (j)
ForStart1:				;Create an initial label to return to for loop effect
	iload 3				;Load value stored in 3 (j)
	aload 1				;Load value stored in 1 (A)
	iconst_0			;Index into first element
	aaload				;Load 2nd dimension
	arraylength			;Get the array's length
	if_icmplt CompTrue1		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd1			;Jump to the end of the comparison
CompTrue1:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd1:				;Exit point for comparison if it is false
	ifeq ForEnd1			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	aload 1				;Load value stored in 1 (A)
	iload 2				;Load value stored in 2 (i)
	aaload
	iload 3				;Load value stored in 3 (j)
	iload 2				;Load value stored in 2 (i)
	iload 3				;Load value stored in 3 (j)
	iadd				;Apply + to the values on the top of the stack
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	iinc 3 1			;Increments variable 3 (j)
	goto ForStart1			;Jump back to ForStart to create the loop effect
ForEnd1:				;Exit point for the loop
	iinc 2 1			;Increments variable 2 (i)
	goto ForStart0			;Jump back to ForStart to create the loop effect
ForEnd0:				;Exit point for the loop
	ldc 1000			;Load constant numerical value 1000
	ldc 1000			;Load constant numerical value 1000
	multianewarray [[D 2		;Construct a new multidimensional array
	astore 4			;Store top of stack in 4 (B)
	ldc 0				;Load constant numerical value 0
	istore 5			;Store top of stack in 5 (m)
ForStart2:				;Create an initial label to return to for loop effect
	iload 5				;Load value stored in 5 (m)
	aload 4				;Load value stored in 4 (B)
	arraylength			;Get the array's length
	if_icmplt CompTrue2		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd2			;Jump to the end of the comparison
CompTrue2:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd2:				;Exit point for comparison if it is false
	ifeq ForEnd2			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	ldc 0				;Load constant numerical value 0
	istore 6			;Store top of stack in 6 (n)
ForStart3:				;Create an initial label to return to for loop effect
	iload 6				;Load value stored in 6 (n)
	aload 4				;Load value stored in 4 (B)
	iconst_0			;Index into first element
	aaload				;Load 2nd dimension
	arraylength			;Get the array's length
	if_icmplt CompTrue3		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd3			;Jump to the end of the comparison
CompTrue3:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd3:				;Exit point for comparison if it is false
	ifeq ForEnd3			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	aload 4				;Load value stored in 4 (B)
	iload 5				;Load value stored in 5 (m)
	aaload
	iload 6				;Load value stored in 6 (n)
	iload 5				;Load value stored in 5 (m)
	iload 6				;Load value stored in 6 (n)
	iadd				;Apply + to the values on the top of the stack
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	iinc 6 1			;Increments variable 6 (n)
	goto ForStart3			;Jump back to ForStart to create the loop effect
ForEnd3:				;Exit point for the loop
	iinc 5 1			;Increments variable 5 (m)
	goto ForStart2			;Jump back to ForStart to create the loop effect
ForEnd2:				;Exit point for the loop
	invokestatic java/lang/System/nanoTime()J
	lstore 7			;Store top of stack in 7 (startTime)
	aload 1				;Load value stored in 1 (A)
	dup				;Dup to get the rows and the columns
	iconst_0			;Index into first dimension
	aaload				;Load second dimension
	arraylength			;Get cols length
	istore 10			;Store length
	arraylength			;Get rows length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 11			;Store length
	aload 4				;Load value stored in 4 (B)
	dup				;Dup to get the rows and the columns
	arraylength			;Get rows length
	istore 12			;Store length
	iconst_0			;Index into first dimension
	aaload				;Load second dimension
	arraylength			;Get cols length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 13			;Store length
	iload 10			;Load first array's columns
	iload 12			;Load second array's rows
	if_icmpeq CompTrue4		;Check dimensions match
	new java/lang/ArithmeticException ;Create a new exception
	dup				;Dup in order to call constructor, and throw
	ldc "Inner matrix dimensions must match for multiplication!" ;Load error message
	invokespecial java/lang/ArithmeticException/<init>(Ljava/lang/String;)V ;Invoke the exception's constructor
	athrow				;Throw the exception
CompTrue4:				;Exit check here if no exception thrown
	multianewarray [[D 2		;Construct a new array to store result
	astore 14			;Store the result array
	iconst_0			;Load 0
	istore 15			;Store index
MatRowStart0:				;Start of loop through rows
	iload 15			;Load index
	iload 11			;Get row length
	if_icmpge MatRowEnd0		;Check if idx has reached the size of the rows
	iconst_0			;Load 0
	istore 16			;Set loop index to 0
MatBColStart0:				;Start of loop through rows
	iload 16			;Load index
	iload 13			;Get row len
	if_icmpge MatBColEnd0		;Check if idx has reached the size of the cols
	iconst_0			;Load 0
	istore 17			;Set loop index to 0
MatAColStart0:				;Start of loop through rows
	iload 17			;Load index
	iload 10			;Get row len
	if_icmpge MatAColEnd0		;Check if idx has reached the size of the cols
	aload 14			;Load the result matrix
	iload 15			;Load row index
	aaload				;Load matrix row
	iload 16			;Load col index
	dup2				;Duplicate the array and its index so that one can be used to load the elementand one can be used to store into at the end
	daload				;Load the array element to add to the result of the multiplication
	aload 1				;Load value stored in 1 (A)
	iload 15			;Load row index
	aaload				;Load matrix row
	iload 17			;Load col index
	daload				;Load current matrix element
	aload 4				;Load value stored in 4 (B)
	iload 17			;Load row index
	aaload				;Load matrix row
	iload 16			;Load col index
	daload				;Load current matrix element
	dmul				;Mul element values
	dadd				;Add multiplied values to what is already in the result array
	dastore				;Store result in new array
	iinc 17 1			;Increment the index
	goto MatAColStart0		;Return to start of inner loop
MatAColEnd0:				;End of the inner loop
	iinc 16 1			;Increment the index
	goto MatBColStart0		;Return to start of middle loop
MatBColEnd0:				;End of the middle loop
	iinc 15 1			;Increment the index
	goto MatRowStart0		;Return to start of inner loop
MatRowEnd0:				;End of the inner loop
	aload 14			;Leave the result matrix on the stack
	astore 9			;Store top of stack in 9 (C)
	invokestatic java/lang/System/nanoTime()J
	lstore 18			;Store top of stack in 18 (endTime)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 20			;Store top of stack in 20 (ps)
	aload 20			;Load value stored in 20 (ps)
	ldc "Took "			;Load constant string "Took " (creates a new String object)
	lload 18			;Load value stored in 18 (endTime)
	lload 7				;Load value stored in 7 (startTime)
	lsub				;Apply - to the values on the top of the stack
	invokestatic java/lang/Long/toString(J)Ljava/lang/String;
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String; ;Use the built in concat method of String
	ldc " ns"			;Load constant string " ns" (creates a new String object)
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String; ;Use the built in concat method of String
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
.end method
