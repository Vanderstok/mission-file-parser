# Basic mission Generator based on templates

import random
import subprocess
import configparser
import json
import os
from math import sqrt, sin, cos, radians
from Position import Position
from Block import Block
from MCU_Icon import MCU_Icon

def GenerateMission(mission_name, template_path, template_name, date, msbin=True):

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

  # Function to return a block in group s, based on block name and starting at st
  def find_block( s, block_name, st=0 ):
      start = s.find(block_name+"\n", st)
      s = s[start:len(s)]
      if '{' in s:
        match = s.split('{',1)[1]
        open = 1
        for index in range(len(match)):
          if match[index] in '{}':
              open = (open + 1) if match[index] == '{' else (open - 1)
          if not open:
              return block_name+"\n{"+match[:index]+"}\n\n"

  # Function to delete a block based on index in group s
  def delete_block( s, index ):
      x = s.find("Index = "+index+";") # find pos of Index
      s1 = s.rfind("{", 0, x) # find pos of first line before {
      for k in range(2): # number of extra lines to cut
        s1 = s.rfind("\n", 0, s1-1)  # find pos at end of }
      #print ("s1 = ", s1)
      open = 1
      for i in range(x,len(s)):
        if s[i] in '{}':
            open = (open + 1) if s[i] == '{' else (open - 1)
        if not open:
          s2 = i
          break
      for k in range(2):
        s2 = s.find("\n", s2+1)
      #print("s2 = ", s2)
      return s[0:s1] + s[s2:len(s)]


  # Function to return Position based on object name in group s and starting at st
  def get_coords( s, name, st=0 ):
      P =Position()
      P.x = float(find_substr( s, "XPos = ", ";", s.find(name)))
      P.y = float(find_substr( s, "YPos = ", ";", s.find(name)))
      P.z = float(find_substr( s, "ZPos = ", ";", s.find(name)))
      P.rx = float(find_substr( s, "XOri = ", ";", s.find(name)))
      P.ry = float(find_substr( s, "YOri = ", ";", s.find(name)))
      P.rz = float(find_substr( s, "ZOri = ", ";", s.find(name)))
      return P

  # Function to set coords of a MCU based on Position object
  def set_coords( s, P, name):
      s = replace_substr(s, "XPos = ", ";", "{0:.3f}".format(P.x), s.find(name))
      s = replace_substr(s, "YPos = ", ";", "{0:.3f}".format(P.y), s.find(name))
      s = replace_substr(s, "ZPos = ", ";", "{0:.3f}".format(P.z), s.find(name))
      s = replace_substr(s, "XOri = ", ";", "{0:.3f}".format(P.rx), s.find(name))
      s = replace_substr(s, "YOri = ", ";", "{0:.3f}".format(P.ry), s.find(name))
      s = replace_substr(s, "ZOri = ", ";", "{0:.3f}".format(P.rz), s.find(name))
      return s

  # Function that finds all blocks in a group and puts them in a list of blocks
  def group2block(s):
    block = []
    if s.count("{")>1:
      start = s.find("{") + 1 # find location of first { in group
      for k in range(s.count("Index = ", s.find("Index = ")+1)):
        a = s.find("{", start) # find location of first { in block
        b = s.rfind("\n", 1, a-1) # find start of line with {
        c = s.rfind("\n", 1, b) # find start of line of block
        x = 1
        for i, ch in enumerate (s[a+1:len(s)]): # iterate through string from a+1
          if ch=="{":
            x += 1
          elif ch=="}":
            x += -1
          if x==0:
            break
        block.append(s[c+1:a+i+3]+"\n")
        s = s[a+i+3:len(s)]
      return block

  # Function to position group( group(string), dest Position (contains destination location and heading based on center of group)
  def position_group(group, D ):
    name = find_substr( group, "Name = ", ";" )
    index = find_substr( group, "Index = ", ";" )
    desc = find_substr( group, "Desc = ", ";" )
    block_list = group2block(group) 
    block_group=[]
    for s in block_list:
      block_group.append(Block(s))
    # Determine rotation Position based on center point of group 
    x_min = min([(i.x) for i in block_group])
    y_min = min([(i.y) for i in block_group])
    z_min = min([(i.z) for i in block_group])
    x_max = max([(i.x) for i in block_group])
    y_max = max([(i.y) for i in block_group])
    z_max = max([(i.z) for i in block_group])
    x_c = x_min + (x_max - x_min)/2
    y_c = y_min + (y_max - y_min)/2
    z_c = z_min + (z_max - z_min)/2
    R = Position(x_c, y_c, z_c, 0,0,0)
    R.ry = D.ry

    #iterate through all block objects and move them
    moved_group = ""
    for b in block_group:
      b.rotate(R)
      b.translate(D - R)
      moved_group += str(b)
    moved_group = "Group\n{\n  Name = "+name+";\n  Index = "+index+";\n  Desc = "+desc+";\n" + moved_group + "}\n\n"
    return moved_group

  # Function to move group( group, move_Position ) group = string, Position contains translation and direction change
  def move_group(group, V, T=Position(0,0,0,0,0,0) ):
    name = find_substr( group, "Name = ", ";" )
    index = find_substr( group, "Index = ", ";" )
    desc = find_substr( group, "Desc = ", ";" )
    block_list = group2block(group) 
    block_group=[]
    for s in block_list:
      block_group.append(Block(s))
    #iterate through all block objects and move them
    moved_group = ""
    for b in block_group:
      b.translate(V)
      if T != Position(0,0,0,0,0,0):
        b.rotate(T)
      moved_group += str(b)
    moved_group = "Group\n{\n  Name = "+name+";\n  Index = "+index+";\n  Desc = "+desc+";\n" + moved_group + "}\n\n"
    return moved_group
    
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

  # read AI fighters and change the plane type and the patrol areas group_name: ie "Patrols", flight_name: ie " fighters_"+side, patrol_name is helper prefix, plane_set is "fighters_all"
  def create_AI_flight(template, flight_name, patrol_name, plane_set, amount=0):
    mission_flight = find_group(template, "Patrols")
    if amount == 0:
      nf = mission_flight.count(flight_name) # number of fighter flights
    else:
      nf = amount
    helper_group = find_group(template, "Helpers") # find helper group with all possible locations
    np = helper_group.count(patrol_name) # number of patrol areas
    fighters =""
    for i in range(nf):
      mission_fighters = find_group(mission_flight, flight_name+str(i+1))
      fighter=plane_set[random.randint(0, len(plane_set)-1)] # choose a plane type
      mission_fighters = mission_fighters.replace(find_substr(mission_fighters, "WorldObjects\Planes\\", ".txt"), fighter) # replace plane
      lst = random.sample(range(1,np+1),2) # n=2 for two waypoints where fighters will cycle between
      for n in range(len(lst)):
        x = (find_substr( helper_group, "XPos = ", ";", helper_group.find(patrol_name+str(lst[n]) )))
        y = str(int(float((find_substr( helper_group, "YPos = ", ";", helper_group.find(patrol_name+str(lst[n]) ))))) + random.randint(-1000,500))
        z = (find_substr( helper_group, "ZPos = ", ";", helper_group.find(patrol_name+str(lst[n]) )))
        mission_fighters = replace_substr(mission_fighters, "XPos = ", ";", x, mission_fighters.find("Area_"+str(n+1)))
        mission_fighters = replace_substr(mission_fighters, "YPos = ", ";", y, mission_fighters.find("Area_"+str(n+1)))
        mission_fighters = replace_substr(mission_fighters, "ZPos = ", ";", z, mission_fighters.find("Area_"+str(n+1)))
      fighters += mission_fighters
    return fighters

  def create_simple_sites(template, group_name, object_name, site_name):
    mission_site = find_group(template, group_name)
    nf = mission_site.count(object_name) # number of object groups
    helper_group = find_group(template, "Helpers")
    np = helper_group.count(site_name) # number of possible locations
    object_site = ""
    lst = random.sample(range(1,np+1),nf)
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

  #
  # Init
  #

  config = configparser.ConfigParser()
  config.read('config.ini')
  il2_path = config['DEFAULT']['il2_path']
  coop_path = il2_path + "\\data\\Multiplayer\\Cooperative\\"
  data_path = il2_path + "\\data\\"
  mission_path = il2_path + "\\data\Missions\\"
  resaver_path = il2_path + "\\bin\\resaver\\"

  mission_description="This is a test mission to test the mission generator.<br><br>Your primary mission is to destroy the target marked on the map. Good luck!"
  mission_author="Vander"
  mission_header="# Mission File Version = 1.0;\n\n"
  mission_footer="\n# end of file"

  objective_types_low = {"airfield": 1,"artillery": 1, "armor": 1, "garrison": 2 } # defines objective types and payload type per objective
  objective_types_high = {"train": 2, "ammo dump": 2, "bridge": 2, "fuel dump": 2}
  objective_types_all = dict(objective_types_low, **objective_types_high)
  objective_desc_all = {
    "airfield": "Enemy bombers have been spotted while lined up on one of the airfields.",
    "artillery": "Our spotters have located an active enemy artillery battery.",
    "train": "An enemy train has been spotted that is unloading supplies and troops.",
    "ammo dump": "An ammo dump has been photographed some distance behind the front lines.",
    "bridge": "After yesterday's successful bridge attack, the enemy has built a replacement pontoon bridge.",
    "armor": "The enemy has moved up armored units to forward positions.",
    "fuel dump" : "An active fuel storage has been found some distance behind the enemy lines.",
    "patrol" : "Enemy air activity has increased recently.",
    "garrison" : "An enemy garrison has been located close to the front lines."
  }

  fighters_allied=["la5s8", "p39l1", "p40e1", "lagg3s29", "lagg3s29", "yak1s69", "yak1s69", "mig3s24"]
  fighters_axis=["bf109e7","bf109f2","bf109f4","bf109g2","fw190a3","mc202s8","bf110e2"]
  fighters_all={
    "allied": fighters_allied,
    "axis": fighters_axis
  }
  bombers_allied=["a20b", "pe2s87", "pe2s87"]
  bombers_axis=["he111h6", "ju88a4"]
  bombers_all={
    "allied": bombers_allied,
    "axis": bombers_axis
  }
  attackers_allied=["a20b", "pe2s87", "pe2s87", "il2m42", "il2m42", "p40e1"]
  attackers_axis=["ju87d3", "ju88a4", "ju87d3", "ju87d3", "hs129b2", "bf110e2"]
  attackers_all={
    "allied": attackers_allied,
    "axis": attackers_axis
  }

  # plane cfg [0:name, 1:attack cfg[payload, mod], 2:bomber cfg[payload, mod], 3:weight (not implemented)]
  plane_config_allied={
    "a20b": ["A-20B", [1,1], [2,1], 2 ],
    "il2m42": ["IL-2 AM-38", [44,1], [48,101001], 4 ],
    "il2m43": ["IL-2 AM-38", [41,1], [25,1], 4 ],
    "pe2s87": ["Pe-2 Series 87", [4,11], [5,101], 4 ],
    "p40e1": ["P-40 E", [30, 11011], [10, 100011], 2 ],
    "p39l1": ["P-39L-1", [0, 1], [0, 1], 2 ],
    "la5s8": ["La-5 Series 8", [0, 1], [0, 1], 2 ],
    "lagg3s29": ["LaGG-3 Series 29", [0, 1], [0, 1], 2 ],
    "yak1s69": ["Yak-1 Series 69", [0, 1], [0, 1], 2 ],
    "mig3s24": ["MiG-3 Series 24", [0, 1], [0, 1], 2 ]
  }
  plane_config_axis={
    "ju87d3": ["Ju 87 D-3", [5,11], [4,1], 3 ],
    "he111h6": ["He 111 H-6", [0,111], [3,1], 3 ],
    "ju88a4": ["Ju 88 A-4", [2,1], [1,11], 2 ],
    "hs129b2": ["Hs 129 B-2", [16,10001], [4,1], 1 ],
    "bf110e2": ["Bf 110 E-2" ,[3,1001], [4,10001], 2 ],
    "bf109e7": ["Bf 109 E-7" ,[0,1], [0,1], 2 ],
    "bf109f2": ["Bf 109 F-2" ,[0,1], [0,1], 1 ],
    "bf109f4": ["Bf 109 F-4" ,[0,1], [0,1], 2 ],
    "bf109g2": ["Bf 109 G-2" ,[0,1], [0,1], 2 ],
    "fw190a3": ["Fw 190 A-3" ,[0,1], [0,1], 2 ],
    "mc202s8": ["MC.202 Series VIII" ,[0,1], [0,1], 1 ]
  }
  plane_config_all={
    "allied": plane_config_allied,
    "axis": plane_config_axis
  }

  mission_objective_desc = {}
  mission_objective = {}
  mission_blue_flight = {}
  mission_red_flight = {}
  mission_patrols = {}
  mission_icons = ""
  mission_AAA = {}

  # Read files 

  with open(template_path + template_name + ".mission", 'r') as file :
    mission_template = file.read()
  with open(template_path + template_name + ".eng", 'r', encoding='UTF-16') as file :
    labels = file.read()


  #
  # Choose Day/Time and Weather
  #
  season = "summer" # only for building textures
  date_new = date
  month = date_new[3:5]
  mission_options = find_block(mission_template, "Options")
  if month in ["10","11"]:
    mission_options = mission_options.replace("LANDSCAPE_Stalin_s", "LANDSCAPE_Stalin_a")
    mission_options = mission_options.replace("stalingrad-summer-1942", "stalingrad-autumn-1942")
  if month in ["12"]:
    mission_options = mission_options.replace("LANDSCAPE_Stalin_s", "LANDSCAPE_Stalin_w")
    mission_options = mission_options.replace("stalingrad-summer-1942", "stalingrad-1942")
    season = "winter"
  mission_options = replace_substr(mission_options, "SeasonPrefix = \"", "\";" , season[0:2])
  mission_options = replace_substr(mission_options, "Date = ", ";" , date_new)

  cloud_prefix = ["00_clear_0","01_Light_0","02_Medium_0","03_Heavy_0","04_Overcast_0"] # note clear; no capital
  if (config['MISSION']['weather'] == "0"):
    hours = "{:02d}".format(random.randint(8, 16))
    minutes = "{:02d}".format(random.randint(0,59))
    time_new = hours + ":" + minutes
    cloud_type = random.choice([0,1,1,1,2,2,2,3,3,4])
    wind_speed = random.randint(0,8)
  else:
    mission_time_c = config['MISSION']['mission_time']
    time_new = {"dawn": "07:15", "morning": "09:00", "noon": "12:00", "afternoon": "15:30", "dusk": "18:00", "night": "00:30"}[mission_time_c]
    mission_wind_c = config['MISSION']['mission_wind']
    wind_speed = {"light": 2, "moderate": 6, "strong": 10}[mission_wind_c]
    mission_cloud_c = config['MISSION']['mission_cloud']
    cloud_type = {"no clouds": 0, "few clouds": 1, "medium clouds": 2, "heavy clouds": 3}[mission_cloud_c]
  cloud_desc = ["Clear","Few","Scattered","Broken","Overcast"][cloud_type]
  clouds_new = season+"\\" + cloud_prefix[cloud_type] + str(random.randint(0,9))
  if (cloud_type == 4) & (random.randint(0,9)>4):
    prectype = 1
    preclevel = random.randint(1,10)
  else:
    prectype = 0
    preclevel = 0
  if cloud_type in [3,4]:
    cloud_level = random.randint(900,1600)
    cloud_height = random.randint(200,600)
  else:
    cloud_level = random.randint(900,2500)
    cloud_height = random.randint(250,1000)
  temp = random.randint(5, 15)
  wind_dir = random.randint(90,179)

  mission_options = replace_substr(mission_options, "Time = ", ";" , time_new + ":0")
  mission_options = replace_substr(mission_options, "CloudLevel = ", ";" , str(cloud_level))
  mission_options = replace_substr(mission_options, "CloudHeight = ", ";" , str(cloud_height))
  mission_options = replace_substr(mission_options, "CloudConfig = \"", "\\sky.ini" , clouds_new)
  mission_options = replace_substr(mission_options, "Temperature = ", ";" , str(temp))
  mission_options = mission_options.replace("0 :     0 :     0;","0 :     "+str(wind_dir)+" :     "+str(wind_speed)+";")
  mission_options = replace_substr(mission_options, "PrecType = ", ";" , str(prectype))
  mission_options = replace_substr(mission_options, "PrecLevel = ", ";" , str(preclevel))

  #
  # Choose Map/Lines & Situation
  # 

  if month in ["09", "10", "11"]:
    phase = month
  elif month == "08":
    phase = "09"
  else:
    phase = "11"

  mission_lines = find_group(mission_template, "Lines_"+ phase)

  #
  # Choose Operations area
  #

  #
  # Populate random objects in operations area
  #

  mission_smoke = create_simple_sites(mission_template, "Smoke", "smoke_", "smoke_pos_")
  transport_groups = find_group(mission_template, "Transports")
  transports = random.sample(range(transport_groups.count("transport_")),10)
  mission_transports = ""
  for i in transports:
    mission_transports += find_group( transport_groups, "transport_"+ str(i+1))

  #
  # Read Static groups
  #

  mission_static = find_group(mission_template, "Static")
  mission_logic = find_group(mission_template, "Logic")
  mission_AAA_all = find_group(mission_template, "AAA")
  helper_group = find_group(mission_template, "Helpers")
  mission_AAA = ""

  # Set AAA AI level
  aaa_gunners = config['MISSION']['aaa_gunners']
  AI_level = "AILevel = " + {"harmless" : "1", "competent" : "2", "dangerous" : "3" }[aaa_gunners]
  mission_AAA_all = mission_AAA_all.replace("AILevel = 1", AI_level)
  mission_AAA_all = mission_AAA_all.replace("AILevel = 2", AI_level)
  #mission_AAA_all = replace_substr( mission_AAA_all, "AILevel = ", ";", AI_level, 0, False)
    
  #
  # For each side: 
  #
  # side_c: 0 -both sides, 1=allied only, 2=axis only
  # scenario[side] = 0 = random, 1: patrol front, 2 = escort bombers, 3 = ground attack, 
  scenario = {}
  random_config = {}
  side_c = int(config['MISSION']['side']) # Side that players want to play

  # Determine scenario or generate if chosen random
  for side in ["allied", "axis"]:
    scenario[side] = int(config['MISSION']['scenario_' + side])
    if scenario[side] == 0:
      random_config[side] = True
      scenarios = []
      k=0
      for i in range(mission_template.count("Blue_flight_" + side)):
        f = mission_template.find("Blue_flight_" + side, k)
        start = f + len("Blue_flight_" + side) + 1
        nr = int(mission_template[start:start+1])# get 1 character
        scenarios.append( nr )
        k = f + 1
      scenario[side] = random.choice(scenarios)
    else:
      random_config[side] = False

  # Main loop per side
  for side in ["allied", "axis"]:
    if side == "allied":
      other_side = "axis"
    else:
      other_side = "allied"

    # Determine objective type
    if scenario[side] != 0:
      objective_type = config['MISSION']['mission_target_' + side]
      payload_type = objective_types_all[objective_type]
    else:
      if cloud_type == 4: # if overcast limit possibilities
        objective_type = random.choice(list(objective_types_low.keys())) 
        payload_type = objective_types_low[objective_type]
      else:
        if random.randint(1,10)>4:
          objective_type = random.choice(list(objective_types_high.keys()))
          payload_type = objective_types_high[objective_type]
        else:
          objective_type = random.choice(list(objective_types_low.keys()))
          payload_type = objective_types_low[objective_type]
    
    if scenario[side] == 1:
      objective_desc = objective_desc_all["patrol"]
      mission_objective_desc[side] = ("<b>Situation: </b>" + objective_desc +"<br>"
      "<b>Your objective: </b>Patrol the lines between the two waypoints indicated on the map.<br>")
    else:
      objective_desc = objective_desc_all[objective_type]
      mission_objective_desc[side] = ("<b>Situation: </b>" + objective_desc +"<br>"
      "<b>Your objective: </b>Destroy the enemy "+ objective_type + " as marked on the map<br>")

    LCText = find_substr( mission_logic, "LCText = ", ";", mission_logic.find("Briefing_"+side) )
    labels = replace_substr( labels, "\n" + LCText +":", "\n", mission_objective_desc[side])

    # Select random objective group (layout) of chosen type
    objectives_group = find_group(mission_template, "Objectives_" + objective_type)
    helpers_group = find_group(mission_template, "Helpers")
    objective_index = random.randint(1,objectives_group.count("objective_" + objective_type + "_" +side))
    objective="objective_" + objective_type + "_" + side + "_" + str(objective_index)
    objective_group = find_group(objectives_group, "objective_" + objective_type + "_" + side + "_" + str(objective_index))
    
    # Select random location of the objective group
    helper_index = random.randint(1,helpers_group.count("objective_" + objective_type + "_" +side))
    helpers_objective = find_group(helpers_group, "objective_" + objective_type + "_" + side + "_" + str(helper_index))
    T = get_coords( helpers_objective, "primary_target")
    C = get_coords( objective_group, "primary_objective" )
    mission_objective[side] = move_group(objective_group, T-C, T)

    # insert code here to move AAA to objective location (see below/airfield)
    for i in range(helpers_objective.count("AAA_")):
      T = get_coords( helpers_objective, "AAA_" + str(i+1))
      mission_object_site = find_group(mission_AAA_all, "objective_" + side +"_"+str(i+1))
      new_group = position_group(mission_object_site, T)
      mission_AAA += new_group
    
    print(objective_type, objective)

    # Determine AI Patrols
    if scenario[side] == 1:
      fighters_flight = create_AI_flight(mission_template, "fighters_" + side + "_", "patrol_" + side + "_", fighters_all[side], 1)
      bombers_flight = create_AI_flight(mission_template, "bombers_" + side + "_", "patrol_" + side + "_", attackers_all[side], 1)
      mission_patrols[side] = fighters_flight + bombers_flight
    else:
      mission_patrols[side] = create_AI_flight(mission_template, "fighters_" + side + "_", "patrol_" + side + "_", fighters_all[side])

    # assign or randomly choose intercept chance
    if random_config[side]:
      intercept_chance = random.choice(["25", "50", "100"]) # Set intercept randomness
    else:
      intercept_chance = {"low": "0", "medium": "50", "high": "100"}[config['MISSION']['intercept_chance_' + other_side]]
    # Apply AI values
    x=0
    for i in range(mission_patrols[side].count("intercept_random")):
      st = mission_patrols[side].find("intercept_random", x)
      mission_patrols[side] = replace_substr(mission_patrols[side], "Random = ", ";", intercept_chance, st)
      x = st + 1

    print("scenario " + side + " :", scenario[side])

    # choose blue_flight group based on chosen scenario
    mission_blue_flight[side] = find_group(mission_template, "Blue_flight_" + side + "_" + str(scenario[side]) )
    mission_red_flight[side] = find_group(mission_template, "Red_flight_" + side)

    # Choose plane type and assign appropriate loadout
    if not random_config[side]:
      bombers_c = config['PLANES']['bombers_'+ side]
      bombers_c = dict(json.loads(bombers_c.replace("'", "\"")))
      fighters_c = config['PLANES']['fighters_'+ side]
      fighters_c = dict(json.loads(fighters_c.replace("'", "\"")))
      if scenario[side] == 1:
        plane_blue_c = config['MISSION']['fighter2_type_' + side]
        plane_blue = fighters_c[plane_blue_c]
      else:
        plane_blue_c = config['MISSION']['bomber_type_' + side]
        plane_blue = bombers_c[plane_blue_c]
      plane_red_c = config['MISSION']['fighter_type_' + side]
      plane_red = fighters_c[plane_red_c]
      fighter_skill_c = config['MISSION']['fighter_skill_' + side]
      skill_red ={"rookie": "1" , "regular": "2", "veteran": "3"}[fighter_skill_c]
      mission_red_flight[side] = replace_substr( mission_red_flight[side], "AILevel = ", ";", skill_red, 0, False)
    elif scenario[side] == 1:
      plane_blue=fighters_all[side][random.randint(0, len(fighters_all[side])-1)]
      plane_red=fighters_all[side][random.randint(0, len(fighters_all[side])-1)] 
    elif scenario[side] == 2:  
      if objective in objective_types_high:
        plane_blue=bombers_all[side][random.randint(0, len(bombers_all[side])-1)]
      else:
        plane_blue=attackers_all[side][random.randint(0, len(attackers_all[side])-1)]
      plane_red=fighters_all[side][random.randint(0, len(fighters_all[side])-1)]

    print(plane_blue, plane_red)

    mission_blue_flight[side] = mission_blue_flight[side].replace(find_substr(mission_blue_flight[side], "WorldObjects\Planes\\", ".txt"), plane_blue)
    mission_red_flight[side] = mission_red_flight[side].replace(find_substr(mission_red_flight[side], "WorldObjects\Planes\\", ".txt"), plane_red)
    payload_blue = str((plane_config_all[side][plane_blue])[payload_type][0])
    mod = str((plane_config_all[side][plane_blue])[payload_type][1])
    mission_blue_flight[side] = mission_blue_flight[side].replace("PayloadId = 0", "PayloadId = " + payload_blue)
    mission_blue_flight[side] = mission_blue_flight[side].replace("WMMask = 1", "WMMask = " + mod)
    
    # Single sided or double sided? 
    
    if (side == "allied" and side_c == 2) or (side == "axis" and side_c == 1):
      mission_blue_flight[side] = mission_blue_flight[side].replace("CoopStart = 1", "CoopStart = 0")
      mission_red_flight[side] = mission_red_flight[side].replace("CoopStart = 1", "CoopStart = 0")

    # Delete planes based on desired number
    bomber_count = {}
    fighter_count = {}
    if not random_config[side]:
      if scenario[side] == 1:
        bomber_count[side] = int(config['MISSION']['fighter2_count_' + side])
        fighter_count[side] = int(config['MISSION']['fighter_count_' + side])
      else:
        bomber_count[side] = int(config['MISSION']['bomber_count_' + side])
        fighter_count[side] = int(config['MISSION']['fighter_count_' + side])
    else:
        bomber_count[side] = 4
        fighter_count[side] = 4
    for i in range(bomber_count[side]+1,mission_blue_flight[side].count("Blue ")+1):
      st = mission_blue_flight[side].find("Blue "+ str(i))
      Index_plane = find_substr( mission_blue_flight[side], "Index = ", ";", st)
      mission_blue_flight[side] = delete_block( mission_blue_flight[side], Index_plane)
      st = mission_blue_flight[side].find("MisObjID = " + Index_plane + ";")
      st = mission_blue_flight[side].rfind("Index = ",0,st)
      Index_entity = find_substr( mission_blue_flight[side], "Index = ", ";", st)
      mission_blue_flight[side] = delete_block( mission_blue_flight[side], Index_entity)

    for i in range(fighter_count[side]+1,mission_red_flight[side].count("Red ")+1):
      st = mission_red_flight[side].find("Red "+ str(i))
      Index_plane = find_substr( mission_red_flight[side], "Index = ", ";", st)
      mission_red_flight[side] = delete_block( mission_red_flight[side], Index_plane)
      st = mission_red_flight[side].find("MisObjID = " + Index_plane + ";")
      st = mission_red_flight[side].rfind("Index = ",0,st)
      Index_entity = find_substr( mission_red_flight[side], "Index = ", ";", st)
      mission_red_flight[side] = delete_block( mission_red_flight[side], Index_entity)

    # Move airfield
    if not random_config[side]:
      if side == "allied":
        airfield_suffix = {"far from": "11", "close to": "09"}[config['MISSION']['start_location_' + side]]
      if side == "axis":
        airfield_suffix = {"far from": "09", "close to": "11"}[config['MISSION']['start_location_' + side]]
    else:
      airfield_suffix = phase
    print (month, phase, "helpers_airfield_" + side + "_" + airfield_suffix)
    helpers_airfield = find_group(mission_template, "helpers_airfield_" + side + "_" + airfield_suffix)
    T = get_coords( helpers_airfield, "wp_0")
    C_blue = get_coords( mission_blue_flight[side], "wp_0" )
    C_red = get_coords( mission_red_flight[side], "wp_0" )
    mission_blue_flight[side] = move_group(mission_blue_flight[side], T-C_blue)
    mission_red_flight[side] = move_group(mission_red_flight[side], T-C_red)

    d_blue = 25 # distance between parked planes in m
    d_red = 16
    T = get_coords( helpers_airfield, "blue_flight")
    for i in range(mission_blue_flight[side].count("WorldObjects\Planes\\")):
      P = T + Position(-d_blue*i*sin(radians(T.ry)),0 , d_blue*i*cos(radians(T.ry)),0 ,0 ,0 )
      mission_blue_flight[side] = set_coords(mission_blue_flight[side], P, "Blue "+str(i+1))
    mission_red_flight[side] = set_coords(mission_red_flight[side], P, "check_bomber_present")

    T = get_coords( helpers_airfield, "red_flight")
    for i in range(mission_red_flight[side].count("WorldObjects\Planes\\")):
      P = T + Position(-d_red*i*sin(radians(T.ry)),0 , d_red *i*cos(radians(T.ry)),0 ,0 ,0 )
      mission_red_flight[side] = set_coords(mission_red_flight[side], P, "Red "+str(i+1))

    for i in range(helpers_airfield.count("AAA_")):
      T = get_coords( helpers_airfield, "AAA_" + str(i+1))
      mission_object_site = find_group(mission_AAA_all, "airfield_" + side +"_"+str(i+1))
      new_group = position_group(mission_object_site, T)
      mission_AAA += new_group

    # Determine Waypoints for Blue flight for each scenario; Red flight will always cover Blue flight

    if scenario[side] == 1:
      patrol_name = "patrol_" + side + "_"
      np = helper_group.count(patrol_name) # number of patrol areas
      lst = random.sample(range(1,np+1),2) # n=2 for two waypoints where fighters will cycle between
      wp = [Position(), Position()]
      for n in [0,1]:
        wp[n].x = float(find_substr( helper_group, "XPos = ", ";", helper_group.find(patrol_name+str(lst[n]) )))
        wp[n].y = float((find_substr( helper_group, "YPos = ", ";", helper_group.find(patrol_name+str(lst[n]) )))) + random.randint(-500,1000)
        wp[n].z = float(find_substr( helper_group, "ZPos = ", ";", helper_group.find(patrol_name+str(lst[n]) )))
      wp_3 = wp[0]
      wp_4 = wp[1]
      wp_0 = get_coords( mission_blue_flight[side], "wp_0" )
      wp_2 = Position(wp_3.x-random.randint(5000,9000)*(wp_3-wp_0).norm().x, wp_3.y, wp_3.z-random.randint(5000,9000)*(wp_3-wp_0).norm().z )
      wp_1 = Position(wp_0.x+random.randint(2000,3000)*(wp_2-wp_0).norm().x, wp_0.y, wp_0.z+random.randint(2000,5000)*(wp_2-wp_0).norm().z)
      wp_5 = Position(wp_0.x+random.randint(2000,3000)*(wp_4-wp_0).norm().x, wp_0.y, wp_0.z+random.randint(4000,6000)*(wp_4-wp_0).norm().z)
      waypoints = [wp_0, wp_1, wp_2, wp_3, wp_4, wp_5]
      icon_pos = 0
      icons=[]
      mission_fp = find_group(mission_template, "Flight_Plan_"+side)
      for i,n in enumerate(waypoints):
        mission_blue_flight[side] = set_coords(mission_blue_flight[side], n, "wp_"+str(waypoints.index(n)))
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
        elif i == 3 or i == 4:
          labels = replace_substr( labels, "\n" + lcname+":", "\n", "Patrol") # write icon name
          labels = replace_substr( labels, "\n" + lcdesc+":", "\n", "Patrol between the two patrol waypoints") # write icon name
          icon_id = 201
        else:
          labels = replace_substr( labels, "\n" + lcname+":", "\n", "WP "+str(i)) # write icon name
          labels = replace_substr( labels, "\n" + lcdesc+":", "\n", "Waypoint") # write icon name
          icon_id = 901
        icons.append(MCU_Icon(index, [0], icon_id, coals, n.x, n.z, lcname, lcdesc ))
        icon_pos += 10

    if scenario[side] == 2:
      wp_3 = get_coords( mission_objective[side], "primary_objective" )
      if objective_type in objective_types_low.keys():
        wp_3.y = float(cloud_level) - 100.000 - random.random()*150.000
        mission_blue_flight[side] = mission_blue_flight[side].replace("AttackGTargets = 0", "AttackGTargets = 1")
      else:
        wp_3.y = 2500.000 + random.random()*1000
        mission_blue_flight[side] = mission_blue_flight[side].replace("AttackGround = 0", "AttackGround = 1")
      wp_0 = get_coords( mission_blue_flight[side], "wp_0" )
      wp_1 = Position(wp_0.x-random.randint(2000,6000)*(wp_3-wp_0).norm().x, wp_0.y, wp_0.z+(5000*(wp_3-wp_0).norm().z))
      wp_2 = Position(wp_3.x-(4000*(wp_3-wp_0).norm().x), wp_3.y, wp_3.z-random.randint(1000,3000)*(wp_3-wp_0).norm().z )
      wp_4 = Position(wp_3.x+random.randint(1000,4000)*(wp_3-wp_0).norm().x, wp_3.y, wp_3.z-(6000*(wp_3-wp_0).norm().z))
      wp_5 = Position(wp_0.x+(3000*(wp_3-wp_0).norm().x), wp_0.y, wp_0.z+random.randint(2000,5000)*(wp_3-wp_0).norm().z)
      waypoints = [wp_0, wp_1, wp_2, wp_3, wp_4, wp_5]
      icon_pos = 0
      icons=[]
      mission_fp = find_group(mission_template, "Flight_Plan_"+side)
      for i,n in enumerate(waypoints):
        mission_blue_flight[side] = set_coords(mission_blue_flight[side], n, "wp_"+str(waypoints.index(n)))
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
          labels = replace_substr( labels, "\n" + lcdesc+":", "\n", "Destroy the " + objective_type) # write icon name
          icon_id = 902
        else:
          labels = replace_substr( labels, "\n" + lcname+":", "\n", "WP "+str(i)) # write icon name
          labels = replace_substr( labels, "\n" + lcdesc+":", "\n", "Waypoint") # write icon name
          icon_id = 901
        icons.append(MCU_Icon(index, [0], icon_id, coals, n.x, n.z, lcname, lcdesc ))
        icon_pos += 10
        
    # Delete Red flight if no planes
    if fighter_count[side] == 0:
      mission_red_flight[side] = ""

    # Chain the icons and write to mission file
    for i,icon in enumerate(icons):
      if i == 5:
        icon.targets = [icons[0].index]
      else:
        icon.targets = [icons[i+1].index]
      mission_icons += str(icon)
    
    # Change search area to objective location in all groups
    for mcu in ["InterceptPlayer", "FlightDetected"]:
      mission_blue_flight[side] = set_coords(mission_blue_flight[side], wp_3, mcu)

    # Move AAA sites to random locations
    nf = mission_AAA_all.count("flak_"+side+"_") # number of object groups
    np = helper_group.count("AAA_"+side+"_") # number of possible locations
    lst = random.sample(range(1,np+1),nf)
    for i, site in enumerate(lst):
      mission_object_site = find_group(mission_AAA_all, "flak_"+side+"_"+str(i+1))
      D = get_coords(helper_group, "AAA_"+side+"_"+str(site) )
      new_group = position_group(mission_object_site, D)
      mission_AAA += new_group

  '''
    mission_options = replace_substr(mission_options, "WorldObjects\\Planes\\", ".txt" , plane_new)

  '''

  # Build mission file
  mission = (mission_header +
    mission_options +
    mission_blue_flight["allied"] +
    mission_blue_flight["axis"] +
    mission_red_flight["allied"] +
    mission_red_flight["axis"] +
    mission_patrols["allied"] +
    mission_patrols["axis"] +
    mission_AAA +
    mission_objective["allied"] +
    mission_objective["axis"] +
    mission_transports +
    mission_logic +
    mission_smoke +
    mission_static +
    mission_lines +
    mission_icons +
    mission_footer)

  # Generate briefing
  if cloud_type != 0:
    cloud_text =" at " + (str(cloud_level) + " m")
  else:
    cloud_text = ""
  mission_description = ("<b>Location: </b>Stalingrad area<br><br>"
  "<b>Date: </b>" + date_new + "<br><b>Time: </b>" + time_new + "<br><br>"
  "<b>Weather: </b>" + str(temp) + " \u00b0C, Clouds: " + cloud_desc + cloud_text + "<br>"
  "Wind strength is " + str(wind_speed) + " m/s from " + str(wind_dir + 180) + " degrees<br><br>"
  "<b>Your orders: </b><ul><li>Blue Flight will follow the orders that will be given at the start of the mission.</li>"
  "<li>Red Flight will wait for Blue flight to take off, then escort Blue Flight on it's mission.</li><br></ul>Good luck!<br>")

  # TEST
  # mission_description = "Have a great mission"
  # Add mission description
  lcname = find_substr(mission_options, "LCName = ", ";")
  lcdesc = find_substr(mission_options, "LCDesc = ", ";")
  lcauthor = find_substr(mission_options, "LCAuthor = ", ";")

  labels = labels.replace("<name>", mission_name) 
  labels = labels.replace("<description>", mission_description)
  labels = labels.replace("<author>", mission_author)
  #labels = replace_substr( labels, lcname+":", "\n", mission_name)
  #labels = replace_substr( labels, lcauthor+":", "\n", mission_author)
  #labels = replace_substr( labels, lcdesc+":", "\n", mission_description)

  # print("The chosen player plane = "+plane_new)
  # print("The chosen objective = "+objective)

  # Write coop mission
  mission_path = coop_path

  # Write the mission file
  with open(mission_path + mission_name + '.mission', 'w') as file:
    file.write(mission)
  
  # Write the description file. Desc files need UTF-16 encoding. .
  with open(mission_path + mission_name + '.eng', 'w', encoding='utf_16') as file:
    file.write(labels)

  # Convert to msbin file
  if msbin:
    #print(resaver_path)
    command_list = [".\MissionResaver.exe", "-d", data_path, "-f", mission_path + mission_name + ".mission"]
    #stream = os.popen(command_list)
    subprocess.run(command_list, cwd=resaver_path, shell=True)

  # Write the description file. Desc files need UTF-16 encoding. Note: resaver seems to destroy desc files (workaround).

  with open(mission_path + mission_name + '.eng', 'w', encoding='utf_16') as file:
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


#
# Main
#

if __name__ == "__main__":
  # Create random mission
  month = "%02d" % random.randint(9,11)
  #month = "09"
  date = "%02d" % random.randint(1, 30) + "." + month + ".1942"

  template_path="C:/Program Files (x86)/1C Game Studios/IL-2 Sturmovik Battle of Stalingrad/data/Multiplayer/Cooperative/"
  template_name="CoopTemplate_1"
  mission_name = "CoopStalingrad_01"
  GenerateMission("CoopStalingrad_01", template_path, template_name, date, True)