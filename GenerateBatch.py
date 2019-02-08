import MissionConstructor

i=1
for month in [9,10,11]:
    for date in [4,9,15,20,28]:
        date_new = "%02d" %date + "." + "%02d" %month + ".1942"
        if i<10:
            MissionConstructor.GenerateMission("CoopStalingrad_0" + str(i), date_new)
        else:
            MissionConstructor.GenerateMission("CoopStalingrad_" + str(i), date_new)
        i += 1

# Create batch based on Date