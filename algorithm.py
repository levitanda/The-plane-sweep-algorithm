#import modules
import mod

def parsing_single_testcase(file, segments):
    num_segments = int(file.readline())
    for id in range(num_segments):
        x1, y1, x2, y2 = map(float, file.readline().split())
        p = mod.Point(x1, y1)
        q = mod.Point(x2, y2)
        segment = mod.Segment(id,p,q)
        segments.append(segment)

def event_queue_initialization(segments, event_priority_queue):
    for seg in segments:
        #0 - beggining of segment, 1 - ending of segment
        event_priority_queue.insert((seg,0), seg.q.x)
        event_priority_queue.insert((seg,1), seg.p.x)

def sweep(events):
    status = None
    while not events.empty():
        ev = events.delete()
        if(ev[1] == False):
            #add_if_intersection
            mod.deleteNode(status, ev[0].id)



def main():
    filename = "input.txt"
    print("starting parsing...")
    with open(filename, "r") as file:
        num_test_cases = int(file.readline())
        print("num of test cases ", num_test_cases)
        for i in range(num_test_cases):
            segments = []
            parsing_single_testcase(file, segments)
            event_priority_queue = mod.CG24PriorityQueue()
            event_queue_initialization(segments, event_priority_queue)
            print("the tast case # ",i)
            counter = 0
            sweep_line_status = mod.SegmentBST()
            while not event_priority_queue.empty():
                s = event_priority_queue.pop()
                if s[1]==0: #segment begin
                    print(s[0].q.x, s[0].id)
                    sweep_line_status.insert(s[0], s[0].q.x, event_priority_queue)
                elif s[1]==1: #segment finish
                    print(s[0].p.x, s[0].id)
                    sweep_line_status.remove(s[0], s[0].p.x, event_priority_queue)
                elif s[1]==2: #intersection
                    print(s[0].x, s[0].y)
                    counter += 1
                    seg1 = s[2]
                    seg2 = s[3]
                    #sweep_line_status.remove(s[0], s[0].x, event_priority_queue)
                    
            print("intersects num: ", counter)
                    



if __name__ == "__main__":
    main()