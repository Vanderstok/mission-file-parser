
import tkinter as tk
from tkinter import filedialog
import configparser
import json
import MissionConstructor

def return_menu():
    print("Return to Main Menu")

def create_mission():
    print ("Chosen plane is: "+ fighter_type.get())
    print ("In a formation of: "+ str(fighter_count.get()))
    print (mission_target.get())
    config['MISSION']['side'] = side
    config['MISSION']['fighter_type'] = fighter_type.get()
    config['MISSION']['bomber_type'] = bomber_type.get()
    config['MISSION']['fighter_count'] = fighter_count.get()
    config['MISSION']['bomber_count'] = bomber_count.get()
    config['MISSION']['start_location'] = start_location.get()
    config['MISSION']['fighter_skill'] = fighter_skill.get()
    config['MISSION']['mission_target'] = mission_target.get() 
    config['MISSION']['mission_time'] = mission_time.get()
    config['MISSION']['mission_wind'] = mission_wind.get()
    config['MISSION']['mission_cloud'] = mission_cloud.get()
    with open("config.ini", "w" ) as configfile:
        config.write(configfile)
    MissionConstructor.GenerateMission( "foo", "foo", False)

def change_targets(val):
    if val in ["IL-2 AM-38", "Ju 87 D-3", "Hs 129 B-2"]:
        targets = ["airfield", "artillery", "armor"]
    else:
        targets = ["airfield", "artillery", "armor", "train", "dump", "bridge"]
    mission_target.set(targets[0])
    mission_target_menu['menu'].delete(0,'end')
    for choice in targets:
        mission_target_menu['menu'].add_command(label=choice, command=tk._setit(mission_target, choice))
    print (val)

def change_side():
    global side
    global background
    global fighters
    global fighter_menu
    global bombers
    global bomber_menu
    if side == "allied":
        side = "axis"
    else:
        side = "allied"
    photo = tk.PhotoImage(file={"allied":"PE2.png", "axis":"HE111.png"}[side])
    background.configure(image=photo)
    background.image = photo
    fighter_type.set(fighters[side][0])
    bomber_type.set(bombers[side][0])    
    fighter_menu['menu'].delete(0,'end')
    bomber_menu['menu'].delete(0,'end')
    for choice in fighters[side]:
        fighter_menu['menu'].add_command(label=choice, command=tk._setit(fighter_type, choice))
    for choice in bombers[side]:
        bomber_menu['menu'].add_command(label=choice, command=tk._setit(bomber_type, choice, change_targets))

def change_path():
    global il2_path
    il2_path = filedialog.askdirectory()
    if il2_path != "":
        status.configure(text="IL2 game folder: "+ il2_path)

global side
global fighters
global bombers

# Read config
config = configparser.ConfigParser()
config.read('config.ini')
il2_path = config['DEFAULT']['il2_path']

side = config['MISSION']['side']
fighter_type_c = config['MISSION']['fighter_type']
bomber_type_c = config['MISSION']['bomber_type']
fighter_count_c = config['MISSION']['fighter_count']
bomber_count_c = config['MISSION']['bomber_count']
start_location_c = config['MISSION']['start_location']
fighter_skill_c = config['MISSION']['fighter_skill']
mission_target_c = config['MISSION']['mission_target']
mission_time_c = config['MISSION']['mission_time']
mission_wind_c = config['MISSION']['mission_wind']
mission_cloud_c = config['MISSION']['mission_cloud']

fighters_red = config['PLANES']['fighters_allied']
fighters_blue = config['PLANES']['fighters_axis']
bombers_red = config['PLANES']['bombers_allied']
bombers_blue = config['PLANES']['bombers_axis']
fighters_allied = list(json.loads(fighters_red.replace("'", "\"")))
fighters_axis = list(json.loads(fighters_blue.replace("'", "\"")))
bombers_allied = list(json.loads(bombers_red.replace("'", "\"")))
bombers_axis = list(json.loads(bombers_blue.replace("'", "\"")))

fighters = { "allied": fighters_allied, "axis": fighters_axis }
bombers = { "allied": bombers_allied, "axis": bombers_axis}

root = tk.Tk()
w,h = 720, 472
root.minsize(width=w, height=h)
root.maxsize(width=w, height=h)
root.title("Coop Mission Creator for IL2 BOX")

# Title

title_frame = tk.Frame(root)
title_frame.pack()

text_title = tk.Label(title_frame, text="Create a Cooperative Mission")
text_title.config(font=('bold', 20))
text_title.pack(pady=10)

# Picture

photo_frame = tk.Frame(root)
photo_frame.pack()
photo = tk.PhotoImage(file={"allied":"PE2.png", "axis":"HE111.png"}[side])
global background
background = tk.Label(photo_frame, image=photo)
background.image = photo
background.pack()

# Mission Options

text_frame = tk.Frame(root)
text_frame.pack(fill=tk.X, padx=10, pady=20)

line_1 = tk.Label(text_frame)
line_2 = tk.Label(text_frame)
line_3 = tk.Label(text_frame)
line_4 = tk.Label(text_frame)
line_5 = tk.Label(text_frame)

line_1.pack(padx=20)
line_2.pack()
line_3.pack()
line_4.pack()
line_5.pack()

fighter_type = tk.StringVar(line_1)
fighter_type.set(fighter_type_c)

bomber_type = tk.StringVar(line_1)
bomber_type.set(bomber_type_c)

fighter_counts = ["1", "2", "3", "4"]
fighter_count = tk.StringVar(line_1)
fighter_count.set(fighter_count_c)

bomber_counts = ["1", "2", "3", "4"]
bomber_count = tk.StringVar(line_1)
bomber_count.set(bomber_count_c)

start_locations = ["close to", "far from"]
start_location = tk.StringVar(line_2)
start_location.set(start_location_c)

fighter_skills = ["rookie", "regular", "veteran"]
fighter_skill = tk.StringVar(line_2)
fighter_skill.set(fighter_skill_c)

mission_targets = ["airfield", "artillery", "armor", "train", "dump", "bridge"]
mission_target = tk.StringVar(line_3)
mission_target.set(mission_target_c)

mission_times = ["dawn", "morning", "noon", "afternoon", "dusk", "night"]
mission_time = tk.StringVar(line_3)
mission_time.set(mission_time_c)

mission_winds = ["light", "moderate", "strong"]
mission_wind = tk.StringVar(line_3)
mission_wind.set(mission_wind_c)

mission_clouds = ["no clouds", "few clouds", "medium clouds", "heavy clouds"]
mission_cloud = tk.StringVar(line_3)
mission_cloud.set(mission_cloud_c)

# Line 1

text_1 = tk.Label(line_1, text="You will fly either a ")
text_1.pack(side=tk.LEFT, pady=8)

global fighter_menu
fighter_menu = tk.OptionMenu(line_1, fighter_type, *fighters[side])
fighter_menu["highlightthickness"]=0
fighter_menu["width"]=15
fighter_menu.pack(side=tk.LEFT)

text_2 = tk.Label(line_1, text=" fighter or a ")
text_2.pack(side=tk.LEFT)

global bomber_menu
bomber_menu = tk.OptionMenu(line_1, bomber_type, *bombers[side], command=change_targets)
bomber_menu["highlightthickness"]=0
bomber_menu["width"]=12
bomber_menu.pack(side=tk.LEFT)

text_3 = tk.Label(line_1, text=" bomber, which the fighters will escort.")
text_3.pack(side=tk.LEFT)

# Line 2

text_4 = tk.Label(line_2, text="There will be  ")
text_4.pack(side=tk.LEFT)

fighter_count_menu = tk.OptionMenu(line_2, fighter_count, *fighter_counts)
fighter_count_menu["highlightthickness"]=0
fighter_count_menu["width"]=2
fighter_count_menu.pack(side=tk.LEFT)

text_5 = tk.Label(line_2, text=" fighters with mostly ")
text_5.pack(side=tk.LEFT)

fighter_skill_menu = tk.OptionMenu(line_2, fighter_skill, *fighter_skills )
fighter_skill_menu["highlightthickness"]=0
fighter_skill_menu["width"]=6
fighter_skill_menu.pack(side=tk.LEFT)

text_6 = tk.Label(line_2, text=" pilots and a flight of ")
text_6.pack(side=tk.LEFT)

bomber_count_menu = tk.OptionMenu(line_2, bomber_count, *bomber_counts)
bomber_count_menu["highlightthickness"]=0
bomber_count_menu["width"]=2
bomber_count_menu.pack(side=tk.LEFT)

text_7 = tk.Label(line_2, text=" bombers. ")
text_7.pack(side=tk.LEFT)

# Line 3

text_8 = tk.Label(line_3, text="The start location will be ")
text_8.pack(side=tk.LEFT)

target_location_menu = tk.OptionMenu(line_3, start_location, *start_locations)
target_location_menu["highlightthickness"]=0
target_location_menu["width"]=6
target_location_menu.pack(side=tk.LEFT)

text_9 = tk.Label(line_3, text=" the front. The objective is to destroy a")
text_9.pack(side=tk.LEFT)

mission_target_menu = tk.OptionMenu(line_3, mission_target, *mission_targets )
mission_target_menu["highlightthickness"]=0
mission_target_menu["width"]=10
mission_target_menu.pack(side=tk.LEFT)

# Line 4

text_10 = tk.Label(line_4, text="It is ")
text_10.pack(side=tk.LEFT)

mission_time_menu = tk.OptionMenu(line_4, mission_time, *mission_times)
mission_time_menu["highlightthickness"]=0
mission_time_menu["width"]=8
mission_time_menu.pack(side=tk.LEFT)

text_11 = tk.Label(line_4, text=". The winds are ")
text_11.pack(side=tk.LEFT)

mission_wind_menu = tk.OptionMenu(line_4, mission_wind, *mission_winds )
mission_wind_menu["highlightthickness"]=0
mission_wind_menu["width"]=7
mission_wind_menu.pack(side=tk.LEFT)

text_12 = tk.Label(line_4, text=" and the sky has ")
text_12.pack(side=tk.LEFT)

mission_cloud_menu = tk.OptionMenu(line_4, mission_cloud, *mission_clouds )
mission_cloud_menu["highlightthickness"]=0
mission_cloud_menu["width"]=13
mission_cloud_menu.pack(side=tk.LEFT)

# Buttons

button_menu = tk.Button(text_frame, text="Set IL2 mission path", command=change_path)
button_menu.pack(side=tk.LEFT, padx=10, pady=10)
button_menu = tk.Button(text_frame, text="Change Side", command=change_side)
button_menu.pack(side=tk.LEFT, padx=10, pady=10, expand=1 )
button_create = tk.Button(text_frame, text="Create Mission", command=create_mission)
button_create.pack(side=tk.RIGHT, padx=10, pady=10)

# Status bar

status = tk.Label(root, text="IL2 game folder: " + il2_path, bd=2, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side=tk.BOTTOM, fill=tk.X)


color = '#F9F9F9'
text_frame.configure(bg = color)
for wid in text_frame.winfo_children():
    wid.configure(bg = color)
    for but in wid.winfo_children():
        but.configure(bg = color)

root.mainloop()