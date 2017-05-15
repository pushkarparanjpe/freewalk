'''
Created on 01-Oct-2014

@author: pushkar

The Track object.

'''
from analyze import Analyze

from os import listdir
from os.path import splitext

stackexts = [".tiff", ".tif"]

bsex = {True:"Female", False:"Male"}

LEG = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']

STATE = ('S3', 'S2', 'S1', 'S0',)

BodyFuncs = ['getWalkingSpeed']

ConcurrFuncs = ['getConcurrency']

class Track(object):
	'''
	classdocs
	'''

	def __init__(self, trackdatapath):
		'''
		Constructor
		'''
		self.ana = Analyze(trackdatapath)
		self.trackdatapath = trackdatapath
		self.sex = bsex[self._isFemale(self.trackdatapath)]


	def __str__(self, *args, **kwargs):
		return 'TRACK ~|%s|~' % self.trackdatapath


	def _isFemale(self, p):
		children = listdir(p)
		# is a TIFF file
		children = filter(lambda c: stackexts.count(splitext(c)[1].lower()) > 0 , children)
		print(children)
		# is a female stack
		children = filter(lambda c: splitext(c)[0].lower().count('f') > 0 , children)
		return bool(len(children))


	def getWhatever(self, paramfuncname):
		if paramfuncname in BodyFuncs:
			return [getattr(self.ana, paramfuncname)(None)]
		elif paramfuncname in ConcurrFuncs:
			return [getattr(self.ana, paramfuncname)(state) for state in STATE]
		return [getattr(self.ana, paramfuncname)(leg) for leg in LEG]







