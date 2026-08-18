// public class simple {
//     public static void main(String[] args) {
//         System.out.println("Hello World");
//     }
// }

// public class simple {
//     public static void main(String[] args) {
//         System.out.println("Pradnyesh");
//         int age = 21;
//         System.out.println("age:"+age);
//         System.out.println("CSN");
//     }
// }

// public class simple {
//     public static void main(String[] args) {
//         int a = 10;
//         int b = 12;
//         int sum = a + b;
//         System.out.println("sum:" + sum);
//     }
// }

// public class simple {
//     public static void main(String[] args) {
//         int a = 10;
//         int b = 21;
//         int c = 21;
//         float avg = (a + b + c) / 3.0f;
//         System.out.println("avg:" + avg);
//     }
// }

// public class simple {
//     public static void main(String[] args) {
//         float l = 21.5f;
//         float b = 56.5f;
//         float rectangle_area = l * b;
//         System.out.println("the area of rectangle is : " + rectangle_area);
//     }
// }

// public class simple {
//     public static void main(String[] args) {
//         float r = 12.4f;
//         float pi = 3.14f;
//         float circle_area = pi * r * r;
//         System.out.println("the area of circle is: " + circle_area);
//     }
// }

import java.util.Scanner;

public class simple {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter 1st no :");
        int a = sc.nextInt();
        System.out.println("emter 2nd no :");
        int b = sc.nextInt();

        System.out.println("before swap :"+a);
        System.out.println("before swap :"+b);

        int temp = a ;
        a = b;
        b = temp;

        System.out.println("After swap:"+a);
        System.out.println("after swap "+b);
        
        sc.close();
    }
}

