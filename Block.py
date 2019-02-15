#
# Block object represents a mission block. An entity in IL2 that has a position and is represented by a string
#
 
from Position import Position  


class Block (Position): 
    def __init__(self, s):
        Position.__init__(self)
        self.s = s
        def find_value( s, s1, s2=";"):
            a = (s.find(s1)+len(s1))
            b = s.find(s2, (s.find(s1)+len(s1)))
            return float(s[a:b])
        self.x = find_value(self.s,"XPos = " )
        self.y = find_value(self.s,"YPos = " )
        self.z = find_value(self.s,"ZPos = " )
        self.rx = find_value(self.s,"XOri = " )
        self.ry = find_value(self.s,"YOri = " )
        self.rz = find_value(self.s,"ZOri = " )

    def __str__(self):
        def replace_value( s, s1, r, s2=";"):
            a = (s.find(s1)+len(s1))
            b = s.find(s2, a)
            s = s[0:a]+r+s[b:len(s)]
            return s 
        self.s = replace_value(self.s,"XPos = ", "{0:.3f}".format(self.x))
        self.s = replace_value(self.s,"YPos = ", "{0:.3f}".format(self.y))
        self.s = replace_value(self.s,"ZPos = ", "{0:.3f}".format(self.z))
        self.s = replace_value(self.s,"XOri = ", "{0:.3f}".format(self.rx))
        self.s = replace_value(self.s,"YOri = ", "{0:.3f}".format(self.ry))
        self.s = replace_value(self.s,"ZOri = ", "{0:.3f}".format(self.rz))
        return self.s

    def __repr__(self):
        return "Block located at: (%d, %d, %d)" % (self.x, self.y, self.z)
