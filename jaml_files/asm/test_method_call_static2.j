.class test_method_call_static2
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method public static getDoub()D
	.limit stack 10
	.limit locals 100
	ldc2_w 10.0			;Load constant numerical value 10.0
	dreturn				;Return from method
.end method
