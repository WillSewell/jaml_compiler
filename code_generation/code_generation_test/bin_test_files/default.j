.class Default
.super java/lang/Object
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	ldc 1				;Load constant numerical value 1
	istore 0			;Store top of stack in 0 (i)
WhileStart0:			;Create an initial label to return to for loop effect
	iload 0				;Load value stored in 0 (i)
	ldc 10				;Load constant numerical value 10
	if_icmple CompTrue0	;If the value on the top of the stack is less than or equal to the one below it,jump to CompTrue
	ldc 0				;Comparison was false, so load binary constant 0
	goto CompEnd0		;Jump to the end of the comparison
CompTrue0:				;End up here if the comparison was true
	ldc 1				;Comparison was true, so load binary constant 1
CompEnd0:				;Exit point for comparison if it is false
	ifeq WhileEnd0		;Jump to WhileEnd if the boolean expression evaluates to false to break out of loop
	iload 0				;Load value stored in 0 (i)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get staic PrintStream object reference
	swap				;Swap the value to print with the reference to the PrintStream object
	invokevirtual java/io/PrintStream/println(I)V ;invoke print method
	iload 0				;Load value stored in 0 (i)
	ldc 1				;Load constant numerical value 1
	iadd				;Apply + to the values on the top of the stack
	istore 0			;Store top of stack in 0 (i)
	goto WhileStart0		;Jump back to WhileStart to create the loop effect
WhileEnd0:				;Exit point for he loop
	return
.end method
