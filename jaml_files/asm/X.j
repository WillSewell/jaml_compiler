.class X
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method public static main ([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	ldc 2				;Load constant numerical value 2
	ldc 1				;Load constant numerical value 1
	if_icmpgt CompTrue0		;If the value on the top of the stack is greater than the one below it, jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd0			;Jump to the end of the comparison
CompTrue0:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd0:				;Exit point for comparison if it is false
	ifeq IfFalse0			;Jump to IfFalse if if-stmt evaluates to false
	ldc 0				;Load constant numerical value 0
	istore 1			;Store top of stack in 1 (x)
	goto IfEnd0
IfFalse0:				;Continue from here if if_stmt was false
IfEnd0:					;End the if statement
	ldc 1				;Load constant numerical value 1
	istore 2			;Store top of stack in 2 (x)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 3			;Store top of stack in 3 (ps)
	aload 3				;Load value stored in 3 (ps)
	iload 2				;Load value stored in 2 (x)
	invokevirtual java/io/PrintStream/println(I)V
	return
.end method
