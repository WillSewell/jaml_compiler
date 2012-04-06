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
	ldc 5				;Load constant numerical value 5
	ldc 5				;Load constant numerical value 5
	multianewarray [[D 2		;Construct a new multidimensional array
	astore 2			;Store top of stack in 2 (A)
	ldc 5				;Load constant numerical value 5
	ldc 5				;Load constant numerical value 5
	multianewarray [[D 2		;Construct a new multidimensional array
	astore 3			;Store top of stack in 3 (B)
	aload 2				;Load value stored in 2 (A)
	arraylength			;Get rows length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 5			;Store length
	aload 3				;Load value stored in 3 (B)
	iconst_0			;Index into first dimension
	aaload				;Load second dimension
	arraylength			;Get cols length
	dup				;Dup to specify dimensions for the result array as well as storing
	istore 6			;Store length
	multianewarray [[D 2		;Construct a new array to store result
	astore 7			;Store the result array
	iconst_0			;Load 0
	istore 8			;Store index
MatRowStart0:				;Start of loop through rows
	iload 8				;Load index
	iload 5				;Get row length
	if_icmpge MatRowEnd0		;Check if idx has reached the size of the rows
	iconst_0			;Load 0
	istore 9			;Set loop index to 0
MatColStart0:				;Start of loop through rows
	iload 9				;Load index
	iload 6				;Get row len
	iconst_1			;Load 1 to subtract from length
	isub				;Subtract 1 because it loops to one less than the length
	if_icmpge MatColEnd0		;Check if idx has reached the size of the cols
	iconst_0			;Load 0
	istore 10			;Set loop index to 0
MatCellStart0:				;Start of loop through rows
	iload 10			;Load index
	iload 6				;Get row len
	if_icmpge MatCellEnd0		;Check if idx has reached the size of the cols
	aload 7				;Load the result matrix
	iload 8				;Load row index
	aaload				;Load matrix row
	iload 9				;Load col index
	dup2				;Duplicate the array and its index so that one can be used to load the elementand one can be used to store into at the end
	daload				;Load the array element to add to the result of the multiplication
	aload 2				;Load value stored in 2 (A)
	iload 8				;Load row index
	aaload				;Load matrix row
	iload 10			;Load col index
	daload				;Load current matrix element
	aload 3				;Load value stored in 3 (B)
	iload 10			;Load row index
	aaload				;Load matrix row
	iload 9				;Load col index
	daload				;Load current matrix element
	dmul				;Mul element values
	dadd				;Add multiplied values to what is already in the result array
	dastore				;Store result in new array
	iinc 10 1			;Increment the index
	goto MatCellStart0		;Return to start of inner loop
MatCellEnd0:				;End of the inner loop
	iinc 9 1			;Increment the index
	goto MatColStart0		;Return to start of middle loop
MatColEnd0:				;End of the middle loop
	iinc 8 1			;Increment the index
	goto MatRowStart0		;Return to start of inner loop
MatRowEnd0:				;End of the inner loop
	aload 7				;Leave the result matrix on the stack
	astore 4			;Store top of stack in 4 (C)
	return
.end method
