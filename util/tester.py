'''
Created on 04-Apr-2014

@author: pushkar
'''
from sys import argv
from analyze import Analyze



yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
magenta = (255, 0, 255)

legs_all = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']
T2 = ['L2', 'R2']
T3 = ['L3', 'R3']

path = argv[1]
ana = Analyze(path)

# [ana.labelLeg(leg, 'SWING_MODE', green) for leg in legs_all]
# [ana.labelLeg(leg, 'STANCE_MODE', magenta) for leg in legs_all]
# [ana.labelLeg(leg, 'SWING_MODE', green) for leg in T2]
# [ana.labelLeg(leg, 'STANCE_MODE', magenta) for leg in T2]
# ana.labelLeg('L3', 'SWING_MODE', green)
# ana.genGaitDiagram()
# ana.genGaitPaint()


# for leg in legs_all:
	# print 'Swing Dur',ana.getSwingDuration(leg)
	# print 'Swing Amp',ana.getSwingAmplitude(leg)

# print "PEA", ana.getPEA("R3")

	

# [ana.labelLeg(leg, 'SWING_MODE', green) for leg in T2]
[ana.labelLeg(leg, 'SWING_MODE', green) for leg in legs_all]
[ana.labelLeg(leg, 'STANCE_MODE', red) for leg in legs_all]


#[ana.labelLeg(leg, 'SWING_MODE', magenta) for leg in legs_all]
#[ana.labelLeg(leg, 'STANCE_MODE', magenta) for leg in legs_all]

#for leg in legs_all:
#	print 'Swing Dur', ana.getSwingDuration(leg)
#for leg in legs_all:
#	print 'Swing Amp', ana.getSwingAmplitude(leg)
#for leg in legs_all:
#	print 'Stance Amp', ana.getStanceAmplitude(leg)


ana.genGaitDiagram()
# ana.genGaitPaint()
# ana.genGaitPlot()

print('Walk speed', int(ana.getWalkingSpeed()[0]))

