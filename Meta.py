'''
Created on Aug 4, 2011

@author: Jeff
'''
class MetaList:
	def __init__(self, name, opts):
		self.name = name
		self.videoList = []
		self.dirList = []
		self.opts = opts.copy()
		
	def formatDisplayText(self, fmt):
		return "%s (%d)" % (self.name, self.__len__())

	def getFullTitle(self):
		return self.name

	def getName(self):
		return self.name

	def addVideo(self, vf):
		nid = vf.getFileID()
		if nid != None:
			for v in self.videoList:
				if nid == v.getFileID():
					print "Title <%s> is a duplicate for metalist <%s>" % (vf.formatDisplayText(self.opts['dispopt']), self.name)
					return
			
		self.videoList.append(vf)
		vf.addMetaRef(self)
		
	def delVideo(self, vf):
		nt = vf.formatDisplayText(self.opts['dispopt'])
		np = vf.getPath()
		for i in range(len(self.videoList)):
			v = self.videoList[i]
			if nt == v.formatDisplayText(self.opts['dispopt']) and np == v.getPath():
				del self.videoList[i]
				return
			
	def setVideoList(self, vl):
		self.videoList = [n for n in vl]
	
	def getVideoList(self):
		return self.videoList
	
	def getOpts(self):
		return self.opts
	
	def setDirList(self, dl):
		self.dirList = [n for n in dl]	
	
	def getDirList(self):
		return self.dirList

	def sort(self):
		def cmpNodes(a, b):
			ta = a.formatSortText(self.opts['sortopt'])
			tb = b.formatSortText(self.opts['sortopt'])
			if (self.opts['sortup']):
				return cmp(ta, tb)
			else:
				return cmp(tb, ta)

		s = sorted(self.videoList, cmpNodes)
		self.videoList = s
		s = sorted(self.dirList, cmpNodes)
		self.dirList = s

	def __iter__(self):
		self.__dindex__ = 0
		self.__vindex__ = 0
		return (self)

	def next(self):
		if self.__dindex__ < len(self.dirList):
			i = self.__dindex__
			self.__dindex__ += 1
			return self.dirList[i]

		if self.__vindex__ < len(self.videoList):
			i = self.__vindex__
			self.__vindex__ += 1
			return self.videoList[i]

		raise StopIteration
	
	def getItem(self, x):
		if x < len(self.dirList):
			return self.dirList[x]
		
		lx = x - len(self.dirList)
		if lx < len(self.videoList):
			return self.videoList[lx]
		
		return None
	
	def __len__(self):
		return len(self.dirList) + len(self.videoList)

	def getMeta(self):
		return {}


HARVEST_KEYSET = 1
HARVEST_KEYVAL = 2

class MetaHarvester:
	def __init__(self, name, opts):
		self.name = name
		self.opts = opts.copy()
		
	def setKeySet(self, metakeys):
		self.metakeys = [k for k in metakeys]
		self.type = HARVEST_KEYSET
		self.mlist = {}
		self.mkeys = []
		
	def setKeyVal(self, metakeydict):
		self.metakeydict = metakeydict.copy()
		self.type = HARVEST_KEYVAL
		self.mlist = MetaList(self.name, self.opts)
		
	def formatDisplayText(self, fmt):
		return self.name
	
	def __len__(self):
		if self.type == HARVEST_KEYSET:
			return len(self.mkeys)
		else:
			return len(self.mlist)
	
	def getItem(self, x):
		if x < len(self.mkeys):
			return self.mlist[self.mkeys[x]]
		
		return None
	
	def harvest(self, vf):
		if self.type == HARVEST_KEYSET:
			self.harvestKEYSET(vf)
		elif self.type == HARVEST_KEYVAL:
			self.harvestKEYVAL(vf)
			
	def harvestKEYVAL(self, vf):
		m = vf.getMeta()
		for k in self.metakeydict.keys():
			if not k in m:
				return
			
			l = self.metakeydict[k]
			if type(m[k]) is list:
				match = 0
				for mv in m[k]:
					if mv in l:
						match += 1

				if match == 0:
					return
			else:
				if not m[k] in l:
					return
				
		self.mlist.addVideo(vf)

	def harvestKEYSET(self, vf):
		m = vf.getMeta()
		for mk in self.metakeys:		
			if mk in m:
				if type(m[mk]) is list:
					for mv in m[mk]:
						if mv not in self.mlist:
							self.mkeys.append(mv)
							self.mlist[mv] = MetaList(mv, self.opts)
						self.mlist[mv].addVideo(vf)
				else:
					mv = m[mk]
					if mv not in self.mlist:
						self.mkeys.append(mv)
						self.mlist[mv] = MetaList(mv, self.opts)
					self.mlist[mv].addVideo(vf)

	def getMetaLists(self):
		if self.type == HARVEST_KEYSET:
			return(self.getMetaListsKEYSET())
		elif self.type == HARVEST_KEYVAL:
			return(self.getMetaListsKEYVAL())
			
	def getMetaListsKEYSET(self):
		self.sort()
		l = []
		for mk in self.mkeys:
			l.append(self.mlist[mk])
			
		return l
	
	def getMetaListsKEYVAL(self):
		self.mlist.sort()
		return self.mlist
	
	def sort(self):
		self.mkeys = sorted(self.mlist.keys())
		for mk in self.mkeys:
			self.mlist[mk].sort()

	def __iter__(self):
		self.__mindex__ = 0
		return(self)

	def next(self):
		if self.__mindex__ < len(self.mkeys):
			i = self.__mindex__
			self.__mindex__ += 1
			return self.mlist[self.mkeys[i]]
	
		raise StopIteration
