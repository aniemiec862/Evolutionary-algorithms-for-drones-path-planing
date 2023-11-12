from math import sqrt

class Point2d:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def count_distance(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    @staticmethod
    def add(a, b):
        return Point2d(a.x + b.x, a.y + b.y)

    @staticmethod
    def sub(a, b):
        return Point2d(a.x - b.x, a.y - b.y)

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y

    @staticmethod
    def hypot2(a, b):
        return Point2d.dot(Point2d.sub(a, b), Point2d.sub(a, b))

    @staticmethod
    def proj(a, b):
        k = Point2d.dot(a, b) / Point2d.dot(b, b)
        return Point2d(k * b.x, k * b.y)

    @staticmethod
    def distance_segment_to_point(segment_p1, segment_p2, external_point):
        AC = Point2d.sub(external_point, segment_p1)
        AB = Point2d.sub(segment_p2, segment_p1)

        # Get point D by taking the projection of AC onto AB then adding the offset of A
        D = Point2d.add(Point2d.proj(AC, AB), segment_p1)

        # Calculate AD vector
        AD = Point2d.sub(D, segment_p1)

        # D might not be on AB so calculate k of D down AB (aka solve AD = k * AB)
        # We can use either component, but choose the larger value to reduce the chance of dividing by zero
        k = (AD.x / AB.x) if abs(AB.x) > abs(AB.y) else (AD.y / AB.y)

        # Check if D is off either end of the line segment
        if k <= 0.0:
            return sqrt(Point2d.hypot2(external_point, segment_p1))
        elif k >= 1.0:
            return sqrt(Point2d.hypot2(external_point, segment_p2))
        else:
            return sqrt(Point2d.hypot2(external_point, D))
