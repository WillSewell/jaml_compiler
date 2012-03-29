.class X
.super java/lang/Object
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
	aload_0 			;Load the local variable in location 0, which is a reference to the current object
	invokevirtual X/meth2()[[B
	astore 1			;Store top of stack in 1 (x)
	aload 1				;Load the array to store into
	ldc 0				;Load constant numerical value 0
	aaload
	ldc 0				;Load constant numerical value 0
	baload
	istore 2			;Store top of stack in 2 (y)
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 3			;Store top of stack in 3 (ps)
	aload 3				;Load value stored in 3 (ps)
	iload 2				;Load value stored in 2 (y)
	invokevirtual java/io/PrintStream/println(I)V
	return
.end method
.method public meth2()[[B
	.limit stack 10
	.limit locals 100
	ldc 5				;Load constant numerical value 5
	ldc 5				;Load constant numerical value 5
	multianewarray [[B 2		;Construct a new multidimensional array
	astore 1			;Store top of stack in 1 (arr)
	aload 1				;Load value stored in 1 (arr)
	ldc 0				;Load constant numerical value 0
	aaload
	ldc 0				;Load constant numerical value 0
	ldc 5				;Load constant numerical value 5
	bastore				;Store the value in the array element
	aload 1				;Load value stored in 1 (arr)
	areturn				;Return from method
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
