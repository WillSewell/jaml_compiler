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
	ldc "s"				;Load constant string "s" (creats a new String object)
	astore 2			;Store top of stack in 2 (s)
	ldc 0				;Load constant numerical value 0
	istore 3			;Store top of stack in 3 (i)
ForStart0:				;Create an initial label to return to for loop effect
	iload 3				;Load value stored in 3 (i)
	ldc 5				;Load constant numerical value 5
	if_icmplt CompTrue0		;If the value on the top of the stack is less than the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd0			;Jump to the end of the comparison
CompTrue0:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd0:				;Exit point for comparison if it is false
	ifeq ForEnd0			;Jump to ForEnd if the boolean expression evaluates to false to break out of loop
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 4			;Store top of stack in 4 (ps)
	aload 4				;Load value stored in 4 (ps)
	aload 2				;Load value stored in 2 (s)
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	iload 3				;Load value stored in 3 (i)
	ldc 1				;Load constant numerical value 1
	iadd				;Apply + to the values on the top of the stack
	istore 3			;Store top of stack in 3 (i)
	goto ForStart0			;Jump back to ForStart to create the loop effect
ForEnd0:				;Exit point for the loop
	return
.end method
