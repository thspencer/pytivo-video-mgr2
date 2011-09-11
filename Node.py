'''
Created on Aug 6, 2011

@author: Jeff
'''
class Node:
	def __init__(self, name, opts, videoList = None, dirList=None):
		self.name = name
		self.opts = opts
		if videoList == None:
			self.videoList = []
		else:
			self.videoList = videoList
			
		if dirList == None:
			self.dirList = []
		else:
			self.dirList = dirList

	def setOpts(self, opts):
		self.opts = opts
		
	def getOpts(self):
		return self.opts
			
	def formatDisplayText(self, fmt):
		return self.name
	
	def getFullTitle(self):
		return self.name
	
	def addVideo(self, node):
		self.videoList.append(node)
		
	def setVideoList(self, vl):
		self.videoList = [n for n in vl]
	
	def getVideoList(self):
		return self.videoList
	
	def addDir(self, node):
		self.dirList.append(node)
		
	def setDirList(self, dl):
		self.dirList = [n for n in dl]	
	
	def getDirList(self):
		return self.dirList
	
	def __len__(self):
		return len(self.videoList) + len(self.dirList)
	
	def getItem(self, x):
		i = x
		if x < len(self.dirList):
			return self.dirList[x]
		
		i = x - len(self.dirList)
		if i < len(self.videoList):
			return self.videoList[i]
		
		return None
	
	def getMeta(self):
		return {}
		
	def __iter__(self):
		self.__index__ = 0
		return self
	
	def next(self):
		v = self.getItem(self.__index__)
		self.__index__ += 1

		if v == None:		
			raise StopIteration
		else:
			return v