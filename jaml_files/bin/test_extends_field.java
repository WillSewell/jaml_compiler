import java.io.*;
class test_extends_field extends test_extends_field2 {
        public static void main(String[] args) {
                test_extends_field sub = new test_extends_field();
                sub.y();
        }
        void y() {
                PrintStream ps = System.out;
                ps.println(x);
        }
}