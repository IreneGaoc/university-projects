import random
list_of_n = [0,1,1,1,2,2,2,2,3,3,3,3,100]
for i in range(100):
   list_of_n.append( random.randrange(101) )

for i,n in enumerate(list_of_n):
   with open("test%i-stdin.txt" % i,mode='w') as f:
      print(n,file=f)
      # generate examples with given asnwers
      # ranging from 0 to n
      c = random.randrange(n+1)
      ex = []
      # add good examples with enough room
      for j in range(c):
         q = random.randrange(2,101)
         p = random.randrange(0,q-2+1)
         ex.append( (p,q) )
      for j in range(c,n):
         q = random.randrange(2,101)
         p = random.randrange(q-2,q+1)
         ex.append( (p,q) )
      random.shuffle(ex)
      for (p,q) in ex:
         print( p, q, file=f)
