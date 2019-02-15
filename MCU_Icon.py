#
# Icon class represents an Icon on the map
# 


class MCU_Icon:
    def __init__(self, index, targets, icon_id, coals, x, z, lcname, lcdesc, ltype=14, color=[100,0,0]):
        self.index = index
        self.targets = targets
        self.icon_id = icon_id
        self.coals = coals
        self.x = x
        self.z = z
        self.lcname = lcname
        self.lcdesc = lcdesc
        self.ltype = ltype
        self.color = color

    def __str__(self):
        return ("MCU_Icon\n"
        "{\n"
        "  Index = "+str(self.index)+";\n"
        "  Targets = ["+str(self.targets[0])+"];\n"
        "  Objects = [];\n"
        "  XPos = {0:.3f}".format(self.x)+";\n"
        "  YPos = 0.00;\n"
        "  ZPos = {0:.3f}".format(self.z)+";\n"
        "  XOri = 0.00;\n"
        "  YOri = 0.00;\n"
        "  ZOri = 0.00;\n"
        "  Enabled = 1;\n"
        "  LCName = "+str(self.lcname)+";\n"
        "  LCDesc = "+str(self.lcdesc)+";\n"
        "  IconId = "+str(self.icon_id)+";\n"
        "  RColor = "+str(self.color[0])+";\n"
        "  GColor = "+str(self.color[1])+";\n"
        "  BColor = "+str(self.color[2])+";\n"
        "  LineType = "+str(self.ltype)+";\n"
        "  Coalitions = "+str(self.coals)+";\n"
        "}\n\n")