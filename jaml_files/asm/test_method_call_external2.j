.class test_method_call_external2
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method public w()F
	.limit stack 10
	.limit locals 100
	ldc 10.1			;Load constant numerical value 10.1
	freturn				;Return from method
.end method
