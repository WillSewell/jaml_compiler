.class test_method_call_external
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
	new test_method_call_external2	;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_method_call_external2/<init>()V ;Call the constructor
	astore 1			;Store top of stack in 1 (y)
	aload 1				;Load value stored in 1 (y)
	invokevirtual test_method_call_external2/w()F
	fstore 2			;Store top of stack in 2 (z)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 3			;Store top of stack in 3 (ps)
	aload 3				;Load value stored in 3 (ps)
	fload 2				;Load value stored in 2 (z)
	invokevirtual java/io/PrintStream/println(F)V
	return
.end method
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	new test_method_call_external	;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_method_call_external/<init>()V ;Call the constructor
	astore 2			;Store top of stack in 2 (meth)
	aload 2				;Load value stored in 2 (meth)
	invokevirtual test_method_call_external/x()V
	return
.end method
