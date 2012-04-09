.class X
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
	ldc 2				;Load constant numerical value 2
	ldc 3				;Load constant numerical value 3
	multianewarray [[D 2		;Construct a new multidimensional array
	astore 2			;Store top of stack in 2 (a1)
	aload 2				;Load value stored in 2 (a1)
	ldc 0				;Load constant numerical value 0
	aaload
	ldc 0				;Load constant numerical value 0
	ldc 1				;Load constant numerical value 1
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 2				;Load value stored in 2 (a1)
	ldc 0				;Load constant numerical value 0
	aaload
	ldc 1				;Load constant numerical value 1
	ldc 2				;Load constant numerical value 2
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 2				;Load value stored in 2 (a1)
	ldc 0				;Load constant numerical value 0
	aaload
	ldc 2				;Load constant numerical value 2
	ldc 3				;Load constant numerical value 3
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 2				;Load value stored in 2 (a1)
	ldc 1				;Load constant numerical value 1
	aaload
	ldc 0				;Load constant numerical value 0
	ldc 4				;Load constant numerical value 4
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 2				;Load value stored in 2 (a1)
	ldc 1				;Load constant numerical value 1
	aaload
	ldc 1				;Load constant numerical value 1
	ldc 5				;Load constant numerical value 5
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 2				;Load value stored in 2 (a1)
	ldc 1				;Load constant numerical value 1
	aaload
	ldc 2				;Load constant numerical value 2
	ldc 6				;Load constant numerical value 6
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	ldc 2				;Load constant numerical value 2
	ldc 3				;Load constant numerical value 3
	multianewarray [[D 2		;Construct a new multidimensional array
	astore 3			;Store top of stack in 3 (a2)
	aload 3				;Load value stored in 3 (a2)
	ldc 0				;Load constant numerical value 0
	aaload
	ldc 0				;Load constant numerical value 0
	ldc 1				;Load constant numerical value 1
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 3				;Load value stored in 3 (a2)
	ldc 0				;Load constant numerical value 0
	aaload
	ldc 1				;Load constant numerical value 1
	ldc 2				;Load constant numerical value 2
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 3				;Load value stored in 3 (a2)
	ldc 0				;Load constant numerical value 0
	aaload
	ldc 2				;Load constant numerical value 2
	ldc 3				;Load constant numerical value 3
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 3				;Load value stored in 3 (a2)
	ldc 1				;Load constant numerical value 1
	aaload
	ldc 0				;Load constant numerical value 0
	ldc 4				;Load constant numerical value 4
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 3				;Load value stored in 3 (a2)
	ldc 1				;Load constant numerical value 1
	aaload
	ldc 1				;Load constant numerical value 1
	ldc 5				;Load constant numerical value 5
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 3				;Load value stored in 3 (a2)
	ldc 1				;Load constant numerical value 1
	aaload
	ldc 2				;Load constant numerical value 2
	ldc 6				;Load constant numerical value 6
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 2				;Load value stored in 2 (a1)
	arraylength			;Get rows length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 5			;Store length
	aload 3				;Load value stored in 3 (a2)
	iconst_0			;Index into first dimension
	aaload				;Load second dimension
	arraylength			;Get cols length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 6			;Store length
	multianewarray [[D 2		;Construct a new array to store result
	astore 7			;Store the result array
	iconst_0			;Load 0
	istore 8			;Store index
MatRowStart0:				;Start of loop through rows
	iload 8				;Load index
	iload 5				;Get row length
	if_icmpge MatRowEnd0		;Check if idx has reached the size of the rows
	iconst_0			;Load 0
	istore 9			;Set loop index to 0
MatColStart0:				;Start of loop through rows
	iload 9				;Load index
	iload 6				;Get row len
	if_icmpge MatColEnd0		;Check if idx has reached the size of the cols
	aload 7				;Load the result matrix
	iload 8				;Load row index
	aaload				;Load matrix row
	iload 9				;Load col index
	aload 2				;Load value stored in 2 (a1)
	iload 8				;Load row index
	aaload				;Load matrix row
	iload 9				;Load col index
	daload				;Load current matrix element
	aload 3				;Load value stored in 3 (a2)
	iload 8				;Load row index
	aaload				;Load matrix row
	iload 9				;Load col index
	daload				;Load current matrix element
	dsub				;Sub element values
	dastore				;Store result in new array
	iinc 9 1			;Increment the index
	goto MatColStart0		;Return to start of inner loop
MatColEnd0:				;End of the inner loop
	iinc 8 1			;Increment the index
	goto MatRowStart0		;Return to start of inner loop
MatRowEnd0:				;End of the inner loop
	aload 7				;Leave the result matrix on the stack
	astore 4			;Store top of stack in 4 (a3)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 10			;Store top of stack in 10 (ps)
	ldc 0				;Load constant numerical value 0
	istore 11			;Store top of stack in 11 (n)
ForStart0:				;Create an initial label to return to for loop effect
	iload 11			;Load value stored in 11 (n)
	ldc 2				;Load constant numerical value 2
	if_icmplt CompTrue0		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd0			;Jump to the end of the comparison
CompTrue0:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd0:				;Exit point for comparison if it is false
	ifeq ForEnd0			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	ldc 0				;Load constant numerical value 0
	istore 12			;Store top of stack in 12 (o)
ForStart1:				;Create an initial label to return to for loop effect
	iload 12			;Load value stored in 12 (o)
	ldc 3				;Load constant numerical value 3
	if_icmplt CompTrue1		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd1			;Jump to the end of the comparison
CompTrue1:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd1:				;Exit point for comparison if it is false
	ifeq ForEnd1			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	aload 10			;Load value stored in 10 (ps)
	aload 4				;Load value stored in 4 (a3)
	iload 11			;Load value stored in 11 (n)
	aaload				;Load inner array
	iload 12			;Load value stored in 12 (o)
	daload				;Load the value
	invokevirtual java/io/PrintStream/println(D)V
	iinc 12 1			;Increments variable 12 (o)
	goto ForStart1			;Jump back to ForStart to create the loop effect
ForEnd1:				;Exit point for the loop
	iinc 11 1			;Increments variable 11 (n)
	goto ForStart0			;Jump back to ForStart to create the loop effect
ForEnd0:				;Exit point for the loop
	return
.end method
