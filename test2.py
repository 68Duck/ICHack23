import json
from math import sqrt, sin, cos, pi, atan
import numpy as np



result = '{"name":"admin"}'
result = json.loads(result)

print(result["name"])

class Point(object):
    def __init__(x, y, z):
        self.x = x 
        self.y = y
        self.z = z
    
    def getX():
        return x

    def getY():
        return y

    def getZ():
        return z 

    def getDistance(p2):
        return sqrt((self.x - p2.getX()) ** 2 + (self.y - p2.getY()) ** 2 + (self.z = p2.getZ()) ** 2)

    def getXDiff(p2):
        return self.x - p2.getX()

    def getYDiff(p2):
        return self.y - p2.getY()

    def getZDiff(p2):
        return self.z - p2.getZ()

    def getDirectionDeg(p2):  #gets the direction in degrees from north
        return (atan)


class Board(object):
    def __init__(p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def getTopLeft():
        return p1 

    def getTopRight():
        return p2 

    def getBottomRight():
        return p3 

    def getBottomLeft():
        return p4 

    def getNormalVector():
        v1 = createVector(self.getTopLeft(), self.getBottomRight())
        v2 = createVector(self.getTopRight(), self.getBottomLeft())

        crossProduct = np.cross(v1.getNpArray(), v2.getNpArray())
        return Vector(crossProduct[0], crossProduct[1], crossProduct[2])


def createVector(p1, p2):
    return Vector(p1.getX() - p2.getX(), p1.getY() - p2.getY(), p1.getZ() - p2.getZ())

class Vector(object):
    def __init__(dx, dy, dz):
        self.dx = dx 
        self.dy = dy 
        self.dz = dz 

    def getNpArray():
        return np.array([self.dx, self.dy, self.dz])

    def normalise():
        size = sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        self.dx = self.dx / size
        self.dy = self.dy / size
        self.dz = self.dz / size

def getPointOnScreen(p1, p2, board):
    directionVector = Vector(p1.getXDiff(p2), p1.getYDiff(p2), p1.getZDiff(p2))
    directionVector.normalise()


     


