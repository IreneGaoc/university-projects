class MinHeap:
    def __init__(self):
        self._array = []

    def add(self,key,value):
        self._array.append( (key,value) )
        self.fix_heap_up( len(self._array)-1 )

    def pop_min(self):
        if not self._array:
            raise RuntimeError("Attempt to call pop_min on empty heap")
        r = self._array[0] #??
        l = self._array[-1]
        del self._array[-1]
        if self._array:
            self._array[0] = l
            self.fix_heap_down(0)
        return r

    def fix_heap_up(self,i):
        if self.isroot(i):
            return
        p = self.parent(i)
        if self._array[i][0]<self._array[p][0]:
            self.swap(i,p)
            self.fix_heap_up(p)

    def swap(self,i,j):
        self._array[i],self._array[j] = \
            self._array[j],self._array[i]

    def isroot(self,i):
        return i==0

    def isleaf(self,i):
        return self.lchild(i)>=len(self._array)

    def lchild(self,i):
        return 2*i+1

    def rchild(self,i):
        return 2*i+2

    def parent(self,i):
        return (i-1)//2

    def min_child_index(self,i):
        l = self.lchild(i)
        r = self.rchild(i)
        retval = l
        if r<len(self._array) and self._array[r][0]<self._array[l][0]:
            retval = r
        return retval

    def isempty(self):
        return len(self._array)==0

    def fix_heap_down(self,i):
        if self.isleaf(i):
            return

        j = self.min_child_index(i)
        if self._array[i][0]>self._array[j][0]:
            self.swap(i,j)
            self.fix_heap_down(j)
