.class test_invoke_implemented_method3
.super java/lang/Object
.implements test_invoke_implemented_method2
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method public y()I
	.limit stack 10
	.limit locals 100
	ldc 10				;Load constant numerical value 10
	ireturn				;Return from method
	return
.end method
