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
	ldc 1				;Load constant numerical value 1
	istore 2			;Store top of stack in 2 (i)
WhileStart0:				;Create an initial label to return to for loop effect
	iload 2				;Load value stored in 2 (i)
	ldc 10				;Load constant numerical value 10
	if_icmple CompTrue0		;If the value on the top of the stack is less than or equal to the one below it, jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd0			;Jump to the end of the comparison
CompTrue0:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd0:				;Exit point for comparison if it is false
	ifeq WhileEnd0			;Jump to WhileEnd if the boolean expression evaluates to false to break out of loop
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 3			;Store top of stack in 3 (ps)
	aload 3				;Load value stored in 3 (ps)
	iload 2				;Load value stored in 2 (i)
	invokevirtual java/io/PrintStream/println(I)V
	iload 2				;Load value stored in 2 (i)
	ldc 1				;Load constant numerical value 1
	iadd				;Apply + to the values on the top of the stack
	istore 2			;Store top of stack in 2 (i)
	goto WhileStart0		;Jump back to WhileStart to create the loop effect
WhileEnd0:				;Exit point for he loop
	return
.end method
