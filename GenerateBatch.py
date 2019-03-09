import MissionConstructor
import configparser

template_path="C:/Program Files (x86)/1C Game Studios/IL-2 Sturmovik Battle of Stalingrad/data/Multiplayer/Cooperative/"
template_name="CoopTemplate_1"

# write stuff to config:
#
# how is time of date determined?

config = configparser.ConfigParser()
config.read('config.ini')
config['MISSION']['side'] = "0"
config['MISSION']['weather'] = "0"
for side in ["allied", "axis"]:
    config['MISSION']['scenario_' + side] = "0"
with open("config.ini", "w" ) as configfile:
    config.write(configfile)

i=1
for month in [9,10,11]:
    for date in [4,9,15,20,28]:
        date_new = "%02d" %date + "." + "%02d" %month + ".1942"
        if i<10:
            MissionConstructor.GenerateMission("CoopStalingrad_0" + str(i), template_path, template_name, date_new)
        else:
            MissionConstructor.GenerateMission("CoopStalingrad_" + str(i), template_path, template_name, date_new)
        i += 1
