'''
Created on Aug 4, 2011

@author: Jeff
'''
class MetaList:
	def __init__(self, name):
		self.name = name
		self.vlist = []
		
	def getTitle(self):
		return "%s (%d)" % (self.name, self.__len__())

	def getFullTitle(self):
		return self.name

	def getName(self):
		return self.name

	def addVideo(self, vf):
		nt = vf.getTitle()
		np = vf.getPath()
		for v in self.vlist:
			if nt == v.getTitle() and np == v.getPath():
				print "Title <%s> is a duplicate for metalist <%s>" % (nt, self.name)
				return
			
		self.vlist.append(vf)
		vf.addMetaRef(self)
		
	def delVideo(self, vf):
		nt = vf.getTitle()
		np = vf.getPath()
		for i in range(len(self.vlist)):
			v = self.vlist[i]
			if nt == v.getTitle() and np == v.getPath():
				del self.vlist[i]
				return

	def sort(self):
		def cmpNodes(a, b):
			ta = a.getSortText()
			tb = b.getSortText()
			return cmp(ta, tb)
		
		s = sorted(self.vlist, cmpNodes)
		self.vlist = s

	def getItem(self, x):
		if x < len(self.vlist):
			return self.vlist[x]
		
		return None
	
	def getVList(self):
		return self.vlist
	
	def __len__(self):
		return len(self.vlist)

	def __iter__(self):
		self.__vindex__ = 0
		return (self)
	
	def getMeta(self):
		return {}

	def next(self):
		if self.__vindex__ < len(self.vlist):
			i = self.__vindex__
			self.__vindex__ += 1
			return self.vlist[i]

		raise StopIteration

class MetaHarvester:
	def __init__(self, name, metakeys):
		self.metakeys = metakeys
		self.name = name
		self.mlist = {}
		self.mkeys = []
		
	def getTitle(self):
		return self.name
	
	def __len__(self):
		return len(self.mkeys)
	
	def getItem(self, x):
		if x < len(self.mkeys):
			return self.mlist[self.mkeys[x]]
		
		return None
	
	def harvest(self, vf):
		m = vf.getMeta();
		for mk in self.metakeys:		
			if mk in m:
				if type(m[mk]) is list:
					for mv in m[mk]:
						if mv not in self.mlist:
							self.mkeys.append(mv)
							self.mlist[mv] = MetaList(mv)
						self.mlist[mv].addVideo(vf)
				else:
					mv = m[mk]
					if mv not in self.mlist:
						self.mkeys.append(mv)
						self.mlist[mv] = MetaList(mv)
					self.mlist[mv].addVideo(vf)

	def getMetaLists(self):
		self.sort()
		l = []
		for mk in self.mkeys:
			l.append(self.mlist[mk])
			
		return l
	
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
