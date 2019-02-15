#
# Position object represents and manipulates x,y,z position and rx, ry, rz orientation coords.
# 

from math import sqrt, sin, cos, radians


class Position: 
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.x = x
        self.y = y
        self.z = z
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def __str__(self):
        return "({0}, {1}, {2}, {3}, {4}, {5})".format(self.x, self.y, self.z, self.rx, self.ry, self.rz)

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x and self.z == other.z and self.rx == other.rx and self.ry == other.ry and self.rz == other.rz

    def __neg__(self):
        return Position(-self.x, -self.y, -self.z, -self.rx, -self.ry, -self.rz)

    def __add__(self, p):
        return Position(self.x + p.x, self.y + p.y, self.z + p.z, (self.rx + p.rx)%360, (self.ry + p.ry)%360, (self.rz + p.rz)%360 )

    def __sub__(self, p):
        return Position(self.x - p.x, self.y - p.y, self.z - p.z, (self.rx - p.rx)%360, (self.ry - p.ry)%360, (self.rz - p.rz)%360 )

    def __mul__(self, p):
        return Position(self.x*p.x, self.y*p.y, self.z*p.z)

    def __truediv__(self, p):
        return Position(self.x/p.x, self.y/p.y, self.z/p.z)

    def __abs__(self):
        return Position(abs(self.x), abs(self.y), abs(self.z))

    def translate(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def rotate(self, p): # rotate self around Position p with angle from p.ry
        alpha = p.ry
        r_alpha = radians(p.ry)
        x_0 = self.x - p.x
        z_0 = self.z - p.z
        x_1 = x_0 * cos(r_alpha) - z_0 * sin(r_alpha)
        z_1 = x_0 * sin(r_alpha) + z_0 * cos(r_alpha)
        self.x = self.x - (x_0 - x_1)
        self.z = self.z + z_1 - z_0
        self.ry = (self.ry + alpha)%360
        return self

    def norm(self):
        return Position(abs(self.x)/self.x, abs(self.y)/self.y, abs(self.z)/self.z)

    def __repr__(self):
        return "Position: (%d, %d, %d, %d, %d, %d)" % (self.x, self.y, self.z, self.rx, self.ry, self.rz)
