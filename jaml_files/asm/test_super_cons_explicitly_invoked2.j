.class test_super_cons_explicitly_invoked2
.super java/lang/Object
.method <init>(Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 2			;Store top of stack in 2 (ps)
	aload 2				;Load value stored in 2 (ps)
	aload 1				;Load value stored in 1 (arg)
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
.end method
