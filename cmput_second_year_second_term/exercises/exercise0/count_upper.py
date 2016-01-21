'''
name: Zihan(Irene) Gao
section: cmput275 B2
title: exercise0: count _upper
created date: 2016/jan/09
purpose:
    Write code that reads from the standard input a string and prints the number of
    upper-case characters in the string to the standard output.
'''
# input a string
a_String= input()

# let c be the counter to count the number of upper-case characters in the string
# let i be the characters in the string
c = 0
i = 0
for i in range(len(a_String)):
    if a_String[i].isupper():
        c +=1
print(c)
