def hexadigit2int(hdigit):
   '''
   Takes a single hexa digit and returns the underlying integer.

   Args:
      hdigit:  hexa digit, i.e., '0',...',9', 'A',...,'F', or
               'a',...,'f'
   Returns:
      returns the integer value of the hdigit passed
   '''
   # hdigit += 1
   # Homework: Use a dictionary to get rid of the ifs
   if hdigit.isdigit():
      return int(hdigit)
   else:
      hdigit = hdigit.lower()
      if 'a'<=hdigit and hdigit<='f':
         return ord(hdigit)-ord('a')+10
   raise ValueError("Incorrect digit: '%s'" % hdigit)


def hexa2int(hexastring):
   power16 = 1
   s = 0
   for i in range(len(hexastring)):
      s += power16 * hexadigit2int( hexastring[-(i+1)] )
      power16 *= 16
   return s

while True:
   try:
      hexastring = input("Please entra hexadecimal integer: ")
      print(hexa2int(hexastring))
      break
   except ValueError as exc:
      print("Ooops, incorrect input!")
      print(exc)
