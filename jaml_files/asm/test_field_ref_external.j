.class test_field_ref_external
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
	new test_field_ref_external2	;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_field_ref_external2/<init>()V ;Call the constructor
	astore 2			;Store top of stack in 2 (x)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 3			;Store top of stack in 3 (ps)
	aload 3				;Load value stored in 3 (ps)
	aload 2				;Load value stored in 2 (x)
	getfield test_field_ref_external2/f Ljava/lang/String; ;Get the fields value
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
.end method
