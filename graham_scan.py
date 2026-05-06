"""
Graham Scan Convex Hull Algorithm
Time Complexity: Θ(n log n)
Space Complexity: Θ(n)

Sort points by polar angle relative to the lowest point, then greedily
build the hull by keeping only left turns using a stack.
"""

import math


def cross_product(o, a, b):
    """
    Returns the cross product of vectors OA and OB.
    Positive = counterclockwise (left turn)
    Negative = clockwise (right turn)
    Zero = collinear
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def distance_sq(a, b):
    """Squared distance between two points (avoids sqrt for comparisons)."""
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def polar_angle(anchor, point):
    """Returns the polar angle from anchor to point using atan2."""
    return math.atan2(point[1] - anchor[1], point[0] - anchor[0])


def graham_scan(points):
    """
    Find the convex hull using Graham Scan.
    
    1. Pick the lowest point (anchor)
    2. Sort all other points by polar angle w.r.t. anchor
    3. Process points in order, maintaining a stack of hull candidates
    4. Pop from stack whenever we detect a right turn (clockwise)
    
    Args:
        points: list of (x, y) tuples
    
    Returns:
        list of (x, y) tuples representing hull vertices in counterclockwise order
    """
    n = len(points)
    if n < 3:
        return sorted(points)

    # Step 1: find the anchor — lowest y, then leftmost x to break ties
    anchor = min(points, key=lambda p: (p[1], p[0]))

    # Step 2: sort the rest by polar angle relative to anchor
    # if same angle, keep the closer one first (farther one stays, closer gets skipped if collinear)
    others = [p for p in points if p != anchor]
    others.sort(key=lambda p: (polar_angle(anchor, p), distance_sq(anchor, p)))

    # handle collinear points at the same angle:
    # for the last group of collinear points (largest angle), we want farthest first
    # so the scan handles them correctly. but for simplicity and correctness on
    # typical inputs, the basic sort above works. the stack logic handles the rest.

    # Step 3: initialize stack with anchor and first sorted point
    stack = [anchor, others[0]]

    # Step 4: process remaining points
    for i in range(1, len(others)):
        # while the last two points on the stack and the new point make a right turn
        # (or are collinear), pop the top
        while len(stack) > 1 and cross_product(stack[-2], stack[-1], others[i]) <= 0:
            stack.pop()
        stack.append(others[i])

    return stack


if __name__ == "__main__":
    # quick sanity check
    test_points = [(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]
    result = graham_scan(test_points)
    print("Graham Scan Hull:", result)
