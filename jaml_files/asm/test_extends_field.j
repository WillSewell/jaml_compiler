.class test_extends_field
.super test_extends_field2
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial test_extends_field2/<init>()V
	return
.end method
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	new test_extends_field	;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_extends_field/<init>()V ;Call the constructor
	astore 2			;Store top of stack in 2 (sub)
	aload 2				;Load value stored in 2 (sub)
	invokevirtual test_extends_field/y()V
	return
.end method
.method y()V
	.limit stack 10
	.limit locals 100
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 1			;Store top of stack in 1 (ps)
	aload 1				;Load value stored in 1 (ps)
	aload_0				;Load "this" in order to access the field
	getfield test_extends_field2/x I ;Get the fields value
	invokevirtual java/io/PrintStream/println(I)V
	return
.end method
