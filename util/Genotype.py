'''
Created on 01-Oct-2014

@author: pushkar
'''
from os import listdir
from os.path import isdir
from os.path import join as pjoin
from Track import Track



class Genotype(object):
	'''
	Collection of Tracks pertaining to a genotype.
	'''


	def __init__(self, genotypedatapath):
		'''
		Constructor
		'''
		self.genotypedatapath = genotypedatapath
	
	
	def getTracks(self):
		trackdatapaths = [pjoin(self.genotypedatapath, p) for p in listdir(self.genotypedatapath)]
		trackdatapaths = filter(lambda p: isdir(p), trackdatapaths)
		trackdatapaths = filter(lambda p: (p.count('ignore') + p.count('unusable')) == 0, trackdatapaths)
		trackdatapaths.sort()
		return map(Track, trackdatapaths)







