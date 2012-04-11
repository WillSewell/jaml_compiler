import java.io.PrintStream;

class LargeMatrixMultLengths {
        public static void main(String[] args) {
                double[][] A = new double[1000][1000];
                for (int i = 0; i < A.length; i++) {
                        for (int j = 0; j < A[0].length; j++) {
                                A[i][j] = i + j;
                        }
                }
                double[][] B = new double[1000][1000];
                for (int m = 0; m < B.length; m++) {
                        for (int n = 0; n < B[0].length; n++) {
                                B[m][n] = m + n;
                        }
                }
                long startTime = System.nanoTime();
                double[][] C = new double[A.length][B[0].length];
                for(int i = 0; i < A.length; i++) {
                        for(int j = 0; j < B[0].length; j++) {
                                for(int k = 0; k < A[0].length; k++) {
                                        C[i][j] += A[i][k] * B[k][j];
                                }
                        }
                }
                long endTime = System.nanoTime();
                PrintStream ps = System.out;
                ps.println("Took " + Long.toString((endTime - startTime)) + " ns");
        }
}