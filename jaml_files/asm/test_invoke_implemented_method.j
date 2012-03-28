.class test_invoke_implemented_method
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
	new test_invoke_implemented_method3 ;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_invoke_implemented_method3/<init>()V ;Call the constructor
	astore 2			;Store top of stack in 2 (x)
	aload 2				;Load value stored in 2 (x)
	invokeinterface test_invoke_implemented_method2/y()I 1
	istore 3			;Store top of stack in 3 (z)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 4			;Store top of stack in 4 (ps)
	aload 4				;Load value stored in 4 (ps)
	iload 3				;Load value stored in 3 (z)
	invokevirtual java/io/PrintStream/println(I)V
	return
.end method
