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

// import java.util.*;

// public class learn {
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);

//         int x = sc.nextInt();

//         if (x % 2 == 0) {
//             System.out.println("even");
//         } else {
//             System.out.println("odd");
//         }
//     }
// }

// import java.util.*;

// public class learn {
//     public static void main(String[] args) {

//         Scanner sc = new Scanner(System.in);

//         int x = sc.nextInt();
//             if (x % 400==0) {
//                 System.out.println("leap");
//             } else {
//                 System.out.println("not leap yr");
//             }
//      }
// }

// import java.util.*;
// public class learn {
//     public static void main(String[] args ){
//         Scanner sc = new Scanner(System.in);
//         int x = sc.nextInt();
//         int i = 1;
//         for(i=1;i<=100;i++){
//             System.out.println(i);
//         }

//     }
// }

// import java util.*;
// public class learn {
//     public static void main(String[] args){
//         Scanner sc = new Scanner(System.in);
//         int sum =0;
//         int n = sc.nextInt();
//         for (int i=1;i<=n;i++ ){
//             sum = sum + i;
//         }
//         System.out.println("sum="+sum);
//     }
// }

// Multiplication Table using for loop
// import java.util.*;
// public class learn {
//     public static void main (String[]args){
//         Scanner sc = new Scanner(System.in);
//         int n = sc.nextInt();
//         for (int i = 1 ; i<=10; i++){
//             int multiply = n * i;
//             System.out.println(n + " x " + i + " = " + multiply);
//         }
//     }
// }

// Palindrome Number Check using while loop
// import java.util.*;
// public class learn {
//     public static void main (String[]args){
//         Scanner sc = new Scanner(System.in);
//         int n = sc.nextInt();
//         int og = n;
//         int rev = 0;
//         while(n > 0){
//             int digit = n % 10;
//             rev = rev * 10 + digit;
//             n = n / 10;
//         }
//         if (og == rev){
//             System.out.println("palindrome");
//         } else {
//             System.out.println("not palindrome");
//         }
//     }
// }

// Concatenate two HashMaps using putAll()
// class LearnConcatHashMaps {
//     public static void main(String[] args) {
//         Map<String, Integer> map1 = new HashMap<>();
//         map1.put("java", 95);
//         map1.put("python", 90);
//
//         Map<String, Integer> map2 = new HashMap<>();
//         map2.put("javascript", 85);
//         map2.put("python", 92);
//
//         Map<String, Integer> merged = new HashMap<>(map1);
//         merged.putAll(map2);
//         System.out.println("Merged: " + merged);
//     }
// }

// Concatenate Maps with conflict resolution using Map.merge
// class LearnMapMerge {
//     public static void main(String[] args) {
//         Map<String, Integer> scores1 = new HashMap<>();
//         scores1.put("math", 80);
//         scores1.put("science", 90);
//
//         Map<String, Integer> scores2 = new HashMap<>();
//         scores2.put("science", 95);
//         scores2.put("english", 88);
//
//         Map<String, Integer> merged = new HashMap<>(scores1);
//         scores2.forEach((key, val) -> merged.merge(key, val, Integer::sum));
//         System.out.println("Merged with sum: " + merged);
//     }
// }


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

// Constructor and 'this' Keyword Example
// class Car {
//     String brand;
//     int year;
//
//     // Parameterized Constructor
//     Car(String brand, int year) {
//         this.brand = brand;
//         this.year = year;
//     }
//
//     public void displayDetails() {
//         System.out.println("Brand: " + this.brand + ", Year: " + this.year);
//     }
// }
// class LearnConstructors {
//     public static void main(String[] args) {
//         Car car1 = new Car("Tesla", 2024);
//         car1.displayDetails();
//     }
// }

// Word Frequency Counter using HashMap
// class LearnWordCountHashMap {
//     public static void main(String[] args) {
//         String text = "java python java c++ python java";
//         String[] words = text.split(" ");
//         Map<String, Integer> freqMap = new HashMap<>();
//         for (String word : words) {
//             freqMap.put(word, freqMap.getOrDefault(word, 0) + 1);
//         }
//         System.out.println(freqMap);
//     }
// Word Frequency Counter using Java 8 Stream API & Collectors.groupingBy
// class LearnWordCountStreams {
//     public static void main(String[] args) {
//         String sentence = "apple banana apple orange banana apple";
//         Map<String, Long> counts = Arrays.stream(sentence.split(" "))
//             .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
//         System.out.println(counts);
//     }
// Check if Key Exists using Map.containsKey and Map.getOrDefault
// class LearnCheckKeyExistMap {
//     public static void main(String[] args) {
//         Map<String, Integer> scores = new HashMap<>();
//         scores.put("Alice", 95);
//         scores.put("Bob", 88);
//
//         boolean hasAlice = scores.containsKey("Alice");
//         boolean hasCharlie = scores.containsKey("Charlie");
//
//         System.out.println("Alice exists: " + hasAlice);
//         System.out.println("Charlie exists: " + hasCharlie);
//         System.out.println("Charlie score: " + scores.getOrDefault("Charlie", 0));
//     }F
// Key Existence and Value Handling using Optional.ofNullable
// class LearnCheckKeyExistOptional {
//     public static void main(String[] args) {
//         Map<String, String> config = new HashMap<>();
//         config.put("db_host", "localhost");
//
//         Optional<String> host = Optional.ofNullable(config.get("db_host"));
//         Optional<String> port = Optional.ofNullable(config.get("db_port"));
//
//         System.out.println("Host: " + host.orElse("127.0.0.1"));
//         System.out.println("Port: " + port.orElse("5432"));
//     }
// }

// import java.util.*;
// public class function {
//     public static int calculateSum(int a , int b ){
//         int sum = a+b;
//         return sum;
//     }

//     public static void main (String args[]){
//         Scanner sc = new Scanner(System.in);
//         int a = sc.nextInt();
//         int b = sc.nextInt();
//         int sum = calculateSum(a,b);
//         System.out.println(sum);
//     }
// }


// import java.util.*;
// public class function{
//     public static int calculateProduct(int a , int b ){
//         int product = a*b;
//         return product;
//     }

//     public static void main(String args[]){
//         Scanner sc = new Scanner(System.in);
//         int a = sc.nextInt();
//         int b = sc.nextInt();
//         int product = calculateProduct(a,b);
//         System.out.println(product);
//     }
// }

// import java.util.*;
// public class start {
//     public static void calculateFactorial(int n) {
//         if (n<0){
//             System.out.println("invalid no");
//             return ;
//         }
//         int factorial = 1;
//         for (int i=n; i>=1 ; i--)
//         {
//             factorial = factorial * i;
//         }
//         System.out.println(factorial);
//     }
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);
//         int n = sc.nextInt();
//         calculateFactorial(n);
//     }
// }

// import java.util.*;
// public class max {
//     public static int checkMaximum(int a , int b , int c) {  
//         int max = a; 
//         if (b>max){
//             max = b;
//         }
//         if (c>max){
//             max = c; 
//         }
//         return max;
//     }
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);
//         int a = sc.nextInt();
//         int b = sc.nextInt();
//         int c = sc.nextInt();
//         int max = checkMaximum(a,b,c);
//         System.out.println("maximum no"+max);
//     }
// }

// import java.util.*;
// public class rev{
//     public static int revNo(int n) {
//         int rev = 0;
//         while (n>0) {
//             int lastdigit = n % 10;
//             rev = rev * 10 + lastdigit;
//             n = n/10;
//         }
//         return rev;
//     }
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);
//         int n = sc.nextInt();
//         int result = revNo(n);
//         System.out.println("reverse = "+result);
//     }
// }

import java.util.*;
public class GCD{
    public static int calculateGcd(int a , int b){
        if (b==0){
            return a ;
        }
        return calculateGcd(b, a%b);
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        int result = calculateGcd(n,m);
        System.out.println("gcd = "+result);
    }
}

// Java Map Iteration Practice (Day 38)
// class MapIteration {
//     public static void main(String[] args) {
//         Map<String, Integer> map = new HashMap<>();
//         map.put("Alice", 85);
//         map.put("Bob", 92);
//         map.put("Charlie", 78);
//
//         // 1. Iterate over entrySet
//         for (Map.Entry<String, Integer> entry : map.entrySet()) {
//             System.out.println(entry.getKey() + " -> " + entry.getValue());
//         }
//
//         // 2. Iterate using forEach lambda (Java 8+)
//         map.forEach((k, v) -> System.out.println(k + ": " + v));
//     }
// }



















