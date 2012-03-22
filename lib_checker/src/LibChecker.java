import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Arrays;

/**
 * Used to check the types of Java library classes using Java's reflection
 * capabilities.
 */
public class LibChecker {
        /**
         * Calls the appropriate checker method.
         * 
         * @param args First arg is what should be checked, either:
         *                  "-class", "-cons" (constructor), "-method",
         *                  "-field".
         *             Second is the class name.
         *             Third is the method/field name if needed (it's a list
         *                  of arguments for constructors.
         *             Fourth is a list of arguments if needed.
         */
        public static void main(String[] args) {
                LibChecker checker = new LibChecker();
                if (args[0].equals("-class")) {
                        checker.checkClass(args[1]);
                } else if (args[0].equals("-cons")) {
                        // Extract the arguments section of the array
                        String[] cArgs = Arrays.copyOfRange(args, 2, 
                                                            args.length);
                        checker.checkCons(args[1], cArgs);
                } else if (args[0].equals("-method")) {
                        String[] mArgs = Arrays.copyOfRange(args, 3,
                                                            args.length);
                        checker.checkMethod(args[1], args[2], mArgs);
                } else if (args[0].equals("-field")) {
                    checker.checkField(args[1], args[2]);
                }
        }
        
        /**
         * Simply check for the existence of the class (or interface).
         * 
         * @param cName The name of the class.
         */
        public void checkClass(String cName) {
                try {
                        // This will throw an exception if it cannot be found
                        Class<?> c = Class.forName(cName);
                        System.out.println(c.getName());
                } catch (ClassNotFoundException e) {
                        System.out.println("E - No library class: " + cName);
                }
        }
        
        /**
         * Used to check the constructor with the same parameter types as the
         * ones provided exists.
         * 
         * @param cName The name of the class.
         * @param argNames An array of the types of the arguments.
         */
        public void checkCons(String cName, String[] argNames) {
                try {
                        Class<?> c = Class.forName(cName);
                        // Get the class object for each parameter type
                        Class<?>[] cArgs = new Class<?>[argNames.length];
                        for (int i = 0; i < argNames.length; i++) {
                                cArgs[i] = Class.forName(argNames[i]);
                        }
                        try {
                                // This will throw an exception if it doesn't
                                // exist
                                @SuppressWarnings("unused")
                                Constructor<?> m = c.getConstructor(cArgs);
                                System.out.println(c.getName());
                        } catch (NoSuchMethodException e) {
                                System.out.println("E - Constructor " +
                                                   "parameters incorrect " +
                                                   "for class " +  cName + "!");
                        }
                 } catch (ClassNotFoundException e) {
                         System.out.println("E - No library class: " + cName +
                                            "!");
                 }
        }
        
        /**
         * Used to check a method exists with the same signature in the full
         * inheritance tree of the current class.  It prints out the return
         * type of the method (if found).
         * 
         * @param cName The name of the class.
         * @param mName The name of the method.
         * @param argNames The types of the method parameters.
         */
        public void checkMethod(String cName, String mName, String[] argNames) {
                try {
                        // Works in the same way as the above method
                        Class<?> c = Class.forName(cName);
                        Class<?>[] mArgs = new Class<?>[argNames.length];
                        for (int i = 0; i < argNames.length; i++) {
                                mArgs[i] = Class.forName(argNames[i]);
                        }
                        try {
                                // getMethod will search through the full
                                // inheritance tree for it (inc. interfaces)
                                Method m = c.getMethod(mName, mArgs);
                                // Print the return type
                                Class<?> type = m.getReturnType();
                                System.out.println(type.getName());
                        } catch (NoSuchMethodException e) {
                                System.out.println("E - No method: " + mName +
                                                   ". Or parameter types " +
                                                   "were incorrect!");
                        }
                 } catch (ClassNotFoundException e) {
                         System.out.println("E - No library class: " + cName +
                                            "!");
                 }
        }
        
        /**
         * Searches for a field in the full inheritance tree of the class and
         * prints out its type if it's found.
         * 
         * @param cName The name of the class.
         * @param fName The name of the field.
         */
        public void checkField(String cName, String fName) {
                try {
                        Class<?> c = Class.forName(cName);
                        try {
                                // Get the field and print its type
                                Field m = c.getField(fName);
                                Class<?> type = m.getType();
                                System.out.println(type.getName());
                        } catch (NoSuchFieldException e) {
                                System.out.println("E - No field: " + fName +
                                                   "!");
                        }
                 } catch (ClassNotFoundException e) {
                         System.out.println("E - No library class: " + cName +
                                            "!");
                 }
        }
}
