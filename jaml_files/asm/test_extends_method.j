.class test_extends_method
.super test_extends_method2
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial test_extends_method2/<init>()V
	aload_0 			;Load the local variable in location 0, which is a reference to the current object
	invokevirtual test_extends_method2/y()J
	lstore 1			;Store top of stack in 1 (z)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 2			;Store top of stack in 2 (ps)
	aload 2				;Load value stored in 2 (ps)
	lload 1				;Load value stored in 1 (z)
	invokevirtual java/io/PrintStream/println(J)V
	return
.end method
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	new test_extends_method	;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_extends_method/<init>()V ;Call the constructor
	return
.end method
