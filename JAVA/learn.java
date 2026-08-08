// public class learn {
//     public static void main(String[] args) {
//         System.out.println("Hello, World!");
//     }
// }


// public class learn{
//     public static void main(String[] args) {
//         System.out.println("*");
//         System.out.println("**");
//         System.out.println("***");
//         System.out.println("****");
//         System.out.println("*****");
//     }
// }


// public class learn{
//     public static void main(String[] args) {
//      // variables
//      String name = "John";
//         double price = 10.99;
//         int age = 21;
//         int a = 25;
//         int b = 10;


//     }
// }

// public class learn {
//     public static void main(String[] args){
//         // Variables
//         int a = 26;
//         int b = 10;
//         int sum = a + b;
//         //System.out.println(sum);
//         int diff = a - b;
//         //System.out.println(diff);
//         int mul = a * b;
//         //System.out.println(mul);
//         int div = a / b;
//         //System.out.println(div);
//         int mod = a % b;
//         // System.out.println(mod);  
//     }
// }


// import java.util.Scanner;

// public class learn {
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);

//         int a = sc.nextInt();  // Reads first integer
//         int b = sc.nextInt();  // Reads second integer

//         int sum = a + b;
//         System.out.println(sum);
//     }
// }

// import java.util.*;

// public class learn {
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);

//         int age = sc.nextInt();

//         if (age >= 18) {
//             System.out.println("Adult");
//         } else {
//             System.out.println("Not Adult");
//         }

//         sc.close();
//     }
// }

import java.util.*;

public class learn {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int x = sc.nextInt();

        if (x % 2 == 0) {
            System.out.println("even");
        } else {
            System.out.println("odd");
        }
    }
}



// Switch statement
// class LearnSwitch {
//     public static void main(String[] args) {
//         int day = 3;
//         switch(day) { case 1: System.out.println("Mon"); break; default: System.out.println("Other"); }
//     }
// }

// For Loop
// class LearnFor {
//     public static void main(String[] args) {
//         for(int i=0; i<5; i++) System.out.println(i);
//     }
// }

// While Loop
// class LearnWhile {
//     public static void main(String[] args) {
//         int i=0;
//         while(i<5) { System.out.println(i); i++; }
//     }
// }

// Do While Loop
// class LearnDoWhile {
//     public static void main(String[] args) {
//         int i=0;
//         do { System.out.println(i); i++; } while(i<5);
//     }
// }

// Break Statement
// class LearnBreak {
//     public static void main(String[] args) {
//         for(int i=0; i<10; i++) { if(i==5) break; System.out.println(i); }
//     }
// }

// Continue Statement
// class LearnContinue {
//     public static void main(String[] args) {
//         for(int i=0; i<10; i++) { if(i%2==0) continue; System.out.println(i); }
//     }
// }

// Array Example
// class LearnArray {
//     public static void main(String[] args) {
//         int[] arr = {1, 2, 3, 4, 5};
//         for(int a : arr) System.out.println(a);
//     }
// }

// 2D Array Matrix Example
// class Learn2DArray {
//     public static void main(String[] args) {
//         int[][] matrix = {
//             {1, 2, 3},
//             {4, 5, 6},
//             {7, 8, 9}
//         };
//         for (int i = 0; i < matrix.length; i++) {
//             for (int j = 0; j < matrix[i].length; j++) {
//                 System.out.print(matrix[i][j] + " ");
//             }
//             System.out.println();
//         }
//     }
// }

// Methods and Overloading Example
// class LearnMethods {
//     public static int calculateSum(int a, int b) {
//         return a + b;
//     }
//     public static double calculateSum(double a, double b) {
//         return a + b;
//     }
//     public static void main(String[] args) {
//         System.out.println("Int sum: " + calculateSum(10, 20));
//         System.out.println("Double sum: " + calculateSum(5.5, 4.5));
//     }
// }

// Classes and Objects Example
// class Student {
//     String name;
//     int age;

//     public void printInfo() {
//         System.out.println("Name: " + this.name + ", Age: " + this.age);
//     }
// }
// class LearnClasses {
//     public static void main(String[] args) {
//         Student s1 = new Student();
//         s1.name = "Alice";
//         s1.age = 20;
//         s1.printInfo();
//     }
// }



