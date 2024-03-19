
class Point:
    x : float # float
    y : float # float
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    # def
# class

class Segment:
    id : int # to overcome numerical error when we find a point on an ...
    #    # already-known segment we identify segments with unique ID.
    #    # binary search with numerical errors is guaranteed to find an ...
    #    # index whose distance from the correct one is O(1) (here it is 2).
    #
    p : Point # Point, after input we compare and swap to guarantee that p.x <= q.x
    q : Point # Point
    
    def __init__(self,id,p,q):
        if p.x > q.x:
            p,q = q,p
        self.id = id
        self.p = p
        self.q = q
    # def
    
    # line: y = ax + b. it is guaranteed that the line is not vertical (a is finite)
    def a(self): # () -> double
        return ((self.p.y - self.q.y) / (self.p.x - self.q.x))
    # def
    
    def b(self): # () -> double
        return (self.p.y - (self.a() * self.p.x))
    # def
    
    # the y-coordinate of the point on the segment whose x-coordinate ..
    #   is given. Segment boundaries are NOT enforced here.
    def calc(x):
        return (self.a() * (x + self.b()))
    # def
# class

def is_left_turn(a, b, c): # (Point,Point,Point) -> bool
    x1 = a.x
    x2 = b.x
    x3 = c.x
    y1 = a.y
    y2 = b.y
    y3 = c.y
    return ((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))) > 0
# def

def intersection(s1, s2): # (segment,segment) -> Point | None
    if ((is_left_turn(s1.p, s1.q, s2.p) != is_left_turn(s1.p, s1.q, s2.q)) and
        (is_left_turn(s2.p, s2.q, s1.p) != is_left_turn(s2.p, s2.q, s1.q))):
        
        a1 = s1.a()
        a2 = s2.a()

        b1 = s1.b()
        b2 = s2.b()

        # commutation consistency: sort by a (then by b)
        if a1 > a2 or (a1 == a2 and b1 > b2):
            a1,a2 = a2,a1
            b1,b2 = b2,b1
        # if

        #
        # a1 x + b1 = y
        # a2 x + b2 = y
        # (a1 - a2)x + (b1-b2) = 0
        # x = (b2-b1)/(a1-a2)
        #

        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

        return Point(x, y)
    else:
        return None
    #else
#def

def intersects(s1, s2): # (Segment,Segment) -> bool
    return not(intersection(s1, s2) is None)
#def


class CG24PriorityQueue:
    max1 : bool# bool
    max2 : bool # bool
    max3 : bool # bool
    t    : int # int
    arr  : any # any[]

    class cEntry:
        #p   # double
        #p2  # double
        #p3  # double
        #pzm # int
        #data
        def __init__(self):
            pass
    # class
    
    def __init__(self, priorityMax=True, tiebreakerMax=True, tiebreaker2Max=True):
        self.max1 = priorityMax
        self.max2 = tiebreakerMax
        self.max3 = tiebreaker2Max
        self.t    = int(0)
        self.arr  = list()
    # def
    
    def compare(self, l, r): # (p1,p2) -> bool
        if l.p != r.p:
            return (l.p > r.p) if self.max1 else (l.p < r.p)
        if l.p2 != r.p2:
            return (l.p2 > r.p2) if self.max2 else (l.p2 < r.p2)
        if l.p != r.p:
            return (l.p3 > r.p3) if self.max3 else (l.p3 < r.p3)
        return l.pzm < r.pzm;
    # def
    
    def insert(self, data, p, tiebreaker=0, tiebreaker2=0): # (any, double[, double[, double]]) -> void
        entry      = CG24PriorityQueue.cEntry()
        entry.p    = float(p)
        entry.p2   = float(tiebreaker)
        entry.p3   = float(tiebreaker2)
        entry.pzm  = self.t
        entry.data = data
        
        self.t = self.t + int(1)
        self.arr.append(entry)
        # heapify up
        i = int(len(self.arr)) - int(1)
        parent = int(i / 2)
        while i != parent and self.compare(self.arr[i], self.arr[parent]):
            self.arr[i], self.arr[parent] = self.arr[parent], self.arr[i]
            i = parent
            parent = int(i / 2)
    # def
    
    def empty(self): # () -> bool
        return 0 == len(self.arr)
    # def
    
    def pop(self): # () -> any
        if 0 == len(self.arr):
            return self.arr[0] # raise exception
        
        res = self.arr[0].data
        
        if len(self.arr) > 1:
            n = len(self.arr)
            self.arr[0], self.arr[n - 1] = self.arr[n - 1], self.arr[0]
            n = n - 1
            
            i  = 0
            while i < n:
                best = i
                j1 = int(2 * i + 1)
                j2 = int(2 * i + 2)
                if j1 < n and self.compare(self.arr[j1], self.arr[best]):
                    best = j1
                #if
                if j2 < n and self.compare(self.arr[j2], self.arr[best]):
                    best = j2
                #if
                if best == i:
                    break
                #if
                self.arr[i], self.arr[best] = self.arr[best], self.arr[i]
                i = best
            # while
        # if
        self.arr.pop()
        return res
    # def
# class