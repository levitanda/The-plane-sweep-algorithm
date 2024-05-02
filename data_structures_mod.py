epsilon = 0.0000001 #assume there is at least 0.0000001 difference between sequense events
filename = "in1.in.txt"

class Point:
    x : float # float
    y : float # float
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

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

    def __str__(self): 
        return "id: " + str(self.id) + " p: " + str(self.p) + " q: " + str(self.q)
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
                    if k.x < x:
                        tup = (-k.x,segment.id, last_biggest.id)
                        tup2 = (-k.x, last_biggest.id, segment.id)
                        if (not any(tup == item for item in event_queue.queue)) and (not any(tup2 == item for item in event_queue.queue)):
                            event_queue.put(tup)
            if last_smallest != None:
                l = intersection(segment, last_smallest)
                if l != None:
                    if l.x < x:
                        tup = (-l.x,segment.id,last_smallest.id)
                        tup2 = (-l.x, last_smallest.id, segment.id)
                        if (not any(tup == item for item in event_queue.queue)) and (not any(tup2 == item for item in event_queue.queue)):
                            event_queue.put(tup)
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
            node, neighbour_big, neighbour_small = self.find_node(segment, self.root,x)
            if neighbour_big != None and neighbour_small != None:
                l = intersection(neighbour_big.segment, neighbour_small.segment)
                if l != None:
                    if l.x < x:
                        tup = (-l.x,neighbour_big.segment.id, neighbour_small.segment.id)
                        tup2 = (-l.x, neighbour_small.segment.id, neighbour_big.segment.id)
                        if (not any(tup == item for item in event_queue.queue)) and (not any(tup2 == item for item in event_queue.queue)):
                            event_queue.put(tup)
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
        if segment1.calc(x+epsilon) < segment2.calc(x+epsilon):
            segment1, segment2 = segment2, segment1
        # Node1 segment is above the segment of node2 before the intersection
        node1, bigger_node1, smaller_node1 = self.find_node(segment1, self.root, x)
        node2, bigger_node2, smaller_node2 = self.find_node(segment2, self.root, x)
        # Swap segments in nodes without changing the tree
        if node1 and node2:
            node1.segment, node2.segment = node2.segment, node1.segment
        if node1 != None:
            if bigger_node1 != None:
                l = intersection(bigger_node1.segment, node1.segment)
                if l != None:
                    if l.x < x:
                        tup = (-l.x,bigger_node1.segment.id, node1.segment.id)
                        tup2 = (-l.x,node1.segment.id, bigger_node1.segment.id)
                        if (not any(tup == item for item in event_queue.queue)) and (not any(tup2 == item for item in event_queue.queue)):
                            event_queue.put(tup)
        if node2 != None:
            if smaller_node2 != None:
                l = intersection(smaller_node2.segment, node2.segment)
                if l != None:
                    if l.x < x:
                        tup = (-l.x,smaller_node2.segment.id, node2.segment.id)
                        tup2 = (-l.x,node2.segment.id, smaller_node2.segment.id)
                        if (not any(tup == item for item in event_queue.queue)) and (not any(tup2 == item for item in event_queue.queue)):
                            event_queue.put(tup)
           

    def get_bigger_neighbour(self, root, bigger, x, segment):
        if root.right == None:
            return bigger
        if bigger.segment.calc(x) > root.right.segment.calc(x):
            bigger = root.right
        if root.left != None:
            if bigger.segment.calc(x) > root.left.segment.calc(x):
                bigger = root.left
                return self.get_bigger_neighbour(root.left, bigger, x,segment)
        return self.get_bigger_neighbour(root.right, bigger, x,segment)
    
    def get_smaller_neighbour(self, root):
        if root == None:
            return None
        if root.right == None:
            return root
        else: 
            return self.get_smaller_neighbour(root.right)
        
    def get_bigger_neighbour(self, root):
        if root == None:
            return None
        if root.left == None:
            return root
        else: 
            return self.get_bigger_neighbour(root.left)
        

    def find_node(self, segment, root, x, bigger_neighbour = None, smaller_neighbour = None):
        if root is None:
            return root, bigger_neighbour, smaller_neighbour
        if root.segment.id == segment.id:
            bigger_candidate = self.get_bigger_neighbour(root.right)
            if bigger_candidate != None:
                if bigger_neighbour != None:
                    bigger_neighbour = bigger_neighbour if bigger_neighbour.segment.calc(x) < bigger_candidate.segment.calc(x) else bigger_candidate
                else:
                    bigger_neighbour = bigger_candidate
            smaller_candidate = self.get_smaller_neighbour(root.left)
            if smaller_candidate != None:
                if smaller_neighbour != None:
                    smaller_neighbour = smaller_neighbour if smaller_neighbour.segment.calc(x) > smaller_candidate.segment.calc(x) else smaller_candidate
                else:
                    smaller_neighbour = smaller_candidate
            return root, bigger_neighbour, smaller_neighbour
        #because of python is cutting float numbers and it becomes smaller than real, I need to add any very small number to check this condition
        if segment.calc(x+epsilon) < root.segment.calc(x+epsilon):
            return self.find_node(segment, root.left, x, root, smaller_neighbour)
        return self.find_node(segment, root.right, x, bigger_neighbour, root)
    
