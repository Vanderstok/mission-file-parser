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
map_name = "Kuban"
#mission_prefix = "CoopStalingrad_"
mission_prefix = "CoopKuban_"
template_path = config['DEFAULT']['template_path']
msbin = {"0": False, "1": True}[config['DEFAULT']['create_msbin']]
config['MISSION']['side'] = "0"
config['MISSION']['weather'] = "0"
config['MISSION']['intercept_chance_axis'] = "high"
config['MISSION']['intercept_chance_allied'] = "high"
config['MISSION']['plane_start'] = "runway"
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
            MissionConstructor.GenerateMission(mission_prefix + "0"+ str(i), template_path, map_name, date_new, msbin)
        else:
            MissionConstructor.GenerateMission(mission_prefix + str(i), template_path, map_name, date_new, msbin)
        i += 1
