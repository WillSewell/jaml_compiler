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
	ldc "fst"			;Load constant string "fst" (creats a new String object)
	ldc "snd"			;Load constant string "snd" (creats a new String object)
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String; ;Use the built in concat method of String
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
.end method
