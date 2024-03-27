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
        self.p = p
        self.q = q
        self.id = id
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
    def calc(self, x):
        return (self.a() * x + self.b())
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
    if s1 != None and s2 != None:
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
            y = s1.calc(x)

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
        p : float
        #p2  # double
        #p3  # double
        pzm : int
        data : any
        def __init__(self):
            pass

        def print(self):
            print(self.p)
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
        if l.p3 != r.p3:
            return (l.p3 > r.p3) if self.max3 else (l.p3 < r.p3)
        return l.pzm < r.pzm
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
        # for i in self.arr:
        #     i.print()
        # print("next elem")
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
    

class TreeNode:
    def __init__(self, segment):
        self.segment = segment
        self.left = None
        self.right = None

class SegmentBST:
    def __init__(self):
        self.root = None

    def insert(self, segment, x, event_queue):
        self.root = self._insert_recursive(self.root, segment, event_queue, x)

    def _insert_recursive(self, root, segment, event_queue, x, last_smallest = None, last_biggest = None):
        if root is None:
            if last_biggest != None:
                k = intersection(segment,last_biggest)
                if k != None:
                    event_queue.insert((k,2,segment, last_biggest), k.x)
            if last_smallest != None:
                l = intersection(segment, last_smallest)
                if l != None:
                    event_queue.insert((l,2,segment,last_smallest), l.x)
            return TreeNode(segment)      
        if (segment.calc(x) < root.segment.calc(x)):
            root.left = self._insert_recursive(root.left, segment, event_queue, x, last_smallest, root.segment)
        else:
            root.right = self._insert_recursive(root.right, segment,event_queue, x, root.segment, last_biggest)
        return root
    
    def empty(self):
        return self.root == None

    def remove(self, segment, x, event_queue):
        self.root = self._remove_recursive(self.root, segment, x, event_queue)

    def _remove_recursive(self, root, segment, x, event_queue, parent = None):
        if root is None:
            return None
        if segment.calc(x) < root.segment.calc(x):
            root.left = self._remove_recursive(root.left, segment, x, event_queue, root)
        elif segment.calc(x) > root.segment.calc(x):
            root.right = self._remove_recursive(root.right, segment, x, event_queue, root)
        elif segment.calc(x) == root.segment.calc(x) and segment.id == root.segment.id:
            neighbour_small, neighbour_big = self.get_neighbours(root.left, root.right, parent, root, x)
            if neighbour_big != None and neighbour_small != None:
                l = intersection(neighbour_big.segment, neighbour_small.segment)
                if l != None:
                    event_queue.insert((l,2,neighbour_big.segment, neighbour_small.segment), l.x)
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            min_right = self._find_min(root.right)
            root.segment = min_right.segment
            root.right = self._remove_recursive(root.right, min_right.segment, x, event_queue)    
        return root

    def _find_min(self, root):
        current = root
        while current.left:
            current = current.left
        return current
    
    def get_neighbours(self, left, right, parent, root, x, another_parent = None):
        difs = []
        if left != None:
            difs.append((left,abs(root.segment.calc(x) - left.segment.calc(x))))
        if right != None:
            difs.append((right,abs(root.segment.calc(x) - right.segment.calc(x))))
        if parent != None:
            difs.append((parent,abs(root.segment.calc(x) - parent.segment.calc(x))))
        if another_parent != None:
            difs.append((another_parent,abs(root.segment.calc(x) - another_parent.segment.calc(x))))    
        difs.sort(key=lambda a: a[1], reverse=True)
        if len(difs) >=2:
            return difs[0][0], difs[1][0]
        elif len(difs) >=1: 
            return difs[0][0], None
        else:
            return None, None
    
    def swap_segments(self, segment1, segment2, event_queue,x):
        if segment1.calc(x+0.0000001) < segment2.calc(x+0.0000001):
            segment1, segment2 = segment2, segment1
        # Node1 segment is above the segment of node2 before the intersection
        node1, bigger_node1, smaller_node1 = self.find_node(segment1, self.root, x, self.root.right, self.root.left)
        node2, bigger_node2, smaller_node2 = self.find_node(segment2, self.root, x, self.root.right, self.root.left)
        print(node1, node2)
        # Если оба узла найдены, обменяем местами их данные (сегменты)
        if node1 and node2:
            node1.segment, node2.segment = node2.segment, node1.segment
        neighbour_small, neighbour_big = self.get_neighbours(bigger_node1, node1.left, node1.right, node1, x)
        if neighbour_small != None and node1 != None and neighbour_small != node2:
            l = intersection(neighbour_small.segment, node1.segment)
            if l != None:
                if l.x < x:
                    event_queue.insert((l,2,neighbour_small.segment, node1.segment), l.x)
        neighbour_small, neighbour_big = self.get_neighbours(smaller_node2, node2.left, node2.right, node2, x)
        if node2 != None and neighbour_big != None and neighbour_big != node1:
            l = intersection(node2.segment, neighbour_big.segment)
            if l != None:
                if l.x < x:
                    event_queue.insert((l,2,node2.segment, neighbour_big.segment), l.x)


    def find_node(self, segment, root, x, bigger_neighbour = None, smaller_neighbour = None):
        # Рекурсивный поиск узла по сегменту
        if root is None or root.segment.id == segment.id:
            return root, bigger_neighbour, smaller_neighbour
        #because of python is cutting float numbers and it becomes smaller than real, I need to add any very small number to check this condition
        if segment.calc(x+0.0000000001) < root.segment.calc(x+0.0000000001):
            return self.find_node(segment, root.left, x, root, smaller_neighbour)
        return self.find_node(segment, root.right, x, bigger_neighbour, root)
