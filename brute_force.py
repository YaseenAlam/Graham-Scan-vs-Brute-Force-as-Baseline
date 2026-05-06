"""
Brute Force Convex Hull Algorithm
Time Complexity: Θ(n³)
Space Complexity: Θ(n)

For every pair of points, check if all other points lie on the same side
of the line formed by that pair. If yes, that edge is on the hull.
"""

def cross_product(o, a, b):
    """
    Returns the cross product of vectors OA and OB.
    Positive = counterclockwise (left turn)
    Negative = clockwise (right turn)
    Zero = collinear
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def brute_force_hull(points):
    """
    Find the convex hull using brute force edge checking.
    
    For each pair of points (p_i, p_j), we check whether ALL other points
    are on the same side of the line through p_i and p_j. If they are,
    that directed edge is part of the convex hull.
    
    Args:
        points: list of (x, y) tuples
    
    Returns:
        list of (x, y) tuples representing hull vertices in counterclockwise order
    """
    n = len(points)
    if n < 3:
        return sorted(points)

    # find all directed hull edges
    hull_edges = []

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            p_i = points[i]
            p_j = points[j]

            # check if all other points are on the left side (or on the line)
            all_left = True
            for k in range(n):
                if k == i or k == j:
                    continue
                cp = cross_product(p_i, p_j, points[k])
                if cp < 0:
                    # point is on the right side -> this edge is not a hull edge
                    all_left = False
                    break

            if all_left:
                hull_edges.append((p_i, p_j))

    if not hull_edges:
        return sorted(points)

    # chain the edges together to get ordered hull vertices
    # start from the first edge and follow the chain
    edge_map = {}
    for (a, b) in hull_edges:
        edge_map[a] = b

    hull = []
    start = hull_edges[0][0]
    current = start

    for _ in range(len(edge_map)):
        hull.append(current)
        if current not in edge_map:
            break
        current = edge_map[current]
        if current == start:
            break

    return hull


if __name__ == "__main__":
    # quick sanity check
    test_points = [(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]
    result = brute_force_hull(test_points)
    print("Brute Force Hull:", result)
