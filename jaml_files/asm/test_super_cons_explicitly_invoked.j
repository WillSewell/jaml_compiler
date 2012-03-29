.class test_super_cons_explicitly_invoked
.super test_super_cons_explicitly_invoked2
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	ldc "pass"			;Load constant string "pass" (creats a new String object)
	invokespecial test_super_cons_explicitly_invoked2/<init>(Ljava/lang/String;)V
	return
.end method
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	new test_super_cons_explicitly_invoked ;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_super_cons_explicitly_invoked/<init>()V ;Call the constructor
	return
.end method
