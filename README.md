# Sweep line algorithm for counting intersections between segments

## Introduction

This project implements a sweep line algorithm for counting number of intersections between segments in Python. 

## Data structures

- **Points**: Saves points on plane by x and y coordinates.
- **Segments**: Saves segments on the plane by saving the start point, end point and id of the segment. 
- **Events Queue**: I used the given data structure of priority queue with light fixes and same additions.
- **Sweep line status**: I built BST based structure for efficient search and maintain of the sweep line status. It saves all segments the sweep line placed on it at the moment, sorted by y coordinate where the sweep line crosses these segments.

## Input
The input is found in a single Ascii file which contains the following data:
1. Number of test cases (a positive integer number n).
2. n sets of segments, each one containing:
- Number of segments (a positive number mi
, 1 ≤ i ≤ n).
- mi segments, each one specified by four (4) point coordinates xi1
,yi1
,xi2
,yi2
.
3. The number -1

## Output
The output contains number of segments intersections per test. Every result ends with newline.

## How to Run

To run the program, follow these steps:

1. Into file mod.py update "filename" variable to contain the ASCII input file. Make sure that the file placed in the same directory with code files.
2. Into file mod.py update "epsilon" variable to contain the minimum difference between variables. It required because the exactly coordinates of intersection points can be infinite numbers.
3. Run the main script using the Python interpreter:

```bash
python algorithm.py
```

## Workflow
1. Line segments are read from input and inserted into the Priority queue (events queue) sorted by their x-coordinate.
2. The sweep line progresses from the right to the left of the plane, starting on the event with biggest x-coordinate.
3. As the sweep line encounters events (segment startpoint, endpoint or intersection point) by popping these events from the event queue, it update the sweep line status and events queue if new intersection was found. 
Also in case of intersection event the counter of intersections is updating and segments are swapping in the sweep line status. 
In case of beggining of new segment the segment adding to sweep line status and if the event is finish of segment - the segment removing from the sweep line status.
4. The algorithm continues until the event queue will be empty.

## Complexity

The complexity of these algorithm depends on these actions:

- **Insertion of segment in BST**: Inserting a segment into the BST has a time complexity of O(log n), where n is the number of segments already in the tree.
- **Removal of segment**: Removing a segment from the BST also has a time complexity of O(log n).
- **Intersection Check**: Checking for intersections between two segments is done in constant time O(1), as it involves simple arithmetic operations.
- **Swap segments if intersect**: Swaping of segments in case of intersection will took O(logn) time as it include the finding of segments we need into BST.

Overall, the algorithm achieves a time complexity of O(n log n), where n is the number of line segments being processed.

