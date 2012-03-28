.class test_extends_field2
.super java/lang/Object
.field x I
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	aload_0				;Load the current to put into field
	ldc 10				;Load constant numerical value 10
	putfield test_extends_field2/x I ;Store into field x
	return
.end method
