# # # class Student:
# # #     name = "Dhiren"

# # # s1 = Student()
# # # print(s1.name)
# # # s2 = Student()
# # # print(s2.name)

# # # class cars:
# # #     colour = "red"
# # #     brand = "BMW"

# # # car1 = cars()
# # # print(car1.colour)
# # # print(car1.brand)

# # class student:
# #     def __init__(self, name, Maths, Science, English):
# #         self.name = name
# #         self.Maths = Maths
# #         self.Science = Science
# #         self.English = English
# #     def average(self):
# #         return (self.Maths + self.Science + self.English) / 3

# # s1=student("Dhiren", 90, 80, 70)
# # s2=student("Ramesh", 80, 70, 60)
# # s3=student("Suresh", 70, 60, 50)

# # print("Average marks of", s1.name, "is:", s1.average())
# # print("Average marks of", s2.name, "is:", s2.average())
# # print("Average marks of", s3.name, "is:", s3.average())

# # class bank:
# #     def __init__(self, acc, bal):
# #         self.account_number = acc
# #         self.balance = bal

# #     def debit(self, amount):
# #         self.balance -= amount
# #         print("Amount debited:", amount)
# #         print("New balance:", self.balance)

# #     def credit(self, amount):
# #         self.balance += amount
# #         print("Amount credited:", amount)
# #         print("New balance:", self.balance)

# # acc1=bank("123456", 1000)
# # acc1.debit(1200)

# # acc2=bank("789012", 500)
# # acc2.credit(600)

# # class student:

# #     def __init__(self,name,marks):
# #         self.name = name
# #         self.marks = marks


# # s1=student("Dhiren", 90)
# # del s1.marks
# # print(s1.name)
# # print(s1.marks) # marks attribute has been deleted, so this will raise an AttributeError

# class car:
#     @staticmethod
#     def start():
#         print("Car started")

#     @staticmethod
#     def stop():
#         print("Car stopped")

# class bmw(car): #the INHERITANCE of the car class is done in the bmw class
#     def __init__(self, model):
#         self.model = model

# car1 = bmw("X5")
# car1.start()  # Output: Car started

# class A:
#     varA="Hello from class A"
# class B(A):
#     varB="Hello from class B"
# class C(B):
#     varC="Hello from class C"

# c1 = C()
# print(c1.varA)  # Output: Hello from class A
# #this is an example of multilevel inheritance where class C inherits from class B, 
# # which in turn inherits from class A. 

# class A:
#     varA="Hello from class A"
# class B:
#     varB="Hello from class B"
# class C(A,B):
#     varC="Hello from class C"
# c1 = C()
# print(c1.varA)  # Output: Hello from class A
# #this is an example of multiple inheritance where class C inherits from both class A and class B.

