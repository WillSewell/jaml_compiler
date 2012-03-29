.class test_field_ref_static
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
	getstatic test_field_ref_static2/x F ;Get the fields value
	invokevirtual java/io/PrintStream/println(F)V
	return
.end method
