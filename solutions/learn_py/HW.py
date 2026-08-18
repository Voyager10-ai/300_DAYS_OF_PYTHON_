import _frozen_importlib_external
# Home Work

# Write a program to input student name and marks of 3 subjects. Print name and percentage in output. 

name = input("Enter your name:")
coa = input("Enter coa marks: ")
ml = input("enter your ML marks" )
dbms = input("enter your dbms marks ")

percentage = (coa+ml+dbms)/300 *100
print(f"{name},have {percentage}%. well done perfect")

