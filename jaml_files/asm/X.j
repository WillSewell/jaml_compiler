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
	ldc2_w 1.1			;Load constant numerical value 1.1
	invokestatic java/lang/Double/isNaN(D)Z
	invokevirtual java/io/PrintStream/println(Z)V
	return
.end method
