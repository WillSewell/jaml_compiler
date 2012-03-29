.class test_field_ref_super2
.super java/lang/Object
.field f J
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	aload_0				;Load the current object to assign to field
	ldc 10				;Load constant numerical value 10
	i2l				;Convert left hand side to match the type of the right
	putfield test_field_ref_super2/f J ;Store into field f
	return
.end method
