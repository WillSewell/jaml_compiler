.class test_extends_method2
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method y()J
	.limit stack 10
	.limit locals 100
	ldc 10				;Load constant numerical value 10
	i2l				;Convert left hand side to match the type of the right
	lreturn				;Return from method
.end method
