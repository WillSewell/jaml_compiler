.class X
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method public x()V
	.limit stack 10
	.limit locals 100
	getstatic java/lang/Short/MAX_VALUE S ;Get the fields value
	istore 1			;Store top of stack in 1 (x)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 2			;Store top of stack in 2 (ps)
	aload 2				;Load value stored in 2 (ps)
	iload 1				;Load value stored in 1 (x)
	invokevirtual java/io/PrintStream/println(I)V
	return
.end method
