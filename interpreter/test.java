{
	int a = 1;
	print a;
	int b = 1;
	print b;
	for (int i = 0; i < 100; i = i + 1) {
		int c = a + b;
		print c;
		a = b;
		b = c;
	}
}