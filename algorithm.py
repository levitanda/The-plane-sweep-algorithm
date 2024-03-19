import modules

def parsing_single_testcase(file, segments):
    num_segments = int(file.readline())
    for id in range(num_segments):
        x1, y1, x2, y2 = map(int, file.readline().split())
        p = modules.Point(x1, y1)
        q = modules.Point(x2, y2)
        segment = modules.Segment(id,p,q)
        segments.append(segment)

def event_priority_queue(segments, event_priority_queue):
    for seg in segments:
        

def main():
    with open(filename, "r") as file:
        num_test_cases = int(file.readline())
        for _ in range(num_test_cases):
            segments = []
            parsing_single_testcase(file, segments)
            event_priority_queue = modules.CG24PriorityQueue()
            event_gueue_initialization(segments, event_priority_queue)
