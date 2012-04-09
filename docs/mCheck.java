  class mCheck {
        public static void main(String[] args) {
                int aRows = 50;
                int aColumns = 50;
                int bRows = 50;
                int bColumns = 50;
                  if ( aColumns != bRows ) {
                    throw new IllegalArgumentException("A:Rows: " + aColumns + " did not match B:Columns " + bRows + ".");
                  }
                if ( aRows != bRows || aColumns != bColumns) {
                    throw new IllegalArgumentException("A:Rows: " + aColumns + " did not match B:Columns " + bRows + ".");
                  }
          }
  }