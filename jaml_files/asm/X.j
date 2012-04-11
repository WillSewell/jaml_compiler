.class X
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
	new X				;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial X/<init>()V	;Call the constructor
	astore 1			;Store top of stack in 1 (x)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 2			;Store top of stack in 2 (ps)
	aload 2				;Load value stored in 2 (ps)
	aload 1				;Load value stored in 1 (x)
	new java/lang/Object		;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial java/lang/Object/<init>()V ;Call the constructor
	invokevirtual java/lang/Object/equals(Ljava/lang/Object;)Z
	invokevirtual java/io/PrintStream/println(Z)V
	return
.end method
