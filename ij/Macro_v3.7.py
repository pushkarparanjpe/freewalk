###
#Author: Pushkar Paranjpe
###

import sys
sys.path.append('/home/pushkar/python/ij_util/')
from ij_util import *
from shutil import rmtree
import commands
from os.path import join as pjoin, exists as pexists
from os import makedirs as mdirs
from sys import exit
from ij.gui import GenericDialog
import ConfigParser
from ij.io import OpenDialog



legnames = {0:"L1",1:"L2",2:"L3",3:"R1",4:"R2",5:"R3"}

img_w = 200
img_h = 200


#Function Space
#-------------------------------------------------------------------------------------------------------------------------
def setProp(path, key, val):
	propfilepath = pjoin(path, 'props.cfg')
	config = ConfigParser.RawConfigParser()
	config.read(propfilepath)
	section = 'Properties'
	if config.has_section(section):
		config.set(section,key,val)
	configfile = open(propfilepath, 'wb')
	config.write(configfile)
	configfile.close()


def loadProps(path):
	config = ConfigParser.RawConfigParser()
	#ordered list of property keys
	keys = (
		'DEBUG',
		'thresh',
		'fly_area',
		'fly_area_error',
		'fly_area_start',
		'fly_area_end',
		'dlimit',
		'leg_area',
		'leg_area_error',
		'leg_area_start',
		'leg_area_end',
		'tmp_dir',
		'tmp_legs_dir',
		'bleg_rois',
	)
	#dict of property:info pairs
	#info = [text, value, digits, cols, unit]
	properties = dict(
			zip(keys,
			(
			['DEBUG', False],
			['Threshold',		-1.0,	1,	6,	'pixels'],
			['Fly Area',		3000.0,	1,	6,	'pixels'],
			['Fly Area Error',	60.0,	1,	6,	'%'],
			['Fly Area Start',	0.0,	1,	6,	'pixels'],
			['Fly Area End',	0.0,	1,	6,	'pixels'],
			['"d" Search Limit',	15.0,	1,	6,	'pixels'],
			['Leg Area',		35.0,	1,	6,	'pixels'],
			['Leg Area Error',	95.0,	1,	6,	'%'],
			['Leg Area Start',	0.0,	1,	6,	'pixels'],
			['Leg Area End', 	0.0,	1,	6,	'pixels'],
			['TMP Dir',			'tmp'],
			['TMP Dir',			'legs'],
			['Leg ROIs exist', False],
			)
			))
			
	propfilepath = pjoin(path, 'props.cfg')
	section = 'Properties'
	if pexists(propfilepath):
		config.read(propfilepath)
		propget = {int: config.getfloat , float: config.getfloat, str: config.get, bool: config.getboolean}	
		for key in keys:
			#print key
			valtype = type(properties[key][1])
			if config.has_option(section,key):
				val = propget[valtype](section, key)
				print key,val
				properties[key][1] = val
	#within dict, dependent variables
	properties['fly_area_start'][1] = properties['fly_area'][1]*(1 - properties['fly_area_error'][1]/100)
	properties['fly_area_end'][1] = properties['fly_area'][1]*(1 + 2*properties['fly_area_error'][1]/100)
	properties['leg_area_start'][1] = properties['leg_area'][1]*(1 - properties['leg_area_error'][1]/100)
	properties['leg_area_end'][1] = properties['leg_area'][1]*(1 + properties['leg_area_error'][1]/100)
	#
	gd = GenericDialog('Extraction Properties')
	fieldset = {int: gd.addNumericField , float: gd.addNumericField, str: gd.addStringField, bool: gd.addCheckbox}
	[ fieldset[type(properties[key][1])](*properties[key]) for key in keys ]
	gd.showDialog()
	fieldget = {int: gd.getNextNumber , float: gd.getNextNumber, str: gd.getNextString, bool: gd.getNextBoolean}

	if not config.has_section(section):	config.add_section(section)
	for key in keys:
		valtype = type(properties[key][1])
		val = fieldget[valtype]()
		config.set(section, key, val)
	configfile = open(propfilepath, 'wb')
	config.write(configfile)
	configfile.close()
	print 'Saved props to',propfilepath
	return properties


def getFarthestPositiveX(X):
	print X
	farX = max(X, key=diffd)
	print "Farthest >>",farX
	return farX


def getFarthestCoords(XY):
	farX, farY = max(XY, key=euclid)
	return (farX, farY)


def euclid(xy):
	x,y = xy
	cX = img_w/2
	cY = img_h/2
	return ( (cX-x)**2 + (cY-y)**2 ) ** 0.5


def distance(x1,y1,x2,y2):
	return ( (x2-x1)**2 + (y2-y1)**2 ) ** 0.5


def diffd(x):
	cX = img_w/2
	return x-cX


def getAreaEstimate(X,Y):
	ae = (max(X)-min(X)) * (max(Y)-min(Y))
	print "Particle Area Estimate:",ae
	return ae


#shrink the ROI by SHRINK pixels,
# then keep shrinking by 1 pixel until the resulting selection is non-composite,
#finally enlarge the ROI by ENLARGE pixels
def shrinkEnlarge(snip=False):
	SHRINK = -5
	ENLARGE = abs(SHRINK) + 1
	run("Enlarge...", "enlarge="+str(SHRINK))
	k = 0
	while(selectionType() not in [2,3,4]):	#a WHILE block to eliminate composite selection events
		run("Enlarge...", "enlarge=-1")
		k += 1
	run("Enlarge...", "enlarge="+str(ENLARGE+k))
	#Fit an ellipse to smoothen the ROI perimeter
	#to help reduce Y-jitter
	run("Fit Ellipse")
	run("Enlarge...", "enlarge=2")
	#

	if snip:
		roiUpdate()
		#Clip Antennae
		X,Y = getSelectionCoordinates()
		farX = int(getFarthestPositiveX(X))
		w = 15
		h = 15
		makeRectangle(farX-w/2,img_w/2-h/2,w,h)
		#debug("Antennae Clipping",1000)
		setForegroundColor(255, 255, 255)
		run("Fill", "slice")
		#wait(1000)
		selectNone()
		roiSelect(0)
		#


#finds null slices and fills them with an roi of
#the next slice if "reverse" is set to be True or
#fills them with an roi of the previous slice by default
def nullRemover(reverse=True):
	#myxs = range(4)
	#myys = range(4)
	myxs = None
	myys = None

	setForegroundColor(0, 0, 0)

	#go through the stack backwards
	if reverse: print '<<'
	start = getNSlices()
	end = 0
	step = -1
	
	if not reverse:
		print '>>'
		#go through the stack forwards
		start = 1
		end = getNSlices()+1
		step = 1
		
	for ctr in range(start,end,step):
		setSlice(ctr)
		run("Select None")
		stats = getStatistics()
		if stats.max:
			run("Create Selection")
			myxs, myys = getSelectionCoordinates()
		elif myxs and myys:
			makePolygon(myxs,myys)
			run("Fill", "slice")

	run("Select None")


def renewdir(base_path,*dirname):
	tmp_path = pjoin(base_path,*dirname)
	if pexists(tmp_path):
		rmtree(tmp_path)	#Delete the tmp directory tree
		print "DELETED previous directory: "+tmp_path
	if not pexists(tmp_path):
		mdirs(tmp_path)	#Create the tmp directory
		print("CREATED directory: "+tmp_path)


def debug(tag,t=15000):
	#if DEBUG:
	print "[",tag,"]"
	wait(t)


#Execution Space
#-------------------------------------------------------------------------------------------------------------------------

print "Clean-up"
reset()


print "Movie Loading and Pre-Processing..."
print "-----------------------------------"
od = OpenDialog("Choose Fly Movie TIF file", None)
path = od.getDirectory()
print path

filename = od.getFileName()
loadMovieFull(pjoin(path,filename))
to8bit()
#run("In [+]")
run("Gaussian Blur...", "sigma=1 stack")


#padding
setBackgroundColor(255, 255, 255)
width, height, nChannels, nSlices, nFrames = getDimensions()
newwidth = width * 2
newheight = height * 2
if (newwidth - width) < 300:	#impose a minimum of 150px flanking each side
	newwidth = width + 200
run("Canvas Size...", "width="+str(newwidth)+" height="+str(newheight)+" position=Center")
#

pty = loadProps(path)
DEBUG = pty['DEBUG'][1]
thresh = pty['thresh'][1]
fly_area = pty['fly_area'][1]
fly_area_error = pty['fly_area_error'][1]
fly_area_start = pty['fly_area_start'][1]
fly_area_end = pty['fly_area_end'][1]
print "Set Fly Area range:",fly_area_start,fly_area_end
leg_area = pty['leg_area'][1]
leg_area_error = pty['leg_area_error'][1]
leg_area_start = pty['leg_area_start'][1]
leg_area_end = pty['leg_area_end'][1]
print "Set Leg Area range:",leg_area_start,leg_area_end

#tmp directory
tmp_dir = pty['tmp_dir'][1]
tmp_legs_dir = pty['tmp_legs_dir'][1]
bleg_rois = pty['bleg_rois'][1]
print '>>>>',bleg_rois

print "tmp directory..."
print "----------------"
renewdir(path,tmp_dir)


print "Finding the Fly..."
print "------------------"
selectWindow(filename)
duplicate("src")
selectWindow("src")

#===============================================================
#THRESHOLD#
if thresh == -1:
	thresh = getString("Threshold ?","")
	setProp(path, 'thresh', thresh)
#setThreshold(0, int(thresh))
#setThreshold(0, 150)	#for CS-3280Lux
#setThreshold(0, 104)	#for CS-Slow
#setThreshold(0, 142)	#for CS-Slow/15/
setThreshold(0, 67)	#for all RNAi data
#===============================================================
run("Convert to Mask", " ")
rename("Mask")
bin_open(mode="stack")
#wait(10000)
run("Analyze Particles...", "size="+str(fly_area_start)+"-"+str(fly_area_end)+" circularity=0.00-1.00 show=Nothing add stack")
count = roiCount()

#Fly centroid, body length extraction code
clearResults()
run("Set Measurements...", "  centroid fit stack redirect=None decimal=3")	#find centroid, fit ellipse, find major axis
#for ctr in range(count):
#	roiSelect(ctr)
#	shrinkEnlarge()
#	measure()
roiDeselect()
selectNone()
roiMeasure()
saveResults(pjoin(path,tmp_dir,"fly_free.tsv"))
#
selectWindow("Mask")
#wait(10000)
close()

print count,"flies suspected"
#run("In [+]")
if(count != getNSlices()):
	mssg = "Fly detection error: ["+str(count-getNSlices())+"]"
	showMessage(mssg)
	exit(mssg)


print filename
selectWindow(filename)
#wait(10000)
print "Cropping..."
print "-----------"
#>> Crop to selection
for ctr in range(count):
	#print 1
	roiSelect(ctr)
	#print 2
	#shrinkEnlarge()
	#
	#print 3
	run("To Bounding Box")
	#print 4
	run("Scale... ", "x=3.0 y=6.0 centered")
	#print 5
	run("Duplicate...", "title=frame")
	#print 6
	run("Canvas Size...", "width=200 height=200 position=Center")
	#print 7
	#clean-up inset
	#run("Select All")
	#run("Scale... ", "x=0.9 y=0.70 centered")
	#run("Make Inverse")
	#setForegroundColor(255, 255, 255)
	#run("Fill", "stack")
	#
	crop_path = pjoin(path,tmp_dir,"f"+str(ctr)+".jpeg")
	run("Save", "save=["+crop_path+"]")
	close()

#close the avi
close()
#roiReset()
#run("Select None")


print "Loading cropped stack..."
print "------------------------"
#>> Load the cropped frames
count = roiCount()
loadStack(pjoin(path,tmp_dir,"f0.jpeg"),count,1)
setThreshold(0, int(thresh))
run("Convert to Mask", " ")
IJ.run("Grid Overlay", "tile=10 tile=10 color=Cyan")

#			***	Automatic Leg Identification	***
#=========================================================================================================
print "Rat's Tail ==> Area Sort (Select Top 6) ==> Area Min Thresh"
print "---------------------------------------------------------------"

x1 = None
y1 = None


#>> Erase the body, leave the appendages
for ctr in range(getNSlices()):
	#in a slice, find the fly and add it ROI to RM
	print "Slice",ctr+1
	setSlice(ctr+1)
	roiDeselect()
	selectNone()
	roiReset()
	bin_open()
	run("Analyze Particles...", "size="+str(fly_area_start)+"-"+str(fly_area_end)+" circularity=0.00-1.00 show=Nothing add slice")
	roiSelect(0)
	
	#Shrink and then enlarge the fly ROI
	#to get the torso-only ROI
	shrinkEnlarge(True)
	#
	#debug("Shrink Enlarge",3000)

	#Clear-out the torso completely
	setForegroundColor(255, 255, 255)
	run("Fill", "slice")
	#
	#debug("Torso Clearing")

	#Find "leg particles"
	roiReset()
	selectNone()
	run("Analyze Particles...", "size=1-Infinity circularity=0.00-1.00 show=Nothing add slice")	
	particlecount = roiCount()
	X = []
	Y = []
	#Find particle/s within "dlimit" distance - "Radial Search"
	#for k in range(particlecount):
	#	roiSelect(k)
	#	x2,y2 = map(mean,getSelectionCoordinates())
	#	X.append(x2)
	#	Y.append(y2)
	#if x1 and y1:
	#	coords = [[x1,y1,x2,y2] for x2,y2 in X,Y]
	#	cands = filter(lambda c: distance(c) <= dlimit, coords)
	
	
	#Choose largest particle if more than one matching particles were found

	#Sort leg particles by size if particle count > 6
	if particlecount > 6:
		roisizes = []
		for k in range(particlecount):
			roiSelect(k)
			X,Y = getSelectionCoordinates()
			roisizes.append([k,getAreaEstimate(X,Y)])
		roisizes = sorted(roisizes,key = lambda j: j[1], reverse=True)
		print roisizes
		#Then keep the 6 largest particles and clear the rest
		rois = []
		for k in range(6, len(roisizes)):
			selectNone()
			j = roisizes[k][0]
			roiSelect(j)
			print "Filling ROI j:",j
			setForegroundColor(255, 255, 255)
			run("Fill", "slice")
			rois.append(j)
		roiSelectMany(rois)
		roiDelete()
		selectNone()

	legcount = roiCount()
	for k in range(legcount):
		selectNone()
		roiSelect(k)
		setForegroundColor(255, 255, 255)
		run("Fill", "slice")
		print "Filled a Leg ..."
		#if ctr>28 and ctr<35:	wait(2000)
		X,Y = getSelectionCoordinates()
		farX, farY = map(int,getFarthestCoords(zip(X,Y)))
		makeEllipse(farX,farY,3,3)
		setForegroundColor(0, 0, 0)
		run("Fill", "slice")
		#wait(1000)


#print "Legs pre-filtering..."
#print "---------------------"
selectNone()
rename("Mask of tmp")
#run("Analyze Particles...", "size="+str(leg_area_start)+"-"+str(leg_area_end)+" circularity=0.00-1.00 show=Masks stack")
#run("Analyze Particles...", "size="+str(leg_area_start)+"-Infinity circularity=0.00-1.00 show=Masks stack")
#selectWindow("tmp")
#close()
#debug("DEBUG - Mask of tmp")

print "Legs tmp directory..."
print "-----------------------------------"
renewdir(path,tmp_dir,tmp_legs_dir)

print "Z temporal color-coded projection mask..."
print "--------------------"
IJ.run("Temporal-Color Code", "lut=physics start=1 end="+str(getNSlices())+" create");
close()
run("In [+]")
#run("In [+]")
#run("In [+]")

roiReset()


#>>Prompt user for manual leg domain selection from the color-coded Z-projection mask
for j in range(6):
	if bleg_rois:
		loadROI(path,legnames[j]+'.roi')
		wait(2000)
	else:
		IJ.runMacro('waitForUser("Select Leg ROI")')
	saveROI(path,legnames[j]+'.roi')
	coords = getSelectionCoordinates()
	if coords is None:
		print '[[[ NULL SELECTION COORDINATES ]]]'
	makePolygon(*coords)
	run("Create Mask")
	rename("leg-mask")
	IJ.runMacro('imageCalculator("AND create stack", "Mask of tmp","leg-mask")')
	#debug("Mask AND Leg")
	print "NullRemover - Back and Forth"
	print '-----------------------------'
	nullRemover()			#Reverse copy
	nullRemover(reverse=False)	#Forward copy
	clearResults()
	print 'Saving Leg Tip Co-ordinates'
	print '-----------------------------'
	for k in range(1,getNSlices()+1):
		setSlice(k)
		selectNone()
		createSelection()
		X,Y = getSelectionCoordinates()
		#setResultRow(["X","Y"],[mean(X),mean(Y)])
		farXY = getFarthestCoords(zip(X,Y))	#a quick way to exclude multiple-point selections that occur especially with T3 (and T1)
		setResultRow(["X","Y"],farXY)
	saveResults(pjoin(path,tmp_dir,tmp_legs_dir,legnames[j]+".tsv"))
	close()
	close()
setProp(path,"bleg_rois",True)


#Call the simpleplot.py to generate a single file that contains the values of the specified parameter for all 6 legs and then display a line plot
#and annotate fly frames for swing events
#import commands
#print commands.getstatusoutput('/usr/bin/python /home/pushkar/python/walking_videos/simpleplot.py "'+path+'tmp/legs/"')

#Call the tester.py to generate a gait diagram and annotae all-6-swings
print 'Wait!'
print 'Generating gait diagram...'
import commands
print commands.getstatusoutput('/home/pushkar/Documents/Workspace/freewalk/.venv/bin/python /home/pushkar/Documents/Workspace/freewalk/util/tester.py "'+path+'/"')


print "Finished Analysis.\n["+path+"]"











