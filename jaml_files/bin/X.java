class X {
	public static void main(String[] args) {
		long[] a = new long[5];
	    for (int i = 0; i < 5; i++) {
	        a[i] = i;
	    }
	   	for (int j = 4; j >= 0; j--) {
	   		System.out.println(a[j]);
	   	}
	}
}