.class test_super_cons_implicitly_invoked
.super test_super_cons_implicitly_invoked2
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial test_super_cons_implicitly_invoked2/<init>()V
	return
.end method
.method public static main([Ljava/lang/String;)V
	.limit stack 10
	.limit locals 100
	new test_super_cons_implicitly_invoked ;Create a new instance of the class
	dup				;Duplicate the reference
	invokespecial test_super_cons_implicitly_invoked/<init>()V ;Call the constructor
	return
.end method
