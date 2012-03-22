.class TestArray
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
	new TestArray			;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial TestArray/<init>()V ;Call the constructor
	astore 2			;Store top of stack in 2 (obj)
	aload 2				;Load value stored in 2 (obj)
	ldc 10				;Load constant numerical value 10
	invokevirtual TestArray/get1D(I)[I
	astore 3			;Store top of stack in 3 (x)
	aload 2				;Load value stored in 2 (obj)
	invokevirtual TestArray/get2D()[[Ljava/lang/String;
	astore 4			;Store top of stack in 4 (y)
	return
.end method
.method get1D(I)[I
	.limit stack 10
	.limit locals 100
	iload 1				;Load value stored in 1 (len)
	newarray int			;Construct new array
	areturn				;Return from method
.end method
.method get2D()[[Ljava/lang/String;
	.limit stack 10
	.limit locals 100
	ldc 10				;Load constant numerical value 10
	ldc 10				;Load constant numerical value 10
	multianewarray [[Ljava/lang/String; 2 ;Construct a new multidimensional array
	areturn				;Return from method
.end method
