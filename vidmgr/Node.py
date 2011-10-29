'''
Created on Aug 6, 2011

@author: Jeff
'''

from Config import TYPE_NODE

OTHER = "<other>"

class Node:
	def __init__(self, name, opts, title = None, videoList = None, dirList=None):
		self.name = name
		if title == None:
			self.title = name
		else:
			self.title = title
			
		self.opts = opts
		if videoList == None:
			self.videoList = []
		else:
			self.videoList = videoList
			
		if dirList == None:
			self.dirList = []
		else:
			self.dirList = dirList
	
	def getObjType(self):
		return TYPE_NODE

	def setOpts(self, opts):
		self.opts = opts
		
	def getOpts(self):
		return self.opts
			
	def formatDisplayText(self, fmt):
		return "%s (%d)" % (self.name, self.__len__())
	
	def formatSortText(self, fmt):
		return self.name
	
	def getFullTitle(self):
		return self.title
	
	def getName(self):
		return self.name
	
	def addVideo(self, vf):
		vfid = vf.getFileID()
		for v in self.videoList:
			if v.getFileID() == vfid:
				# duplicate file reference - do not add
				return
			
		self.videoList.append(vf)
		
	def delVideo(self, vf):
		vfid = vf.getFileID()
		for i in range(len(self.videoList)):
			v = self.videoList[i]
			if v.getFileID() == vfid:
				del self.videoList[i]
				return
			
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
	
	def getMeta(self):
		return {}
	
	def sort(self):
		def cmpNodes(a, b):
			ta = a.formatSortText(self.opts['sortopt'])
			if ta == OTHER:
				return 1
			tb = b.formatSortText(self.opts['sortopt'])
			if tb == OTHER:
				return -1
			
			if (self.opts['sortup']):
				return cmp(ta, tb)
			else:
				return cmp(tb, ta)

		s = sorted(self.videoList, cmpNodes)
		self.videoList = s
		s = sorted(self.dirList, cmpNodes)
		self.dirList = s

	def __len__(self):
		return len(self.videoList) + len(self.dirList)
	
	def getItem(self, x):
		if x < len(self.dirList):
			return self.dirList[x]
		
		i = x - len(self.dirList)
		if i < len(self.videoList):
			return self.videoList[i]
		
		return None
	
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