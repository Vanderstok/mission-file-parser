import MissionConstructor

for i in range(1,10):
    if i<10:
        MissionConstructor.GenerateMission("CoopStalingrad_0" + str(i))
    else:
        MissionConstructor.GenerateMission("CoopStalingrad_" + str(i))
