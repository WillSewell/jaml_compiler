.class test_method_call_static
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
	invokestatic test_method_call_static2/getDoub()D
	dstore 2			;Store top of stack in 2 (x)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 4			;Store top of stack in 4 (ps)
	aload 4				;Load value stored in 4 (ps)
	dload 2				;Load value stored in 2 (x)
	invokevirtual java/io/PrintStream/println(D)V
	return
.end method
