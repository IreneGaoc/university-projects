'''
Ask user for temperature in Fahrenheit and convert it to Celsius,
printed to the screen; repeat until user had enough
'''
yn = "y"
while yn!="n":
    # ask for input
    f = input("Please enter temperature in Fahrenheit: ")
    f = float(f)
    # conversion
    c=(f-32)/1.8
    print("Temperature in Celsius:", c )
    print("Temperature in Celsius: {:.2f} {:.4f}".format(c,2*c))
    yn = input("One more conversion? [y/n] ")

print("Bye!")


# print( .. )

