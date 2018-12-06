import math

# In this file, a few different algorithms have been implemented.
# These sometimes get uses in asteroids.py


def sign(x):
    # Helper function, returns the sign of x.
    if x >= 0:
        return 1
    else:
        return -1


# Bresenham's Line algorithm!
# Generates a list of integer points which most closes follow the line
# given by (x0,y0) and (x1,y1.
# Returned points are ordered
# (x0,y0) -> (x1,y1)
def line(x0, y0, x1, y1):
    # Change in X and Change in Y, used int the Mathematics.
    dx = x1 - x0
    dy = y1 - y0

    points = [(x0, y0)]

    # Step in X and Step in Y
    sx = sign(dx)
    sy = sign(dy)

    # Bresenham's Requires that a line be drawn with slope of less than one.
    # for cases where isn't true (i.e Delta Y > Delta X), the line is drawn
    # using x wrt. y instead.
    if abs(dx) >= abs(dy):
        # These Coefficients are gotten by transforming the the equation
        # y = mx + b, and transforming it into
        # f(x,y) = y - mx - b = 0
        # Then the fractional part of m is multiplied out onto y and b, and the coefficients are
        # reassigned as
        # g(x,y) = Ay +Bx + C = 0
        # D is the "Decision" Parameter, gotten by computer the error at the midpoint of
        # x_(i+1) = x_i + 1 and y_(i+1) = y_i + 1 or y_i based on decision parameter.
        # Multiplied out by a factor of 2, to remove fractions.
        A = abs(dx)
        B = -abs(dy)
        D = A + 2 * B

        x = x0
        y = y0

        # P and Q are the change in the Decision parameter which occur when you made a Decision.
        # Of course since there are two cases in your decision, thee must be two differences.
        # D_i+2 - D_i+1 = Delta D, P or Q.
        P = 2 * (A + B)
        Q = 2 * B

        # Now until we reach the end, keep updating the decision parameter and draw the line!
        while x != x1:
            x += sx
            if D < 0:
                y += sy
                D += P
            else:
                D += Q
            points.append((x, y))
    else:
        # Reverse the x's and y's above, otherwise identical.
        A = abs(dy)
        B = -abs(dx)
        D = A + 2 * B

        x = x0
        y = y0

        P = 2 * (A + B)
        Q = 2 * B

        while y != y1:
            y += sy
            if D < 0:
                x += sy
                D += P
            else:
                D += Q
            points.append((x, y))
    return points


# Bresenham's Midpoint Circle Algorithm, implemented in Python.
# It is very similar in idea to the line algorithm, by using a decision parameter and drawing a circle.
# using it.
# Returns a list of points, which is the rasterized circle drawn counterclockwise starting from x=r, y=0
def circle(x0, y0, r):
    points = []

    # Integer calculations of the decision parameter d. This requires multiple pages of
    # proof to demonstrate why these numbers are used.
    d = 3 - 2 * int(r)
    x = int(r)
    y = 0

    # Computing the first octant.
    while x >= y:
        points.append((x, y))

        if d > 0:
            d += 4 * (y - x) + 10
            x -= 1
        else:
            d += 4 * y + 6
        y += 1

    # Flipped around x,y Don't include the last point if x=y
    # To maintain counter clockwise, iterated in reverse.
    x, y = points[-1]
    if x != y:
        # print("X != Y")
        flipped_points = [(y, x) for x, y in points[::-1]]
    else:
        # print("X == Y")
        flipped_points = [(y, x) for x, y in points[-2::-1]]
    quarter_circle = points + flipped_points

    # Now do the circle, reflected over y axis.
    flipped_points = [(-x, y) for x, y in quarter_circle[-2::-1]]
    half_circle = quarter_circle + flipped_points

    # Now do the bottom half circle.
    flipped_points = [(x, -y) for x, y in half_circle[-2:0:-1]]
    completed_circle = half_circle + flipped_points

    # We finally return the translated circle!
    return [(x + x0, y + y0) for x, y in completed_circle]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nearest = None
        self.distance = math.inf  # Actually distance squared, makes math faster.

    def update_nearest(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        new_distance = dx*dx + dy*dy
        if new_distance < self.distance:
            self.distance = new_distance
            self.nearest = other


def prims_algorithm(euclidian_points):
    # Computes the minimum spanning tree using a greedy algorithm! Runs in O(n^2) time. ( And O(n) space )
    # There are faster algorithm's in theory, but because the number of points is fairly small,
    # the asymptotic complexity is less relevant.

    # Technically this can be done in O(n*log(log(n))) average time.
    # using Borůvka's algorithm and Delaunay triangulation.
    # which are derived from very complicated math on the plane.

    # The last point is always chosen as the first point in the graph.

    # Edge case of nothing being passed.
    if not euclidian_points:
        return []

    disjoint = [Point(x, y) for x, y in euclidian_points]
    newest_point = disjoint.pop()
    minimum_spanning = [newest_point]

    while disjoint:
        # First, Update all points with the newest added to the tree
        for point in disjoint:
            point.update_nearest(newest_point)

        # Now find the point with the minimum distance from the tree and connect it to it.
        closest_point = disjoint[0]
        closest_index = 0
        for i, point in enumerate(disjoint[1:], start=1):
            if point.distance < closest_point.distance:
                closest_point = point
                closest_index = i

        # We do a fancy swap before the pop to make sure this is friendly on memory.
        # the arrangement of disjoint is irrelevant to the algorithm.
        disjoint[-1], disjoint[closest_index] = disjoint[closest_index], disjoint[-1]

        newest_point = disjoint.pop()
        minimum_spanning.append(newest_point)
    return minimum_spanning


""" Slower Algorithm for circles, not as accurate, much simpler to reason about.
def circle(x0, y0, r):
    # points = np.zeros((int(2*math.pi + 4), 2))
    points = []

    # First generate arounds 0,0, translate after
    x = int(r)
    y = 0
    r2 = r*r

    while(x >= y):
        points.append((x,y))
        y += 1
        if x*x + y*y >= r2:
            x -= 1

    # Flipped around x,y Don't include the last point if x=y
    # To maintain counter clockwise, iterated in reverse.
    x,y = points[-1]
    if x != y:
        # print("X != Y")
        flipped_points = [ (y,x) for x,y in points[::-1] ]
    else:
        # print("X == Y")
        flipped_points = [ (y,x) for x,y in points[-2::-1] ]
    quarter_circle = points + flipped_points

    # Now do the circle, reflected over y axis.
    flipped_points = [(-x, y) for x,y in quarter_circle[-2::-1]]
    half_circle = quarter_circle + flipped_points

    # Now do the bottom half circle.
    flipped_points = [(x, -y) for x,y in half_circle[-2:0:-1]]
    circle = half_circle + flipped_points

    return circle
"""
