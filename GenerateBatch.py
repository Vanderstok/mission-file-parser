import MissionConstructor
import configparser

#template_path="C:/Program Files (x86)/1C Game Studios/IL-2 Sturmovik Battle of Stalingrad/data/Multiplayer/Cooperative/"
#template_name="CoopTemplate_1"

# write stuff to config:
#
# how is time of date determined?

config = configparser.ConfigParser()
config.read('config.ini')
il2_path = config['DEFAULT']['il2_path']
mission_prefix = "CoopGenerated_"
template_path = config['DEFAULT']['template_path']
config['MISSION']['side'] = "0"
config['MISSION']['weather'] = "0"
config['MISSION']['intercept_chance_axis'] = "high"
config['MISSION']['intercept_chance_allied'] = "high"
config['MISSION']['plane_start'] = "runway"
config['MISSION']['fighter_count_allied'] = "4"
config['MISSION']['fighter2_count_allied'] = "4"
config['MISSION']['bomber_count_allied'] = "4"
config['MISSION']['fighter_count_axis'] = "4"
config['MISSION']['fighter2_count_axis'] = "4"
config['MISSION']['bomber_count_axis'] = "4"
for side in ["allied", "axis"]:
    config['MISSION']['scenario_' + side] = "0"
with open("config.ini", "w" ) as configfile:
    config.write(configfile)

i=1
for month in [9,10,11,12]:
    for date in [7,14,21,28]:
        date_new = "%02d" %date + "." + "%02d" %month + ".1942"
        print("Generating mission for: "+date_new)
        if i<10:
            MissionConstructor.GenerateMission(mission_prefix + "0"+ str(i), template_path, date_new)
        else:
            MissionConstructor.GenerateMission(mission_prefix + str(i), template_path, date_new)
        i += 1
