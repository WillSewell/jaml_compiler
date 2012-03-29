.class test_field_ref_super
.super test_field_ref_super2
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial test_field_ref_super2/<init>()V
	return
.end method
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	new test_field_ref_super	;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_field_ref_super/<init>()V ;Call the constructor
	astore 2			;Store top of stack in 2 (x)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 3			;Store top of stack in 3 (ps)
	aload 3				;Load value stored in 3 (ps)
	aload 2				;Load value stored in 2 (x)
	getfield test_field_ref_super2/f J ;Get the fields value
	invokevirtual java/io/PrintStream/println(J)V
	return
.end method
