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
	ldc 5				;Load constant numerical value 5
	anewarray long			;Construct new array
	astore 2			;Store top of stack in 2 (a)
	ldc 0				;Load constant numerical value 0
	istore 4			;Store top of stack in 4 (i)
ForStart0:				;Create an initial label to return to for loop effect
	iload 4				;Load value stored in 4 (i)
	ldc 5				;Load constant numerical value 5
	if_icmplt CompTrue0		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd0			;Jump to the end of the comparison
CompTrue0:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd0:				;Exit point for comparison if it is false
	ifeq ForEnd0			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	aload 2				;Load value stored in 2 (a)
	iload 4				;Load value stored in 4 (i)
	iload 4				;Load value stored in 4 (i)
	i2l				;Convert left hand side to match the type of the right
	lastore				;Store the value in the array element
	iinc 4 1			;Increments variable 4 (i)
	goto ForStart0			;Jump back to ForStart to create the loop effect
ForEnd0:				;Exit point for the loop
	ldc 4				;Load constant numerical value 4
	istore 5			;Store top of stack in 5 (j)
ForStart1:				;Create an initial label to return to for loop effect
	iload 5				;Load value stored in 5 (j)
	ldc 0				;Load constant numerical value 0
	if_icmpge CompTrue1		;If the value on the top of the stack is greater than or equal to the one below it, jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd1			;Jump to the end of the comparison
CompTrue1:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd1:				;Exit point for comparison if it is false
	ifeq ForEnd1			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 6			;Store top of stack in 6 (ps)
	aload 6				;Load value stored in 6 (ps)
	aload 2				;Load the array to store into
	iload 5				;Load value stored in 5 (j)
	laload
	invokevirtual java/io/PrintStream/println(J)V
	iinc 5 -1			;Increments variable 5 (j)
	goto ForStart1			;Jump back to ForStart to create the loop effect
ForEnd1:				;Exit point for the loop
	return
.end method
