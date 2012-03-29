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
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 2			;Store top of stack in 2 (ps)
	aload 2				;Load value stored in 2 (ps)
	ldc 1				;Load constant numerical value 1
	ldc 1				;Load constant numerical value 1
	iadd				;Apply + to the values on the top of the stack
	invokevirtual java/io/PrintStream/println(I)V
	return
.end method
