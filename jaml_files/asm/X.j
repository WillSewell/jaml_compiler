.class X
.super java/lang/Object
.field f [I
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
	ldc 1				;Load constant numerical value 1
	newarray int			;Construct new array
	putfield X/f [I		;Store into field f
	aload_0				;Load "this" in order to access the field
	getfield X/f [I		;Get the fields value
	ldc 0				;Load constant numerical value 0
	ldc 5				;Load constant numerical value 5
	iastore				;Store the value in the array element
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 1			;Store top of stack in 1 (ps)
	aload 1				;Load value stored in 1 (ps)
	aload_0				;Load "this" in order to access the field
	getfield X/f [I		;Get the fields value
	ldc 0				;Load constant numerical value 0
	iaload
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
