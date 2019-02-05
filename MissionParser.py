# Reads the mission file
# Transforms elements

import random
import subprocess
import configparser

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __repr__(self):
      s = self.Blocktype +"\n{\n"
      for i, j in self.__dict__.items():
        if i != "Blocktype":
          s+="  " + i + " = " + j + ";\n"
      s+="}\n\n"
      return s

class Point: #     Point object represents and manipulates x,y,z coords.
      def __init__(self,x=0,y=0,z=0):
          self.x = x
          self.y = y
          self.z = z

      def __str__(self):
          return "({0}, {1}, {2})".format(self.x, self.y, self.z)
      
      def __eq__(self, other):
          return self.y == other.y and self.x == other.x and self.z == other.z

      def __neg__(self):
          return Point(-self.x, -self.y, -self.z)

      def __add__(self, p):
          return Point(self.x+p.x, self.y+p.y, self.z+p.z)
      
      def __sub__(self, p):
          return self + (-p)
      
      def __mul__(self, p):
          return Point(self.x*p.x, self.y*p.y, self.z*p.z)

      def __truediv__(self, p):
          return Point(self.x/p.x, self.y/p.y, self.z/p.z)

      def __abs__(self):
          return Point(abs(self.x), abs(self.y), abs(self.z))

      def norm(self):
          return Point(abs(self.x)/self.x, abs(self.y)/self.y, abs(self.z)/self.z)

      def __repr__(self):
          return "Point (%d, %d, %d)" % (self.x, self.y, self.z)


class Block: #     Block object represents a mission block
    def __init__(self, s):
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

    def __add__(self, p):
      return Vector(self.x + p.x, self.y + p.y, self.z + p.z, (self.rx + p.rx)%360, (self.ry + p.ry)%360, (self.rz + p.rz)%360 )

    def __sub__(self, p):
      return Vector(self.x - p.x, self.y - p.y, self.z - p.z, (self.rx - p.rx)%360, (self.ry - p.ry)%360, (self.rz - p.rz)%360 )

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

    def translate(self, v):
      self.x += v.x
      self.y += v.y
      self.z += v.z
      self.rx = (self.rx + v.rx)%360
      self.ry = (self.ry + v.ry)%360
      self.rz = (self.rz + v.rz)%360
      return self

class Vector: #     Vector used for transforming blocks
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):
      self.x = x
      self.y = y
      self.z = z
      self.rx = rx
      self.ry = ry
      self.rz = rz

    def __add__(self, p):
      return Vector(self.x + p.x, self.y + p.y, self.z + p.z, (self.rx + p.rx)%360, (self.ry + p.ry)%360, (self.rz + p.rz)%360 )

    def __sub__(self, p):
      return self + (-p)

    def __str__(self):
      return "({0}, {1}, {2}, {3}, {4}, {5})".format(self.x, self.y, self.z, self.rx, self.ry, self.rz)
 
    def __repr__(self):
      return "Vector: (%d, %d, %d, %d, %d, %d)" % (self.x, self.y, self.z, self.rx, self.ry, self.rz)

def find_block( s, name, st=0 ):
    start = s.find(name+"\n", st)
    s = s[start:len(s)]
    if '{' in s:
      match = s.split('{',1)[1]
      open = 1
      for index in range(len(match)):
        if match[index] in '{}':
            open = (open + 1) if match[index] == '{' else (open - 1)
        if not open:
            return name+"\n{"+match[:index]+"}\n\n"

# Function to return a block object (input string, block type name, index)
def get_block_old( s, b_type, index=0 ):
  start = s.find(b_type+"\n")
  s = s[start:len(s)]
  if '{\n' in s:
    match = s.split('{\n',1)[1]
    open = 1
    for i in range(len(match)):
      if match[i] in '{}':
          open = (open + 1) if match[i] == '{' else (open - 1)
      if not open:
          break
  lines = match[:i].split('\n')
  del(lines[-1])
  lines = [s.strip(" ;") for s in lines]
  D={"Blocktype" : b_type}
  for i,l in enumerate(lines):
    entry = l.split(" = ")
    D[entry[0]] = entry[1]
  return Struct(**D)

# Function to return a block object (input string, block type name, index)
def get_block( s, b_type, index=0 ):
  start = s.find(b_type+"\n")
  s = s[start:len(s)]
  if '{\n' in s:
    match = s.split('{\n',1)[1]
    open = 1
    for i in range(len(match)):
      if match[i] in '{}':
          open = (open + 1) if match[i] == '{' else (open - 1)
      if not open:
          break
  match = match[:i]
  sblock = ""
  if 'Carriages' in match:
    sblock_name = 'Carriages\n'
    start = match.find(sblock_name)
    sblock = match[start:len(s)]
    #sblock = sblock.split('{\n',1)[1]
    open = 0
    for i in range(len(sblock)):
      if sblock[i] in '{}':
        if open == 1:
          break
        open = (open + 1) if sblock[i] == '{' else (open - 1)
    sblock = sblock[0:i]+"}\n"
    match = match[:start-1] + sblock[i+2:] #exclude }\n
  else:
    match = match[:start-1]
  lines = match.split('\n')
  del(lines[-1])
  lines = [s.strip(" ;") for s in lines]
  D={"Blocktype" : b_type}
  for i,j in enumerate(lines):
    entry = j.split(" = ")
    D[entry[0]] = entry[1]
  D["Carriages"] = sblock
  return Struct(**D)


config = configparser.ConfigParser()
config.read('config_coop.ini')
data_path = config['DEFAULT']['data_path']
mission_path = config['DEFAULT']['mission_path']
resaver_path = config['DEFAULT']['resaver_path']
coop_path = config['DEFAULT']['coop_path']
mission_name = config['DEFAULT']['mission_name']
template_name = config['DEFAULT']['template_name']

with open(coop_path + template_name + ".Mission", 'r') as file :
  mission = file.read()

#plane = get_block(mission, "Plane")



plane = Block(find_block( mission, "Plane"))
train = Block(find_block( mission, "Train"))
vehicle = Block(find_block( mission, "Vehicle" ))



print (plane)
print ("")
print (train)
print ("")
print (vehicle)

T = Vector(2,4,6,45,90,300)
R = Vector(1,2,3,30,60,60)

print ("")
T = (plane - train)
print (T)
print (vehicle.translate(T))


