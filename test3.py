import numpy as np
from math import sqrt
import math
from flask import g,Flask,render_template,request,make_response

app = Flask(__name__)

x = 0
y = 0
xScaleFactor = 1
yScaleFactor = 1

@app.route("/sendDot", methods = ["POST"])
def sendDot():
    data = request.get_json()
    print(data)
    if data is None:
        pass 
    else:
        if len(data) > 1:
            global x, y
            x = int(data[0])
            y = int(data[1])
        return ("nothing")

@app.route("/")
def homePage():
    return render_template("index.html")


@app.route("/requestUpdate", methods=["POST"])
def requestUpdate():
    global x, y
    return str(x) + "," + str(y)

@app.route("/dot")
def test():
    return render_template("dot.html", xPercentage = x + 50, yPercentage = y + 50)
 

if __name__ == "__main__":
    app.run(host="localhost", port = 8000)

def recieve(xInput, yInput, z):
    if (xInput > 0):
        x += xScaleFactor
    elif (xInput < 0):
        x -= xScaleFactor
    if (yInput > 0):
        y += yScaleFactor
    elif (yInput < 0):
        y -= yScaleFactor
    


class Point(object):
    def __init__(self, x, y, z):
        self.x = x 
        self.y = y
        self.z = z
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z 

    def getDistance(self,p2):
        return sqrt((self.x - p2.getX()) ** 2 + (self.y - p2.getY()) ** 2 + (self.z - p2.getZ()) ** 2)

    def getXDiff(self,p2):
        return self.x - p2.getX(self)

    def getYDiff(self,p2):
        return self.y - p2.getY(self)

    def getZDiff(self,p2):
        return self.z - p2.getZ(self)

    # def getDirectionDeg(p2):  #gets the direction in degrees from north
    #     return (atan)

    def getNpArray(self):
        return np.array([self.x, self.y, self.z])

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)


class Board(object):
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def getTopLeft(self):
        return self.p1 

    def getTopRight(self):
        return self.p2 

    def getBottomRight(self):
        return self.p3 

    def getBottomLeft(self):
        return self.p4 

    def getNormalVector(self):
        v1 = createVector(self.getTopLeft(), self.getBottomRight())
        v2 = createVector(self.getTopRight(), self.getBottomLeft())

        crossProduct = np.cross(v1.getNpArray(), v2.getNpArray())
        return Vector(crossProduct[0], crossProduct[1], crossProduct[2])


def createVector(p1, p2):
    return Vector(p1.getX() - p2.getX(), p1.getY() - p2.getY(), p1.getZ() - p2.getZ())

class Vector(object):
    def __init__(self, dx, dy, dz):
        self.dx = dx 
        self.dy = dy 
        self.dz = dz 

    def getNpArray(self):
        return np.array([self.dx, self.dy, self.dz])

    def getDx(self):
        return self.dx 

    def getDy(self):
        return self.dy 

    def getDz(self):
        return self.dz

    def getXDiff(self, v2):
        return self.dx - v2.getDx()

    def getYDiff(self, v2):
        return self.dy - v2.getDy()

    def getZDiff(self, v2):
        return self.dz - v2.getDz()

    def getMagnitude(self):
        return sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)

    def normalise(self):
        size = sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)
        self.dx = self.dx / size
        self.dy = self.dy / size
        self.dz = self.dz / size

    def __str__(self):
        return str(self.dx) + "," + str(self.dy) + "," + str(self.dz)


def vec(v1, v2, v3, v4, v5):
    plane = Board(Point(v1.getDx(), v1.getDy(), v1.getDz()),
    Point(v2.getDx(), v2.getDy(), v2.getDz()),
    Point(v3.getDx(), v3.getDy(), v3.getDz()),
    Point(v4.getDx(), v4.getDy(), v4.getDz()))

    normalVector = plane.getNormalVector()
    pointOnPlane = plane.getTopLeft()
    # p5 = Point(v5.getDx(), v5.getDy(), v5.getDz())

    d = np.dot(normalVector.getNpArray(), pointOnPlane.getNpArray())
    print(np.dot(v5.getNpArray(), normalVector.getNpArray()))
    llamda = d / np.dot(v5.getNpArray(), normalVector.getNpArray())

    x = llamda * v5.getDx()
    y = llamda * v5.getDy()
    z = llamda * v5.getDz()

    point = Point(x, y, z)

    topLineVector = Vector(v1.getXDiff(v2), v1.getYDiff(v2), v1.getZDiff(v2))
    # print(topLineVector)
    # print(point)
    # crossP = np.cross(point.getNpArray(), topLineVector.getNpArray())
    # print(crossP)
    # numerator = Vector(crossP[0], crossP[1], crossP[2]).getMagnitude()

    # yDistance = abs(numerator) / topLineVector.getMagnitude()

    llamda = (topLineVector.getDx() * (x - v1.getDx()) + topLineVector.getDy() * (y - v1.getDy()) + topLineVector.getDz() * (z - v1.getDz())) / (topLineVector.getMagnitude() ** 2)
    lineX = v1.getDx() + llamda * topLineVector.getDx()
    lineY = v1.getDy() + llamda * topLineVector.getDy()
    lineZ = v1.getDz() + llamda * topLineVector.getDz()
    linePoint = Point(lineX, lineY, lineZ)
    yDistance = linePoint.getDistance(Point(v1.getDx(), v1.getDy(), v1.getDz()))
    print(yDistance)


      
    leftLineVector = Vector(v1.getXDiff(v4), v1.getYDiff(v4), v1.getZDiff(v4))

    llamda = (leftLineVector.getDx() * (x - v1.getDx()) + leftLineVector.getDy() * (y - v1.getDy()) + leftLineVector.getDz() * (z - v1.getDz())) / (leftLineVector.getMagnitude() ** 2)
    lineX = v1.getDx() + llamda * leftLineVector.getDx()
    lineY = v1.getDy() + llamda * leftLineVector.getDy()
    lineZ = v1.getDz() + llamda * leftLineVector.getDz()
    linePoint = Point(lineX, lineY, lineZ)
    xDistance = linePoint.getDistance(Point(v1.getDx(), v1.getDy(), v1.getDz()))
    print(xDistance)
    # crossP2 = np.cross(point.getNpArray(), leftLineVector.getNpArray())
    # numerator2 = Vector(crossP2[0], crossP2[1], crossP2[2]).getMagnitude()
    # xDistance = abs(numerator2) / leftLineVector.getMagnitude()

    # print(xDistance)
    print(topLineVector.getMagnitude())
    print(leftLineVector.getMagnitude())
    print(leftLineVector)
    xPercentage = xDistance / topLineVector.getMagnitude() * 100 
    yPercentage = yDistance / leftLineVector.getMagnitude() *  100

    if (math.isnan(xPercentage) or math.isnan(yPercentage)):
        Exception("The line and this rectangle do not intersect")

    return (xPercentage, yPercentage)


# v1 = Vector(1, 2, 3)
# v2 = Vector(4, 5, 6)
# v3 = Vector(7, 8, 9)
# v4 = Vector(10, 11, 12)
# v5 = Vector(-1, 3, -2)


# print(vec(v1, v2, v3, v4, v5))