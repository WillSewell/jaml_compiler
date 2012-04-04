class MatrixMult{
  public static void main(String[] args)  {
    int array[][] = {{5,6,7},{4,8,9}};
    int array1[][] = {{6,4},{5,7},{1,1}};
    int array2[][] = new int[3][3];
    int x= array.length;
    System.out.println("Matrix 1 : ");
    for(int i = 0; i < x; i++) {
      for(int j = 0; j <= x; j++) {
        System.out.print(" "+ array[i][j]);
      }
      System.out.println();
      }  
      int y= array1.length;
      System.out.println("Matrix 2 : ");
      for(int i = 0; i < y; i++) {
        for(int j = 0; j < y-1; j++) {
          System.out.print(" "+array1[i][j]);
        }  
        System.out.println();
      }
// part that actually does the mult below!!
      for(int i = 0; i < x; i++) {
        for(int j = 0; j < y-1; j++) {
          for(int k = 0; k < y; k++){

            array2[i][j] += array[i][k]*array1[k][j];
          }
        }  
      }
// end
      System.out.println("Multiply of both matrix : ");
      for(int i = 0; i < x; i++) {
        for(int j = 0; j < y-1; j++) {
        System.out.print(" "+array2[i][j]);
        }  
      System.out.println();
    }
  }
}