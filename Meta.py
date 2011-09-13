'''
Created on Aug 4, 2011

@author: Jeff
'''

from Node import Node
from Config import ConfigError

HARVEST_KEYSET = 1
HARVEST_KEYVAL = 2

class MetaHarvester:
	def __init__(self, name, opts):
		self.name = name
		self.opts = opts.copy()
		self.root = Node(name, opts)
		self.nodeMap = {}
		self.metakeys = []
		self.metakeydict = {}
		self.type = None
		self.count = 0
		self.gcount = 0
		
	def setKeySet(self, metakeys):
		self.metakeys = [k for k in metakeys]
		self.type = HARVEST_KEYSET
		
	def setKeyVal(self, metakeydict):
		self.metakeydict = metakeydict.copy()
		self.type = HARVEST_KEYVAL
		
	def formatDisplayText(self, fmt):
		return self.name
	
	def harvest(self, vf):
		if self.type == HARVEST_KEYSET:
			self.harvestKEYSET(vf)
		elif self.type == HARVEST_KEYVAL:
			self.harvestKEYVAL(vf)
			
	def harvestKEYVAL(self, vf):
		# get the metadata for the video we are trying to add
		mvf = vf.getMeta()
		
		# now go through our dictionary of matching tags
		for k in self.metakeydict.keys():
			# if a tag is NOT in the video, then do not
			# include that video here
			if not k in mvf:
				return

			# otherwise - get the list og values for that
			# metadata item from our map			
			l = self.metakeydict[k]
			if type(mvf[k]) is list:
				# if the metadata item is a list, then
				# success == the intersection between
				# the two lists is not empty
				match = 0
				for mv in mvf[k]:
					if mv in l:
						match += 1

				if match == 0:
					# no matches here - video does not qualify
					return
			else:
				# otherwise it's not a list - so make
				# sure our matching value is in the
				# metadata
				if not mvf[k] in l:
					return
				
		# we passed all checks - so add this video
		
		# determine grouping
		groupTag = self.opts['group']
		if groupTag == None or groupTag not in mvf:
			# no grouping - stuff into root node
			target = self.root
		else:
			# get the grouping value
			grp = mvf[groupTag]
			if type(grp) is list:
				raise ConfigError("Configuration Error - grouping item must not be a list")

			if grp in self.nodeMap:
				# if we've seen this group, then just reuse the 
				# same node
				target = self.nodeMap[grp]
			else:
				# Otherwise create a new node and link it in
				target = Node(grp, self.opts)
				self.nodeMap[grp] = target
				self.root.addDir(target)
				self.gcount += 1
		
		target.addVideo(vf)
		self.count += 1

	def harvestKEYSET(self, vf):
		# get the metadata for the video
		mvf = vf.getMeta()
		groupTag = self.opts['group']
		
		addlist = []
		
		# now scan through our list of keys
		for mk in self.metakeys:	
			# check if the video even has this key	
			if mk in mvf:
				# it does - get the values and build up our worklist
				if type(mvf[mk]) is list:
					for mv in mvf[mk]:
						if mv not in addlist:
							addlist.append(mv)
				else:
					mv = mvf[mk]
					if mv not in addlist:
						addlist.append(mv)
					
				# now go through the worklist and build the structure as we go
		tally = False
		for mv in addlist:
			if groupTag == None or groupTag not in mvf:
				# no grouping for this share OR video does not have
				# grouping metadata item
				if mv not in self.nodeMap:
					# we've not seen this value yet - create a Node
					# and link it in
					target = Node(mv, self.opts)
					self.nodeMap[mv] = target
					self.root.addDir(target)
				else:
					# otherwise we've seen it so just use it
					target = self.nodeMap[mv]
					
			else:
				# otherwise we are grouping
				grp = mvf[groupTag]
				if type(grp) is list:
					raise ConfigError ("Configuration Error - grouping item must not be a list")

				if grp not in self.nodeMap:
					grpNode = Node(grp, self.opts)
					self.nodeMap[grp] = grpNode
					self.root.addDir(grpNode)
					self.gcount += 1
				else:
					grpNode = self.nodeMap[grp]
					
				mvkey = grp + "/" + mv
				if mvkey not in self.nodeMap:
					target = Node(mvkey, self.opts)
					self.nodeMap[mvkey] = target
					grpNode.addDir(target)
				else:
					target = self.nodeMap[mvkey]
					
			target.addVideo(vf)
			tally = True
			
		if tally:
			self.count += 1

	def getNode(self):
		self.root.sort()
		for n in self.nodeMap.keys():
			self.nodeMap[n].sort()
			
		return self.root
	
	def videoCount(self):
		if self.opts['group'] == None:
			return (self.count, None)
		else:
			return (self.count, self.gcount)
