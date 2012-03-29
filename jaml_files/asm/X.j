.class X
.super java/lang/Object
.field f I
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method public meth()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object to assign to field
	ldc 5				;Load constant numerical value 5
	putfield X/f I			;Store into field f
	aload_0				;Load the current object to assign to field
	aload_0				;Load "this" in order to access the field
	getfield X/f I			;Get the fields value
	ldc 1				;Push 1 or -1 onto the stack
	iadd				;Add the 1 to the value
	putfield X/f I			;Store into field f
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 1			;Store top of stack in 1 (ps)
	aload 1				;Load value stored in 1 (ps)
	aload_0				;Load "this" in order to access the field
	getfield X/f I			;Get the fields value
	invokevirtual java/io/PrintStream/println(I)V
	return
.end method
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	new X				;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial X/<init>()V	;Call the constructor
	astore 2			;Store top of stack in 2 (inst)
	aload 2				;Load value stored in 2 (inst)
	invokevirtual X/meth()V
	return
.end method
