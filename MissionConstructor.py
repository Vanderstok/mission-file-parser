# Basic mission Generator based on templates

import random
import subprocess
import configparser

def GenerateMission(mission_name):

  class Point(object):
      """ Point class represents and manipulates x,y,z coords. """
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

  class MCU_Icon(object):
    """Icon class represents an Icon on the map"""
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

  # Function to return a group in a mission file based on the group Name
  def find_group( s, name ):
      start = s.find("  Name = \""+name+"\"")
      s ="Group\n{\n"+s[start:len(s)]
      if '{' in s:
        match = s.split('{',1)[1]
        open = 1
        for index in range(len(match)):
          if match[index] in '{}':
              open = (open + 1) if match[index] == '{' else (open - 1)
          if not open:
              return "Group\n{"+match[:index]+"}\n\n"

  # Function to return a block based on block header name and starting at st
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

  #Function to find a substring between s1 and s2, starting at st (optional)
  def find_substr( s, s1, s2, st=0 ):
    x = (s.find(s1, st)+len(s1))
    y = s.find(s2, x)
    return s[x:y]

  #Function to find a substring between s1 and s2 and replace it with r, starting at st (optional) for one or all
  def replace_substr( s, s1, s2, r, st=0, single=True):
    while s.find(s1, st)>=0:
      a = (s.find(s1, st)+len(s1))
      b = s.find(s2, a)
      s = s[0:a]+r+s[b:len(s)]
      if single:
        break
      st = b
    return s 

  def random_set(x,y,n): #Get n random but unique numbers out range x:y
    values=list(range(x,y+1)) # max-1
    nums=[]
    for m in range(1,n+1):
      r1=random.randint(x-1,y-m)
      nums.append(values[r1])
      del values[r1]
    return nums

  def create_AI_flight(group_name, flight_name, patrol_name, plane_set): # read AI fighters and change the plane type and the patrol areas
    mission_flight = find_group(mission_template, group_name)
    nf = mission_flight.count(flight_name) # number of fighter flights
    helper_group = find_group(mission_template, "Helpers") # find helper group with all possible locations
    np = helper_group.count(patrol_name) # number of patrol areas
    fighters =""
    for i in range(nf):
      mission_fighters = find_group(mission_flight, flight_name+str(i+1))
      fighter=plane_set[random.randint(0, len(plane_set)-1)] # choose a plane type
      mission_fighters = mission_fighters.replace(find_substr(mission_fighters, "WorldObjects\Planes\\", ".txt"), fighter) # replace plane
      lst = random_set(1,np,2) # n=2 for two attack areas where fighters will cycle between
      for n in range(len(lst)):
        x = (find_substr( helper_group, "XPos = ", ";", helper_group.find(patrol_name+str(lst[n]) )))
        y = str(int(float((find_substr( helper_group, "YPos = ", ";", helper_group.find(patrol_name+str(lst[n]) ))))) + random.randint(-1000,500))
        z = (find_substr( helper_group, "ZPos = ", ";", helper_group.find(patrol_name+str(lst[n]) )))
        mission_fighters = replace_substr(mission_fighters, "XPos = ", ";", x, mission_fighters.find("Area_"+str(n+1)))
        mission_fighters = replace_substr(mission_fighters, "YPos = ", ";", y, mission_fighters.find("Area_"+str(n+1)))
        mission_fighters = replace_substr(mission_fighters, "ZPos = ", ";", z, mission_fighters.find("Area_"+str(n+1)))
      fighters += mission_fighters
    return fighters

  def create_simple_sites(group_name, object_name, site_name):
    mission_site = find_group(mission_template, group_name)
    nf = mission_site.count(object_name) # number of object groups
    helper_group = find_group(mission_template, "Helpers")
    np = helper_group.count(site_name) # number of possible locations
    object_site = ""
    lst = random_set(1,np,nf)
    for i, site in enumerate(lst):
      mission_object_site = find_group(mission_site, object_name+str(i+1))
      x = (find_substr( helper_group, "XPos = ", ";", helper_group.find(site_name+str(site))))
      y = (find_substr( helper_group, "YPos = ", ";", helper_group.find(site_name+str(site))))
      z = (find_substr( helper_group, "ZPos = ", ";", helper_group.find(site_name+str(site))))
      mission_object_site = replace_substr(mission_object_site, "XPos = ", ";", x, 0, False)
      mission_object_site = replace_substr(mission_object_site, "YPos = ", ";", y, 0, False)
      mission_object_site = replace_substr(mission_object_site, "ZPos = ", ";", z, 0, False)
      object_site += mission_object_site
    return object_site  

  config = configparser.ConfigParser()
  config.read('config.ini')
  data_path = config['DEFAULT']['data_path']
  mission_path = config['DEFAULT']['mission_path']
  resaver_path = config['DEFAULT']['resaver_path']
  coop_path = config['DEFAULT']['coop_path']
  #mission_name = config['DEFAULT']['mission_name']

  # Define Mission characteristics

  mission_description="This is a test mission to test the mission generator.<br><br>Your primary mission is to destroy the target marked on the map. Good luck!"
  mission_author="Vander"

  # Read Mission Template file
  with open(mission_path + "MissionTemplate_1.Mission", 'r') as file :
    mission_template = file.read()

  # Read description file. Desc files need UTF-16 encoding
  with open(mission_path + "MissionTemplate_1.eng", 'r', encoding='UTF-16') as file :
    labels = file.read()

  # Define Mission file blocks
  mission_header="# Mission File Version = 1.0;\n\n"
  mission_footer="\n# end of file"

  # all plane id's
  #fighters_allied_all=["i16t24", "la5s8", "p39l1", "p40e1", "p47d28", "lagg3s29", "yak1s127", "yak1s69", "la5fns2", "mig3s24", "spitfiremkvb", "yak7bs36", "spitfiremkixe"]
  #fighters_axis_all=["bf109e7","bf109f2","bf109f4","bf109g2","bf109g4","bf109g6","bf109g14","bf109k4","fw190a3","fw190a5","mc202s8","bf110e2","bf110g2","fw190a8"]
  #bombers_allied_all=["a20b", "il2m42", "il2m41", "il2m43", "pe2s35", "pe2s87"]
  #bombers_axis_sub=["ju87d3", "he111h6", "ju88a4", "hs129b2", "ju523mg4e"]

  # set bomber attributes: name, interdiction payload, bombing payload [payload_id, mod mask]
  payload_config={
    "a20b": ["A-20B", [1,1], [2,1] ],
    "il2m42": ["IL-2 AM-38", [44,1], [48,101001] ],
    "pe2s87": ["Pe-2 Series 87", [4,11], [5,101] ],
    "p40e1": ["P-40 E", [30, 11011], [10, 100011] ],
    "ju87d3": ["Ju 87 D-3", [5,11], [4,1] ],
    "he111h6": ["He 111 H-6", [0,111], [3,1] ],
    "ju88a4": ["Ju 88 A-4", [2,1], [1,11] ],
    "hs129b2": ["Hs 129 B-2", [16,10001], [4,1] ],
    "bf110e2": ["Bf 110 E-2" ,[3,1001], [4,10001] ]
  }

  # Tune for 1942 period
  fighters_allied=["la5s8", "p39l1", "p40e1", "lagg3s29", "lagg3s29", "yak1s69", "yak1s69", "mig3s24"]
  fighters_axis=["bf109e7","bf109f2","bf109f4","bf109g2","fw190a3","mc202s8","bf110e2"]
  bombers_allied=["a20b", "pe2s87", "pe2s87"]
  bombers_axis=["he111h6", "ju88a4"]
  attackers_allied=["a20b", "pe2s87", "pe2s87", "il2m42", "il2m42", "p40e1"]
  attackers_axis=["ju87d3", "ju88a4", "ju87d3", "ju87d3", "hs129b2", "bf110e2"]

  # Read mission_options template
  mission_options = find_block(mission_template, "Options")
  season = "summer"
  time_new = str(random.randint(8, 17)) + ":" + str(random.randint(0,59))
  month_new = str(random.randint(10,11))
  date_new = str(random.randint(1, 30)) + "." + month_new + ".1942" # specific for Stalingrad summer 42
  cloud_prefix = ["00_clear_0","01_Light_0","02_Medium_0","03_Heavy_0","04_Overcast_0"] # note clear no capital
  cloud_type = random.randint(0,4)
  cloud_desc = ["Clear","Few","Scattered","Broken","Overcast"][cloud_type]
  clouds_new = season+"\\" + cloud_prefix[cloud_type] + str(random.randint(0,9))
  if (cloud_type == 4) & (random.randint(0,9)>4):
    prectype = 1
    preclevel = random.randint(0,10)
  else:
    prectype = 0
    preclevel = 0
  if cloud_type in [3,4]:
    cloud_level = random.randint(900,1600)
  else:
    cloud_level = random.randint(1000,2500)
  cloud_height = random.randint(250,1000)
  temp = random.randint(15, 25)
  wind_speed = random.randint(1,10)
  wind_dir = random.randint(60,120)

  mission_options = replace_substr(mission_options, "SeasonPrefix = \"", "\";" , season[0:2])
  mission_options = replace_substr(mission_options, "Date = ", ";" , date_new)
  mission_options = replace_substr(mission_options, "Time = ", ";" , time_new + ":0")
  mission_options = replace_substr(mission_options, "CloudLevel = ", ";" , str(cloud_level))
  mission_options = replace_substr(mission_options, "CloudHeight = ", ";" , str(cloud_height))
  mission_options = replace_substr(mission_options, "CloudConfig = \"", "\\sky.ini" , clouds_new)
  mission_options = replace_substr(mission_options, "Temperature = ", ";" , str(temp))
  mission_options = mission_options.replace("0 :     0 :     0;","0 :     "+str(wind_dir)+" :     "+str(wind_speed)+";")
  mission_options = replace_substr(mission_options, "PrecType = ", ";" , str(prectype))
  mission_options = replace_substr(mission_options, "PrecLevel = ", ";" , str(preclevel))

  # split between high and low altitude attacks unless weather is overcast
  objective_types_low = {"airfield": 1,"artillery": 1, "armor": 1 } # defines objective types and payload type per objective
  objective_types_high = {"train": 2, "dump": 2, "bridge": 2}
  if cloud_type == 4:
    objective_type = random.choice(list(objective_types_low.keys()))
    payload_type = objective_types_low[objective_type]
  else:
    if random.randint(1,10)>5:
      objective_type = random.choice(list(objective_types_high.keys()))
      payload_type = objective_types_high[objective_type]
    else:
      objective_type = random.choice(list(objective_types_low.keys()))
      payload_type = objective_types_low[objective_type]

  # Select random objective within type
  objective_group = find_group(mission_template, "Objectives_" + objective_type)
  objective="objective_"+str(random.randint(1,objective_group.count("objective_")))
  mission_objective = find_group(objective_group, objective)

  # Generate objective description
  objective_desc = {
    "airfield": "Enemy bombers are bombing defences in Stalingrad on a daily basis.",
    "artillery": "Our spotters have located an enemy artillery battery that they will mark with red smoke.",
    "train": "An enemy train has been spotted that is unloading supplies and troops.",
    "dump": "A supply dump has been photographed some distance behind the front lines.",
    "bridge": "After yesterday's successful bridge attack, the enemy has built a replacement pontoon bridge.",
    "armor": "Our lines are threatened by enemy armor advancing slowly, but steadily."
  }[objective_type]

  #Determine plane set and choose random plane type
  if objective == "bridge":
    plane_new=bombers_allied[random.randint(0, len(bombers_allied)-1)] 
  else:
    plane_new=attackers_allied[random.randint(0, len(attackers_allied)-1)]
  escort_new=fighters_allied[random.randint(0, len(fighters_allied)-1)]

  mission_options = replace_substr(mission_options, "WorldObjects\\Planes\\", ".txt" , plane_new)

  # Read player flights
  mission_player = find_group(mission_template, "Player")
  mission_escort = find_group(mission_template, "Escort")

  wp_3=Point() # waypoint of the target
  wp_3.x=float(find_substr( mission_objective, "XPos = ", ";", mission_objective.find("primary_objective")))
  wp_3.z=float(find_substr( mission_objective, "ZPos = ", ";", mission_objective.find("primary_objective")))
  if objective_type in objective_types_low.keys():
    wp_3.y = float(cloud_level) - 100.000 - random.random()*150.000
    mission_player = mission_player.replace("AttackGTargets = 0", "AttackGTargets = 1")
  else:
    wp_3.y = 2500.000 + random.random()*1000
    mission_player = mission_player.replace("AttackGround = 0", "AttackGround = 1")

  wp_0=Point() # waypoint of player start
  wp_0.x=float(find_substr( mission_player, "XPos = ", ";", mission_player.find("wp_0")))
  wp_0.y=float(find_substr( mission_player, "YPos = ", ";", mission_player.find("wp_0")))
  wp_0.z=float(find_substr( mission_player, "ZPos = ", ";", mission_player.find("wp_0")))

  wp_1 = Point(wp_0.x-random.random()*2000*(wp_3-wp_0).norm().x, wp_0.y, wp_0.z+(5000*(wp_3-wp_0).norm().z))
  wp_2 = Point(wp_3.x-(4000*(wp_3-wp_0).norm().x), wp_3.y, wp_3.z-random.random()*3000*(wp_3-wp_0).norm().z )
  wp_4 = Point(wp_3.x+random.random()*2000*(wp_3-wp_0).norm().x, wp_3.y, wp_3.z-(5000*(wp_3-wp_0).norm().z))
  wp_5 = Point(wp_0.x+(3000*(wp_3-wp_0).norm().x), wp_0.y, wp_0.z+random.random()*1000*(wp_3-wp_0).norm().z)

  waypoints = [wp_0, wp_1, wp_2, wp_3, wp_4, wp_5]
  icon_pos = 0
  icons=[]
  mission_fp = find_group(mission_template, "Flight_Plan")
  for i,n in enumerate(waypoints):
    mission_player = replace_substr(mission_player, "XPos = ", ";", "{0:.3f}".format(n.x), mission_player.find("wp_"+str(waypoints.index(n))))
    mission_player = replace_substr(mission_player, "YPos = ", ";", "{0:.3f}".format(n.y), mission_player.find("wp_"+str(waypoints.index(n))))
    mission_player = replace_substr(mission_player, "ZPos = ", ";", "{0:.3f}".format(n.z), mission_player.find("wp_"+str(waypoints.index(n))))
    icon_pos = mission_fp.find("MCU_Icon", icon_pos) # create an icon corresponding with the wp and retrieve index etc
    icon_block = find_block( mission_fp, "MCU_Icon", icon_pos )
    index = find_substr( icon_block, "Index = ", ";" )
    lcname = find_substr( icon_block, "LCName = ", ";" )
    lcdesc = find_substr( icon_block, "LCDesc = ", ";" )
    coals = find_substr( icon_block, "Coalitions = ", ";" )
    if i == 0:
      labels = replace_substr( labels, "\n" + lcname+":", "\n", "Start") # write icon name
      labels = replace_substr( labels, "\n" + lcdesc+":", "\n", "Take-off and land here") # write icon name
      icon_id = 903
    elif i == 3:
      labels = replace_substr( labels, "\n" + lcname+":", "\n", "Attack") # write icon name
      labels = replace_substr( labels, "\n" + lcdesc+":", "\n", "Destroy the Primary Target") # write icon name
      icon_id = 902
    else:
      labels = replace_substr( labels, "\n" + lcname+":", "\n", "WP "+str(i)) # write icon name
      labels = replace_substr( labels, "\n" + lcdesc+":", "\n", "Waypoint") # write icon name
      icon_id = 901
    icons.append(MCU_Icon(index, [0], icon_id, coals, n.x, n.z, lcname, lcdesc ))
    icon_pos += 10

  # chain the icons and write to mission file
  mission_icons = ""
  for i,icon in enumerate(icons):
    if i == 5:
      icon.targets = [icons[0].index]
    else:
      icon.targets = [icons[i+1].index]
    mission_icons += str(icon)

  # Change Player & Escort Plane parameters
  mission_player = mission_player.replace(find_substr(mission_player, "WorldObjects\Planes\\", ".txt"), plane_new)
  mission_escort = mission_escort.replace(find_substr(mission_escort, "WorldObjects\Planes\\", ".txt"), escort_new)
  payload = str((payload_config[plane_new])[payload_type][0])
  mod = str((payload_config[plane_new])[payload_type][1])
  mission_player = mission_player.replace("PayloadId = 0", "PayloadId = " + payload)
  mission_player = mission_player.replace("WMMask = 1", "WMMask = " + mod)

  # Determine AI flights for Axis and Allies
  mission_fighters_axis = create_AI_flight("Fighters_Axis", "fighters_de_", "patrol_axis_", fighters_axis)
  mission_fighters_allied = create_AI_flight("Fighters_Allied", "fighters_ru_", "patrol_allied_", fighters_allied)

  # Change search area to objective location in all groups
  nf = mission_fighters_axis.count("fighters_de_")
  fighters =""
  for i in range(nf):
    mission_fighters = find_group(mission_fighters_axis, "fighters_de_"+str(i+1))
    for mcu in ["InterceptPlayer", "PlayerDetected"]:
      mission_fighters = replace_substr(mission_fighters, "XPos = ", ";", "{0:.3f}".format(wp_3.x), mission_fighters.find(mcu))
      mission_fighters = replace_substr(mission_fighters, "YPos = ", ";", "{0:.3f}".format(wp_3.y), mission_fighters.find(mcu))
      mission_fighters = replace_substr(mission_fighters, "ZPos = ", ";", "{0:.3f}".format(wp_3.z), mission_fighters.find(mcu))
    fighters += mission_fighters
  mission_fighters_axis = fighters

  # Create a simple German bomber flight
  mission_bombers_axis = find_group(mission_template, "Bombers_Axis")
  helper_group = find_group(mission_template, "Helpers") # find helper group with all possible locations
  np = helper_group.count("target_axis_") # number of patrol areas
  bomber=random.choice(bombers_axis) # choose a plane type
  mission_bombers_axis = mission_bombers_axis.replace(find_substr(mission_bombers_axis, "WorldObjects\Planes\\", ".txt"), bomber) # replace plane
  target = random.choice(list(range(1,np+1))) # could have been randint as well
  x = (find_substr( helper_group, "XPos = ", ";", helper_group.find("target_axis_" + str(target))))
  z = (find_substr( helper_group, "ZPos = ", ";", helper_group.find("target_axis_" + str(target))))
  if cloud_type == 4:
    y = "{0:.3f}".format(float(cloud_level) - 100.000)
  else:
    y = (find_substr( helper_group, "YPos = ", ";", helper_group.find("target_axis_" + str(target))))

  mission_bombers_axis = replace_substr(mission_bombers_axis, "XPos = ", ";", x, mission_bombers_axis.find("WP_bomb"))
  mission_bombers_axis = replace_substr(mission_bombers_axis, "YPos = ", ";", y, mission_bombers_axis.find("WP_bomb"))
  mission_bombers_axis = replace_substr(mission_bombers_axis, "ZPos = ", ";", z, mission_bombers_axis.find("WP_bomb"))
  payload_type = 2
  payload = str((payload_config[bomber])[payload_type][0])
  mission_bombers_axis = mission_bombers_axis.replace("PayloadId = 0", "PayloadId = " + payload)

  # Position AAA sites and smoke
  mission_AAA_axis = create_simple_sites("AAA_Axis", "flak_axis_", "AAA_axis_")
  mission_AAA_allied = create_simple_sites("AAA_Allied", "flak_allied_", "AAA_allied_")
  mission_smoke = create_simple_sites("Smoke", "smoke_", "smoke_pos_")

  # Read mission transports
  transport_groups = find_group(mission_template, "Transports")
  #transports = random_set(1,transport_groups.count("transport_"),10) # get 10 random but unique indexes
  transports = random.sample(range(transport_groups.count("transport_")),10)
  mission_transports = ""
  for i in transports:
    mission_transports += find_group( transport_groups, "transport_"+ str(i+1))

  # Read mission_logic
  mission_logic = find_group(mission_template, "Logic")

  # Read static groups template
  mission_static = find_group(mission_template, "Static")

  # Read Lines groups template
  mission_lines = find_group(mission_template, "Lines_"+month_new)

  # Build mission file
  mission = (mission_header +
    mission_options +
    mission_player +
    mission_escort +
    mission_fighters_axis +
    mission_fighters_allied +
    mission_bombers_axis +
    mission_AAA_axis +
    mission_AAA_allied +
    mission_objective +
    mission_transports +
    mission_logic +
    mission_smoke +
    mission_static +
    mission_lines +
    mission_icons +
    mission_footer)

  # Generate briefing
  if cloud_type != 0:
    cloud_text = (str(cloud_level) + " m")
  else:
    cloud_text = ""
  mission_description=("<b>Location: </b>East of Stalingrad<br><br>"
    "<b>Date: </b>" + date_new + "<br><b>Time: </b>" + time_new + "<br><br>"
    "<b>Weather: </b>" + str(temp) + " \u00b0C, Clouds: " + cloud_desc + " at " + cloud_text + "<br>"
    "Wind strength is " + str(wind_speed) + " m/s from " + str(wind_dir) + " degrees<br><br>"
    "<b>Situation: </b>" + objective_desc +"<br>"
    "<b>Your objective: </b>Destroy the enemy "+ objective_type + " as marked on the map<br>"
    "<b>Your orders: </b><ul><li>Blue Flight will attack the primary target.</li>"
    "<li>Red Flight will wait for Blue flight to take off, then escort Blue Flight to the target.</li><br></ul>Good luck!<br>")

  # Add mission description
  lcname = find_substr(mission_options, "LCName = ", ";")
  lcdesc = find_substr(mission_options, "LCDesc = ", ";")
  lcauthor = find_substr(mission_options, "LCAuthor = ", ";")

  labels = replace_substr( labels, lcname+":", "\n", mission_name)
  labels = replace_substr( labels, lcauthor+":", "\n", mission_author)
  labels = replace_substr( labels, lcdesc+":", "\n", mission_description)

  # print("The chosen player plane = "+plane_new)
  # print("The chosen objective = "+objective)

  # Write coop mission
  mission_path = coop_path

  # Write the mission file
  with open(mission_path + mission_name + '.mission', 'w') as file:
    file.write(mission)

  # Convert to msbin file
  subprocess.call([resaver_path+"MissionResaver.exe", "-d", data_path, "-f", mission_path + mission_name + ".mission" ])

  # Write the description file. Desc files need UTF-16 encoding. Note: resaver seems to destroy desc files (workaround).

  with open(mission_path + mission_name + '.eng', 'w', encoding='UTF-16') as file:
    file.write(labels)
  with open(mission_path + mission_name + '.fra', 'w', encoding='UTF-16') as file:
    file.write(labels)
  with open(mission_path + mission_name + '.ger', 'w', encoding='UTF-16') as file:
    file.write(labels)
  with open(mission_path + mission_name + '.pol', 'w', encoding='UTF-16') as file:
    file.write(labels)
  with open(mission_path + mission_name + '.rus', 'w', encoding='UTF-16') as file:
    file.write(labels)
  with open(mission_path + mission_name + '.spa', 'w', encoding='UTF-16') as file:
    file.write(labels)
