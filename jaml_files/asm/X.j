.class X
.super java/lang/Object
.method <init>()V
	.limit stack 10
	.limit locals 100
	aload_0				;Load the current object
	invokespecial java/lang/Object/<init>()V
	return
.end method
.method public x()V
	.limit stack 10
	.limit locals 100
	ldc 6				;Load constant numerical value 6
	multianewarray [[D 2		;Construct a new multidimensional array
	astore 1			;Store top of stack in 1 (A)
	ldc 6				;Load constant numerical value 6
	multianewarray [[D 2		;Construct a new multidimensional array
	astore 2			;Store top of stack in 2 (B)
	aload 1				;Load value stored in 1 (A)
	dup				;Duplicate to get row and col lengths
	arraylength			;Get rows length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 4			;Store length
	iconst_0			;Index into first dimension
	aaload				;Load second dimension
	arraylength			;Get cols length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 5			;Store length
	multianewarray [[D 2		;Construct a new array to store result
	astore 6			;Store the result array
	istore 7			;Store index
	istore 8			;Store index
MatRowStart0:				;Start of loop through rows
	iload 7				;Load index
	iload 4				;Get row length
	if_icmpge MatRowEnd0		;Check if idx has reached the size of the rows
MatColStart0:				;Start of loop through rows
	iload 8				;Load index
	iload 5				;Get row len
	if_icmpge MatColEnd0		;Check if idx has reached the size of the cols
	aload 6				;Load the result matrix
	iload 7				;Load row index
	aaload				;Load matrix row
	iload 8				;Load col index
	aload 1				;Load value stored in 1 (A)
	iload 7				;Load row index
	aaload				;Load matrix row
	iload 8				;Load col index
	daload				;Load current matrix element
	aload 2				;Load value stored in 2 (B)
	iload 7				;Load row index
	aaload				;Load matrix row
	iload 8				;Load col index
	daload				;Load current matrix element
	dadd				;Add both element values
	dastore				;Store result in new array
	iinc 8 1			;Increment the index
	goto MatColStart0		;Return to start of inner loop
MatColEnd0:				;End of the inner loop
	iinc 7 1			;Increment the index
	goto MatRowStart0		;Return to start of inner loop
	iinc 7 1			;Increment the index
MatRowEnd0:				;End of the inner loop
	aload 6				;Leave the result matrix on the stack
	astore 3			;Store top of stack in 3 (C)
	return
.end method
