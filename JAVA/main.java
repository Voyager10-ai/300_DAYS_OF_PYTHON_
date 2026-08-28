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

// import java.util.*;
// public class begineer{
//     public static int calculateGcd(int a , int b){
//         if (b==0){
//             return a ;
//         }
//         return calculateGcd(b, a%b);
//     }
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);
//         int n = sc.nextInt();
//         int m = sc.nextInt();
//         int result = calculateGcd(n,m);
//         System.out.println("gcd = "+result);
//     }
// }

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

// ARRAYS

// type[] arrayName = new type[size];   _____ syntax 
// type[] arrayName = {1,2,3,4,5,6};

// import java.util.*;
// public class array{
//     public static void main(String[] args) {
//         int marks[] = new int[3];
//         // int marks[] = {97,98,99};
//         // marks[0]=97;
//         // marks[1]=98;
//         // marks[2]=99;
//         System.out.println(marks[0]);
//         System.out.println(marks[1]);
//         System.out.println(marks[2]);

//         for (int i=0;i<3;i++){
//             System.out.println(marks[i]);
//         }
//     }
// }

// import java.util.*;
// public class arrays {
//     public static void main(String[] args) {
//         Scanner sc = new Scanner (System.in);
//             int size = sc.nextInt();
//             int numbers[] = new int[size];

//             //input
//             for (int i=0;i<size;i++){
//                 numbers[i] = sc.nextInt();
//             }

//             //output
//             for (int i=0;i<size;i++){
//                 System.out.println("enter value no "+i);

//             }
//         }
//     }

// -- Linear Search --

// import java.util.*;
// public class array1{
//         public static void main(String[] args) {
//             Scanner input = new Scanner(System.in);
//             int size = input.nextInt();

//             int numbers[] = new int[size];

//             for (int i =0; i<size ; i++){
//                 numbers[i] = input.nextInt();
//             }
//             int x = input.nextInt();

//             for(int i =0 ;i<numbers.length;i++){
//                 if(numbers[i] == x ){
//                     System.out.println("x founf at index"+i);
//                 }
//             }
//         }    
// }

// Take an array of names as input from the user and print them on the screen

// import java.util.*;

// public class array1 {
//     public static void main(String[] args) {
//         Scanner input = new Scanner(System.in);
//         System.out.println("how many friends are there : ");
//         int size = input.nextInt();

//         String names[] = new String[size];

//         for (int i = 0; i < size; i++) {
//             System.out.println("enter your friends name : ");
//             names[i] = input.next();
//         }
//         for (int i = 0; i < names.length; i++) {
//             System.out.println("my friends name is " + names[i]);
//         }

//     }
// }

// Find the max & min number in an array of integers 

// import java.util.*;

// public class Array2 {
//     public static void main(String[] args) {
//         Scanner input = new Scanner(System.in);
//         int size = input.nextInt();
//         int numbers[] = new int[size];

//         for (int i = 0; i < size; i++) {
//             numbers[i] = input.nextInt();
//         }
//         int max = Integer.MIN_VALUE;
//         int min = Integer.MAX_VALUE;

//         for (int i = 0; i < size; i++) {
//             if (numbers[i] > max) {
//                 max = numbers[i];
//             }
//             if (numbers[i] < min) {
//                 min = numbers[i];
//             }

//         }
//         System.out.println("max no is " + max);
//         System.out.println("min no is " + min);
//     }
// }

// 2D ARRAY

// type[]arrayName = new type[rows][columns];
// int[][] numbers = new int[3][4];


// import java.util.*;
// public class TwoDarrays{
//     public static void main(String[] args) 
//     {
//         Scanner sc = new Scanner(System.in);
//         int rows = sc.nextInt();
//         int columns = sc.nextInt();
//         int[][]numbers = new int[rows][columns];
//         // input
//         for (int i = 0 ; i<rows ; i++)
//         {
//             for(int j = 0 ; j<columns ; j++)
//             {
//                 numbers[i][j] = sc.nextInt();
//             }
//         }
//         // output
//         for (int i = 0 ; i<rows ; i++)
//         {
//             for(int j = 0 ; j<columns ; j++)
//                 {
//                 System.out.print(numbers[i][j]+" ");
//                 }
//             System.out.println();
//         }
//     }
// } 


// import java.util.*;
// public class question2D{
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);

//         int rows = sc.nextInt();
//         int columns = sc.nextInt();

//         int[][] numbers = new int[rows][columns];

//         // input
//         for (int i = 0 ; i<rows ; i++){
//             for(int j = 0; j<columns ; j++){
//                 numbers[i][j] = sc.nextInt();
//             }
//             }

//             // no to search
//             int x = sc.nextInt();

//             // Search x 
//             for (int i = 0 ; i<rows ; i++){
//                 for(int j = 0 ; j<columns ; j++){
//                 if (numbers[i][j] == x){

//                     System.out.println("indices:"+i+" "+j);
//                 }
//             }
//             }
//         }
//     }

// Java File Size Practice (Day 42)
// import java.io.File;
// import java.nio.file.Files;
// import java.nio.file.Path;
// import java.nio.file.Paths;
// class FileSizePractice {
//     public static void main(String[] args) throws Exception {
//         File file = new File("README.md");
//         if (file.exists()) {
//             long bytesLegacy = file.length();
//             long bytesNio = Files.size(Paths.get("README.md"));
//             System.out.println("File size (File.length()): " + bytesLegacy + " bytes");
//             System.out.println("File size (Files.size()):  " + bytesNio + " bytes");
//         }
//     }
// }

// Java First N Lines Practice (Day 43)
// import java.io.BufferedReader;
// import java.io.FileReader;
// import java.nio.file.Files;
// import java.nio.file.Paths;
// import java.util.List;
// class FirstNLinesPractice {
//     public static void main(String[] args) throws Exception {
//         String filePath = "README.md";
//         int n = 5;
//         System.out.println("--- Reading First " + n + " Lines via Files.lines() ---");
//         try (var lines = Files.lines(Paths.get(filePath)).limit(n)) {
//             lines.forEach(System.out::println);
//         }
//     }
// }

// Java Longest Word in File Practice (Day 44)
// import java.nio.file.Files;
// import java.nio.file.Paths;
// import java.util.Arrays;
// import java.util.Comparator;
// class LongestWordFilePractice {
//     public static void main(String[] args) throws Exception {
//         String filePath = "README.md";
//         String longest = Files.lines(Paths.get(filePath))
//             .flatMap(line -> Arrays.stream(line.split("\\s+")))
//             .map(word -> word.replaceAll("^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$", ""))
//             .filter(w -> !w.isEmpty())
//             .max(Comparator.comparingInt(String::length))
//             .orElse("");
//         System.out.println("Longest word in " + filePath + ": " + longest + " (length: " + longest.length() + ")");
//     }
// }

// Java Random Line Practice (Day 45)
// import java.nio.file.Files;
// import java.nio.file.Paths;
// import java.util.List;
// import java.util.Random;
// class RandomLinePractice {
//     public static void main(String[] args) throws Exception {
//         String filePath = "README.md";
//         List<String> lines = Files.readAllLines(Paths.get(filePath));
//         if (!lines.isEmpty()) {
//             Random rand = new Random();
//             int index = rand.nextInt(lines.size());
//             System.out.println("Random line (" + (index + 1) + "/" + lines.size() + "): " + lines.get(index));
//         }
//     }
// }

// Java Check Parentheses Practice (Day 46)
// import java.util.Stack;
// class CheckParenthesesPractice {
//     public static boolean isValid(String s) {
//         Stack<Character> stack = new Stack<>();
//         for (char c : s.toCharArray()) {
//             if (c == '(') stack.push(')');
//             else if (c == '{') stack.push('}');
//             else if (c == '[') stack.push(']');
//             else if (c == ')' || c == '}' || c == ']') {
//                 if (stack.isEmpty() || stack.pop() != c) return false;
//             }
//         }
//         return stack.isEmpty();
//     }
//     public static void main(String[] args) {
//         String expr = "{[()]}";
//         System.out.println("Is '" + expr + "' valid? " + isValid(expr));
//     }
// }

// Java Circle Practice (Day 47)
// class CirclePractice {
//     private double radius;
//     public CirclePractice(double radius) {
//         if (radius < 0) throw new IllegalArgumentException("Radius cannot be negative");
//         this.radius = radius;
//     }
//     public double getArea() { return Math.PI * radius * radius; }
//     public double getPerimeter() { return 2 * Math.PI * radius; }
//     public static void main(String[] args) {
//         CirclePractice c = new CirclePractice(7.5);
//         System.out.println("Radius: " + c.radius + ", Area: " + c.getArea() + ", Perimeter: " + c.getPerimeter());
//     }
// }

// Java Convert to Int Practice (Day 48)
// class ConvertToIntPractice {
//     public static int customAtoi(String s) {
//         if (s == null) throw new IllegalArgumentException("Input string is null");
//         s = s.trim();
//         if (s.isEmpty()) throw new IllegalArgumentException("Input string is empty");
//         int sign = 1, idx = 0;
//         if (s.charAt(0) == '-') { sign = -1; idx++; }
//         else if (s.charAt(0) == '+') { idx++; }
//         long res = 0;
//         while (idx < s.length() && Character.isDigit(s.charAt(idx))) {
//             res = res * 10 + (s.charAt(idx) - '0');
//             if (sign * res > Integer.MAX_VALUE) return Integer.MAX_VALUE;
//             if (sign * res < Integer.MIN_VALUE) return Integer.MIN_VALUE;
//             idx++;
//         }
//         return (int) (sign * res);
//     }
//     public static void main(String[] args) {
//         String s = "  -42";
//         System.out.println("String: '" + s + "' -> int: " + customAtoi(s));
//     }
// }

// Java Convert to Roman Practice (Day 49)
// class ConvertToRomanPractice {
//     private static final int[] VALUES = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
//     private static final String[] SYMBOLS = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
//     public static String intToRoman(int num) {
//         if (num < 1 || num > 3999) throw new IllegalArgumentException("Num must be between 1 and 3999");
//         StringBuilder sb = new StringBuilder();
//         for (int i = 0; i < VALUES.length; i++) {
//             while (num >= VALUES[i]) {
//                 num -= VALUES[i];
//                 sb.append(SYMBOLS[i]);
//             }
//         }
//         return sb.toString();
//     }
//     public static void main(String[] args) {
//         int year = 2026;
//         System.out.println("Year " + year + " in Roman Numerals: " + intToRoman(year));
//     }
// }

// Java Get and Print Practice (Day 50)
// import java.util.Scanner;
// class GetAndPrintPractice {
//     private String text;
//     public void getString(Scanner sc) {
//         System.out.print("Enter string: ");
//         this.text = sc.nextLine();
//     }
//     public void printString() {
//         if (this.text != null) {
//             System.out.println(this.text.toUpperCase());
//         }
//     }
//     public static void main(String[] args) {
//         GetAndPrintPractice obj = new GetAndPrintPractice();
//         // Scanner sc = new Scanner(System.in);
//         // obj.getString(sc);
//         // obj.printString();
//     }
// }

import java.util.*;










public class main{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);

    int n = sc.nextInt();
    int[] arr = new int [n];

    for(int i=0;i<n;i++){
      arr[i]=sc.nextInt();
    }
    int max = arr[0];
    
    for (int i=0;i<n;i++){
      if(arr[i]>max){
        max=arr[i];
      }
    }
    System.out.println(max);
  }
}







