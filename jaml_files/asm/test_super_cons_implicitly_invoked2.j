.class test_super_cons_implicitly_invoked2
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 1			;Store top of stack in 1 (ps)
	aload 1				;Load value stored in 1 (ps)
	ldc "pass"			;Load constant string "pass" (creats a new String object)
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
.end method
