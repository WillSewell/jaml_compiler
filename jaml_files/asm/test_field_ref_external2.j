.class test_field_ref_external2
.super java/lang/Object
.field f Ljava/lang/String;
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	aload_0				;Load the current object to assign to field
	ldc "pass"			;Load constant string "pass" (creats a new String object)
	putfield test_field_ref_external2/f Ljava/lang/String; ;Store into field f
	return
.end method
