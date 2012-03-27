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
	getstatic java/lang/System/out Ljava/io/PrintStream; ;Get the fields value
	astore 2			;Store top of stack in 2 (ps)
	aload 2				;Load value stored in 2 (ps)
	iconst_1			;Load constant boolean value 1
	ifeq IsFalse1			;If its 0, go to the code to change it to 1
	iconst_0			;It was 1, so change to 0
	goto NotEnd1			;Exit the not code
IsFalse1:				;Start here to change to 1
	iconst_1			;Change to 1
NotEnd1:				;Exit the not code
	invokevirtual java/io/PrintStream/println(Z)V
	return
.end method
