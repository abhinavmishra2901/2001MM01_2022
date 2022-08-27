def factorial (x):
    fact=1
    for i in range(1,x+1):
        fact=fact*i
    print("The factorial of",x, "is",fact)

    

x=int(input("Enter the number whose factorial is to be found"))
factorial(x)
