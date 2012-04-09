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
	astore 1			;Store top of stack in 1 (ps)
	aload 1				;Load value stored in 1 (ps)
	aload 0				;Load value stored in 0 (args)
	ldc 0				;Load constant numerical value 0
	aaload
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
.end method
