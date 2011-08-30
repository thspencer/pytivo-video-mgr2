'''
Created on Aug 3, 2011

@author: Jeff
'''
from VideoShare import VideoShare
from DVDShare import DVDShare
from VideoFile import VideoFile
from Meta import MetaHarvester
import ConfigParser
import cPickle as pickle
from Node import Node
import os
from Config import SHARETYPE_VIDEO, SHARETYPE_DVD

VMSECTION = "vidmgr"
CACHEFILE = "video.cache"
OPTSECT = 'options'
BUILDINI = 'buildcache.ini'

class VideoCache:
	def __init__(self, opts, cfg):
		self.cache = None
		self.built = False
		self.opts = opts
		self.cfg = cfg
		p = os.path.dirname(__file__)
		self.filename = os.path.join(p, CACHEFILE)

	def load(self):
		self.cache = None

		try:
			f = open(self.filename)
		except:
			print "Video Cache does not exist - attempting to build..."
			self.build()
		else:
			try:
				self.cache = pickle.load(f)
			except:
				print "Error loading video cache - trying to build..."
				self.build()
		
			f.close()
			
		return self.cache

	def loadShares(self):
		shares = []
		section = 'pytivos'
		cfg = self.cfg
		if cfg.has_section(section):
			i = 0
			while (True):
				i = i + 1
				key = "pytivo" + str(i) + ".config"
				if not cfg.has_option(section, key): break
				cfgfile = cfg.get(section, key)
				
				shares.extend(self.loadPyTivoShares(cfgfile))
				
		return shares
					
	def loadPyTivoShares(self, cf):
		shares = []
		pyconfig = ConfigParser.ConfigParser()
		if not pyconfig.read(cf):
			print "ERROR: pyTivo config file " + cf + " does not exist."
			return shares

		for section in pyconfig.sections():
			if (pyconfig.has_option(section, "type") and pyconfig.get(section, "type") == "video" and 
				pyconfig.has_option(section, 'path')):
				path = pyconfig.get(section, 'path')
				shares.append([section, path, SHARETYPE_VIDEO])
				
			if (pyconfig.has_option(section, "type") and pyconfig.get(section, "type") == "dvdvideo" and 
				pyconfig.has_option(section, 'path')):
				path = pyconfig.get(section, 'path')
				shares.append([section, path, SHARETYPE_DVD])
				
		return shares
		
	def build(self):
		p = os.path.dirname(__file__)
		fn = os.path.join(p, BUILDINI)
		bcfg = ConfigParser.ConfigParser()
		
		title = "Main Menu"
		sharepage = True

		harvesters = []

		if bcfg.read(fn):
			for section in bcfg.sections():
				if section != OPTSECT:
					if bcfg.has_option(section, 'tags'):
						harvesters.append(MetaHarvester(section, bcfg.get(section,'tags').split()))

			if bcfg.has_option(OPTSECT, 'sharepage'):
				v = bcfg.get(OPTSECT, 'sharepage')
				if v.lower() == 'false':
					sharepage = False

			if bcfg.has_option(OPTSECT, 'topsubtitle'):
				title = bcfg.get(OPTSECT, 'topsubtitle')


		sl = self.loadShares()
		if len(sl) == 0:
			print "Error - no shares are defined"
			self.cache = None
			return

		root = Node(title)

		if sharepage:
			shares = Node("Browse Shares")
			for name, path, type in sl:
				if type == SHARETYPE_VIDEO:
					print "Processing video share " + name
					s = VideoShare(self.opts, name, path, harvesters)
					print "%d Videos found" % s.VideoCount()
				else: # type == SHARETYPE_DVD
					print "Processing DVD share " + name
					s = DVDShare(self.opts, name, path, harvesters)
					print "%d DVD Videos found" % s.VideoCount()
					
				shares.addNode(s)
			root.addNode(shares)
		else:
			for name, path, type in sl:
				if type == SHARETYPE_VIDEO:
					print "Processing video share " + name
					s = VideoShare(self.opts, name, path, harvesters)
					print "%d Videos found" % s.VideoCount()
				else: # type == SHARETYPE_DVD
					print "Processing DVD share " + name
					s = DVDShare(self.opts, name, path, harvesters)
					print "%d DVD Videos found" % s.VideoCount()

				root.addNode(s)

		for h in harvesters:
			print "%s count: %d" % (h.getTitle(), len(h))
			root.addNode(Node(h.getTitle(), h.getMetaLists()))

		self.cache = root
		self.built = True
		return root

	def save(self, force=False):
		if not force and self.built:
			print "Video cache not being saved because it was built dynamically on entry"
			return

		try:
			f = open(self.filename, 'w')
		except:
			print "Error opening video cache file for write"
		else:
			try:
				pickle.dump(self.cache, f)
			except:
				print "Error saving video cache"
			else:
				f.close()
