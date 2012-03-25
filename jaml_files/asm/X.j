.class X
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial Object<init>()V
	return
.end method
.method x()L;
	.limit stack 10
	.limit locals 100
	getfield java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 1			;Store top of stack in 1 (ps)
	aload 1				;Load value stored in 1 (ps)
	invokevirtual java/io/PrintStream/println(I)V
	return
.end method
