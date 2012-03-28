import java.io.*;
class test_invoke_implemented_method {
        public static void main(String[] args) {
                test_invoke_implemented_method2 x = new test_invoke_implemented_method3();
                int z = x.y();
                PrintStream ps = System.out;
                ps.println(z);
        }
}