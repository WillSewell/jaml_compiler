
public class Matrix {

    public static void main(String[] args) {
        double[][] a1 = {{1, 2, 3},{4, 5, 6}};
        double[][] a2 = {{1, 2, 3},{4, 5, 6}};
        double[][] a3 = new double[a1.length][a1[1].length];
        for (int i = 0; i < a1.length; i++) {
            for (int j = 0; j < a1[1].length; j++) {
                a3[i][j] = a1[i][j] + a2[i][j];
            }
        }
    }
}
