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
	ldc 10				;Load constant numerical value 10
	anewarray java/lang/String	;Construct new array
	astore 2			;Store top of stack in 2 (arr)
	aload 2				;Load value stored in 2 (arr)
	ldc "hello"			;Load constant string "hello" (creats a new String object)
	ldc "Hello"			;Load constant string "Hello" (creats a new String object)
	aastore				;Store the value in the array element
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 3			;Store top of stack in 3 (ps)
	aload 3				;Load value stored in 3 (ps)
	aload 2				;Load value stored in 2 (arr)
	ldc 0				;Load constant numerical value 0
	aaload
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
.end method
