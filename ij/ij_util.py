###
#Author: Pushkar Paranjpe
###

from ij.measure import ResultsTable as RT
from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi, PolygonRoi
from ij.plugin import ImageCalculator as IC, Duplicator
from os.path import join as pjoin
import pickle
from ij.gui import Line


#Image Calculator functions
#------------------------------------------------------
def calculate(str_comm,imp1,imp2):
	ic = IC()
	ic.run(str_comm,imp1,imp2)


#Math functions
def mean(arr):
	return sum(arr)/float(len(arr))


#"Metadata" functions - applicable to TIFF format files
#------------------------------------------------------
def setMetadata(dictobj):
	namespace = "CUSTOM_INFO"
	


def ImageJDirPath():
	return IJ.getDirectory("imagej")


#user input / dialog Functions
#-------------------------------

"""
	Get and return user specified String input
"""
def getString(mssg,default):
	return IJ.getString(mssg,default)


"""
	 Delays 'msecs' milliseconds.
"""
def wait(msecs):
	IJ.runMacro('wait('+str(msecs)+')')



"""
	 Waits for user input and shows non-modal mssg.
"""
def waitForUser(mssg):
	IJ.runMacro('waitForUser("'+mssg+'")')

"""
	 Shows modal mssg.
"""
def showMessage(mssg):
	IJ.runMacro('showMessage("'+mssg+'")')


"""
	Saves the image to path
"""
def save(path):
	IJ.save(path)


def setAutoThreshold():
	imp = IJ.getImage()
	IJ.setAutoThreshold(imp,"Default")


def setThreshold(lt, ut):
	IJ.setThreshold(lt,ut)


def to8bit():
	run("8-bit", "")


def loadROI(path,roiname):
	IJ.open(pjoin(path,roiname))


"""
	Load the images stack
"""
def loadStack(path,count,start):
	run("Image Sequence...", "open=["+path+"] number="+str(count)+" starting="+str(start)+" increment=1 scale=100 file=[] sort")


"""
	Load FULL video stack
"""
def loadMovieFull(path):
	IJ.open(path)


"""
	Load the video stack
"""
def loadMovie(path,start,end):
	run("AVI...", "select=["+path+"] first="+str(start)+" last="+str(end))
	run("In")


"""
	Load the video stack in 8-bit mode
"""
def loadMovie8bit(path,start,end):
	run("AVI...", "select=["+path+"] first="+str(start)+" last="+str(end)+" convert")
	run("In")
	rename("Source")



#Results table Functions
#----------------------

def getNResults():
	return RT.getResultsTable().getCounter()


"""
	Save Results
"""
def saveResults(path):
	IJ.saveAs("Results", path);


"""
	Clears the Results table
"""
def clearResults():
	#RT.getResultsTable().reset()
	run("Clear Results", "")


"""
	Update results table
"""
def updateResults():
	rt = RT.getResultsTable()
	rt.updateResults()


"""
	Get result by column and row
"""
def getResult(col_name,row):
	rt = RT.getResultsTable()
	return rt.getValue(col_name,row)


"""
	set result by column and row
"""
def setResultRow(col_names,results):
	rt = RT.getResultsTable()
	rt.incrementCounter()
	[rt.addValue(col_name,res) for col_name, res in zip(col_names,results)]
	rt.show("Results")

def measure():
	run("Measure")


#Selection Functions
#---------------------

def crop():
	run("Crop")


def saveROI(path,roiname):
	IJ.saveAs("Selection", pjoin(path,roiname))


def rotSelection(degrees):
	run("Rotate...", "angle="+degrees)


"""
	makeEllipse(x,y,w,h)	:	Makes an ellipse selection
	makes a centered ellipse by default
"""
def makeEllipse(x,y,w,h,centered=True):
	if centered:
		x = x - w/2
		y = y - h/2
	IJ.makeOval(x,y,w,h)


"""
	makeRectangle(x,y,w,h)	:	Makes a rectangle selection
"""
def makeRectangle(x,y,w,h):
	IJ.makeRectangle(x,y,w,h)



"""
	makeArrow(x1,y1,x2,y2)	:	Makes an arrow selection
"""
def makeArrow(x1,y1,x2,y2):
	IJ.setTool("arrow")
	imp = IJ.getImage()
	imp.setRoi(Line(x1,y1,x2,y2))


"""
	makeLine(x1,y1,x2,y2)	:	Makes a line selection
"""
def makeLine(x1,y1,x2,y2):
	IJ.makeLine(x1,y1,x2,y2)


"""
	makePoint(x,y)	:	Makes a point selection
"""
def makePoint(x,y):
	IJ.makePoint(x,y)


def selectionType():
	return int(IJ.runMacro("return toString(selectionType());"))

def createSelection():
	run("Create Selection")

def selectNone():
	run("Select None")

def makePolygon(xs,ys):
	imp = IJ.getImage()
	imp.setRoi(PolygonRoi(xs,ys,len(xs),Roi.POLYGON));


#returns [Xs,Ys]
def getSelectionCoordinates():
	c = []
	c.append(IJ.getImage().getRoi().getFloatPolygon().xpoints)
	c.append(IJ.getImage().getRoi().getFloatPolygon().ypoints)
	return c


#returns [Xs,Ys]
def pointsFromMask():
	run("Points from Mask")
	return getSelectionCoordinates()


#ROI Manager Functions
#----------------------
"""
	Clears the ROI Manager
"""
def roiReset():
	if roiCount() > 0:
		roiRun("Deselect")
		roiRun("Delete")


"""
	Updates the currenty selected ROI
"""
def roiUpdate():
	roiRun("Update")


"""
	Returns the slice number of the specified ROI name
	ROI name should be original ImageJ generated name.
"""
def roiSlice(roiname):
	return _RM().getSliceNumber(roiname)


"""
	Returns the name of the ROI with specified index
"""
def roiName(index):
	return _RM().getName(index)


"""
	Sets the new name of the ROI
"""
def roiSetName(name):
	return _RM().runCommand("Rename",name)


"""
	Delete the selected ROI
"""
def roiDelete():
	roiRun("Delete")


"""
	Split the composite ROI in to component ROIs
"""
def roiSplit():
	roiRun("Split")


"""
	Sort ROIs in the ROI Manager
"""
def roiSort():
	roiRun("Sort")


"""
	Execute ROI Manager XOR Function on ROIs
"""
def roiXOR():
	roiRun("XOR")


"""
	Measure over selected ROI
"""
def roiMeasure():
	rm = _RM()
	rm.runCommand("Measure")


"""
	Deselect the selected ROI from the ROI Manager
"""
def roiDeselect():
	rm = _RM()
	rm.runCommand("Deselect")


"""
	Add the ROI to the ROI Manager
"""
def roiAdd():
	rm = _RM()
	rm.runCommand("Add")


"""
	Rename the name of the selected ROI in the ROI Manager
"""
def roiRename(name):
	roiRun("Rename",name)


"""
	Run specified comm with (optional) arg on the ROI Manager
"""
def roiRun(comm,*arg):
	rm = _RM()
	rm.runCommand(comm,*arg)


"""
	Select specified indices in the ROI Manager
	indices is a list of integers
"""
def roiSelectMany(indices):
	rm = _RM()
	rm.setSelectedIndexes(indices)


"""
	Select index ROI in the ROI Manager
"""
def roiSelect(index):
	rm = _RM()
	rm.select(index)


"""
	Return the count of ROis in the ROI Manager
"""
def roiCount():
	rm = _RM()
	return rm.getCount()


def getRM():
	return _RM()


def _RM():
	return RoiManager.getInstance()


#Base Image/Stack Functions
#----------------------

def reset():
	print "calling RESET..."
	roiReset()
	clearResults()


def bin_erode():
	run("Erode")

def bin_open(mode="slice"):
	run("Open", mode)


def setBackgroundColor(r,g,b):
	IJ.setBackgroundColor(r,g,b)


def delSlice():
	run("Delete Slice")


def addSlice():
	run("Add Slice")


#1<=j<=k
#j<=k<=nSlices
def substack(j,k):
	run("Make Substack...", "  slices="+str(j)+"-"+str(k))


def concat(s1,s2):
	run("Concatenate...", "  title="+s1+" image1="+s1+" image2="+s2+" image3=[-- None --]")


"""
	Returns the number of slices in the current image.

	Note: An image has to be open in order for this function to work.
"""
def getNSlices():
	imp = IJ.getImage()
	return imp.getStackSize()

"""
	Returns the number of slices in the current image.

	Note: An image has to be open in order for this function to work.
"""
def getStackSize():
	imp = IJ.getImage()
	return imp.getStackSize()



"""
	Returns the list of statistics as:
	(area, mean, mode, min and max)

	Note: An image has to be open in order for this function to work.
"""
def getStatistics():
	imp = IJ.getImage()
	return imp.getStatistics()


"""
	Returns the list of dimensions as:
	(width, height, nChannels, nSlices, nFrames)

	Note: An image has to be open in order for this function to work.
"""
def getDimensions():
	imp = IJ.getImage()
	return imp.getDimensions()

	
"""
	Returns the pixel value
	Note: An image has to be open in order for this function to work.
"""
def getPixel(x,y):
	imp = IJ.getImage()
	v = imp.getPixel(x,y)
	return v


"""
	Duplicate the entire Image/Stack
"""
def duplicate(name):
	imp = IJ.getImage()
	run("Duplicate...", "title="+name+" duplicate range=1-"+str(imp.getNSlices()));


"""
	Duplicate the entire Image/Stack
"""
def dupFrame(name):
	imp = IJ.getImage()
	run("Duplicate...", "title="+name);


"""
	setForegroundColor(r,g,b)	:	Sets the foreground color
	0 <= r,g,b <= 255
"""
def setForegroundColor(r,g,b):
	IJ.setForegroundColor(r,g,b)


"""
	close()	:	Closes the current image window
"""
def close():
	IJ.runMacro("close()")


"""
	setSlice(index)	:	Sets the current slice in the stack to index
	1 <= index <= stack_size
"""
def setSlice(index):
	IJ.setSlice(index)


"""
	rename(newname)	:	Rename the current image
"""
def rename(newname):
	IJ.runMacro('rename("'+newname+'")')


"""
	selectWindow(name)	:	Select the specified window
"""
def selectWindow(name):
	IJ.runMacro('selectWindow("'+name+'")')


"""
	run(command_string)	:	Execute ImageJ "run" command string
"""
def run(*comm):
	IJ.run(*comm)
