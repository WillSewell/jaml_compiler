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
	ldc 4				;Load constant numerical value 4
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
	ldc 1				;Load constant numerical value 1
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
	ldc 1				;Load constant numerical value 1
	aaload
	ldc 0				;Load constant numerical value 0
	ldc 2				;Load constant numerical value 2
	i2d				;Convert left hand side to match the type of the right
	dastore				;Store the value in the array element
	aload 2				;Load value stored in 2 (a1)
	dup				;Dup to get the rows and the columns
	iconst_0			;Index into first dimension
	aaload				;Load second dimension
	arraylength			;Get cols length
	istore 5			;Store length
	arraylength			;Get rows length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 6			;Store length
	aload 3				;Load value stored in 3 (a2)
	dup				;Dup to get the rows and the columns
	arraylength			;Get rows length
	istore 7			;Store length
	iconst_0			;Index into first dimension
	aaload				;Load second dimension
	arraylength			;Get cols length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 8			;Store length
	iload 6				;Load first array's rows
	iload 7				;Load second array's rows
	if_icmpne CompTrue0		;If dimensions don't match, jump to exception throwing section
	iload 5				;Load first array's cols
	iload 8				;Load second array's cols
	if_icmpeq CompTrue1		;Check dimensions match
CompTrue0:				;First check failed
	new java/lang/ArithmeticException ;Create a new exception
	dup				;Dup in order to call constructor, and throw
	ldc "Matrix dimensions must be equal for addition/subtraction!" ;Load error message
	invokespecial java/lang/ArithmeticException/<init>(Ljava/lang/String;)V ;Invoke the exception's constructor
	athrow				;Throw the exception
CompTrue1:				;Exit check here if no exception thrown
	multianewarray [[D 2		;Construct a new array to store result
	astore 9			;Store the result array
	iconst_0			;Load 0
	istore 10			;Store index
MatRowStart0:				;Start of loop through rows
	iload 10			;Load index
	iload 6				;Get row length
	if_icmpge MatRowEnd0		;Check if idx has reached the size of the rows
	iconst_0			;Load 0
	istore 11			;Set loop index to 0
MatColStart0:				;Start of loop through rows
	iload 11			;Load index
	iload 8				;Get row len
	if_icmpge MatColEnd0		;Check if idx has reached the size of the cols
	aload 9				;Load the result matrix
	iload 10			;Load row index
	aaload				;Load matrix row
	iload 11			;Load col index
	aload 2				;Load value stored in 2 (a1)
	iload 10			;Load row index
	aaload				;Load matrix row
	iload 11			;Load col index
	daload				;Load current matrix element
	aload 3				;Load value stored in 3 (a2)
	iload 10			;Load row index
	aaload				;Load matrix row
	iload 11			;Load col index
	daload				;Load current matrix element
	dadd				;Add element values
	dastore				;Store result in new array
	iinc 11 1			;Increment the index
	goto MatColStart0		;Return to start of inner loop
MatColEnd0:				;End of the inner loop
	iinc 10 1			;Increment the index
	goto MatRowStart0		;Return to start of inner loop
MatRowEnd0:				;End of the inner loop
	aload 9				;Leave the result matrix on the stack
	astore 4			;Store top of stack in 4 (a3)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 12			;Store top of stack in 12 (ps)
	ldc 0				;Load constant numerical value 0
	istore 13			;Store top of stack in 13 (n)
ForStart0:				;Create an initial label to return to for loop effect
	iload 13			;Load value stored in 13 (n)
	aload 2				;Load value stored in 2 (a1)
	arraylength			;Get the array's length
	if_icmplt CompTrue2		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd2			;Jump to the end of the comparison
CompTrue2:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd2:				;Exit point for comparison if it is false
	ifeq ForEnd0			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	ldc 0				;Load constant numerical value 0
	istore 14			;Store top of stack in 14 (o)
ForStart1:				;Create an initial label to return to for loop effect
	iload 14			;Load value stored in 14 (o)
	aload 3				;Load value stored in 3 (a2)
	iconst_0			;Index into first element
	aaload				;Load 2nd dimension
	arraylength			;Get the array's length
	if_icmplt CompTrue3		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd3			;Jump to the end of the comparison
CompTrue3:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd3:				;Exit point for comparison if it is false
	ifeq ForEnd1			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	aload 12			;Load value stored in 12 (ps)
	aload 4				;Load value stored in 4 (a3)
	iload 13			;Load value stored in 13 (n)
	aaload				;Load inner array
	iload 14			;Load value stored in 14 (o)
	daload				;Load the value
	invokevirtual java/io/PrintStream/println(D)V
	iinc 14 1			;Increments variable 14 (o)
	goto ForStart1			;Jump back to ForStart to create the loop effect
ForEnd1:				;Exit point for the loop
	iinc 13 1			;Increments variable 13 (n)
	goto ForStart0			;Jump back to ForStart to create the loop effect
ForEnd0:				;Exit point for the loop
	return
.end method
