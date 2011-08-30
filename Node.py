'''
Created on Aug 6, 2011

@author: Jeff
'''
class Node:
	def __init__(self, name, list = None):
		self.name = name
		if list == None:
			self.vlist = []
		else:
			self.vlist = list
		
	def getTitle(self):
		return self.name
	
	def getFullTitle(self):
		return self.name
	
	def addNode(self, node):
		self.vlist.append(node)
	
	def __len__(self):
		return len(self.vlist)
	
	def getItem(self, x):
		if x < len(self.vlist):
			return self.vlist[x]
		
		return None
	
	def getMeta(self):
		return {}
		
	def __iter__(self):
		self.__index__ = 0
		return self
	
	def next(self):
		if self.__index__ < len(self.vlist):
			i = self.__index__
			self.__index__ += 1
			return self.vlist[i]
		
		raise StopIteration