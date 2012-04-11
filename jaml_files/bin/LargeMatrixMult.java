import java.io.PrintStream;

class LargeMatrixMult {
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
                int aRows = A.length;
                int bCols = B[0].length;
                int aCols = A[0].length;
                double[][] C = new double[aRows][bCols];
                for(int i = 0; i < aRows; i++) {
                        for(int j = 0; j < bCols; j++) {
                                for(int k = 0; k < aCols; k++) {
                                        C[i][j] += A[i][k] * B[k][j];
                                }
                        }
                }
                long endTime = System.nanoTime();
                PrintStream ps = System.out;
                ps.println("Took " + Long.toString((endTime - startTime)) + " ns");
        }
}