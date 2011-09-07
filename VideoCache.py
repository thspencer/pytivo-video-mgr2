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
import sys
from Config import SHARETYPE_VIDEO, SHARETYPE_DVD

VMSECTION = "vidmgr"
CACHEFILE = "video.cache"
OPTSECT = 'options'
BUILDINI = 'buildcache.ini'
NESTLIMIT = 10000

class VideoList:
	def __init__(self):
		self.list = []

	def addVideo(self, vf):
		self.list.append(vf)
			
	def findVideo(self, fid):
		for v in self.list:
			if v.getFileID() == fid:
				print "Found %d refs to: %s" % (v.getRefCount()+1, v.getFullPath())
				return v
			
		return None

	def __iter__(self):
		self.__index__ = 0
		return (self)

	def next(self):
		if self.__index__ < len(self.ist):
			i = self.__index__
			self.__index__ += 1
			return self.list[i]

		raise StopIteration

class VideoCache:
	def __init__(self, opts, cfg):
		self.cache = None
		self.built = None
		self.opts = opts
		self.cfg = cfg
		self.vidlist = VideoList()
		p = os.path.dirname(__file__)
		self.filename = os.path.join(p, CACHEFILE)

	def load(self):
		self.cache = None

		try:
			f = open(self.filename)
		except:
			print "Video Cache does not exist - attempting to build..."
			self.build()
			self.built = True
		else:
			try:
				sys.setrecursionlimit(NESTLIMIT)
				self.cache = pickle.load(f)
				self.built = False
			except:
				print "Error loading video cache - trying to build..."
				self.build()
				self.built = True
		
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
					s = VideoShare(self.opts, name, path, self.vidlist, harvesters)
					print "%d Videos found" % s.VideoCount()
				else: # type == SHARETYPE_DVD
					print "Processing DVD share " + name
					s = DVDShare(self.opts, name, path, self.vidlist, harvesters)
					print "%d DVD Videos found" % s.VideoCount()
					
				shares.addNode(s)
			root.addNode(shares)
		else:
			for name, path, type in sl:
				if type == SHARETYPE_VIDEO:
					print "Processing video share " + name
					s = VideoShare(self.opts, name, path, self.vidlist, harvesters)
					print "%d Videos found" % s.VideoCount()
				else: # type == SHARETYPE_DVD
					print "Processing DVD share " + name
					s = DVDShare(self.opts, name, path, self.vidlist, harvesters)
					print "%d DVD Videos found" % s.VideoCount()

				root.addNode(s)

		for h in harvesters:
			print "%s count: %d" % (h.getTitle(), len(h))
			root.addNode(Node(h.getTitle(), h.getMetaLists()))

		self.cache = root

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
				sys.setrecursionlimit(NESTLIMIT)
				pickle.dump(self.cache, f)
			except:
				print "Error saving video cache"
			else:
				f.close()

	def save2(self):
		f = open(self.filename, 'w')
		self.saveNode(self.cache, f)
		f.close();

	def saveNode(self, node, f):
		f.write("Node { name=%s" % node.getTitle)

		for vn in node:
			if isinstance(Node, vn):
				self.saveNode(vn, f)
			elif isinstance(VideoShare, vn):
				self.saveVideoShare(vn, f)
			elif isinstance(DVDShare, vn):
				self.saveDVDShare(vn, f)
			else:
				print "Unknown object in Node object"

		f.write("}")

	def saveVideoShare(self, shr, f):
		f.write("VideoShare{ name=%s title=%s count=%d root=%s"
				% (shr.name, shr.title, shr.count, shr.root))
		self.saveOpts(shr.opts, f)
		vl = shr.getVList()
		self.saveVideoDir(vl[0])
		f.write("}")

	def saveVideoDir(self, vdir, f):
		f.write("VideoDir{ name=%s share=??? path=%s apath=%s title=%s sorttext=%s" % (vdir.name, vdir.path, vdir.apath, vdir.title, vdir.sorttext))
		self.saveOpts(vdir.opts, f)
		self.saveMeta(vdir.meta, f)
		for d in vdir.dirList:
			self.saveVideoDir(d, f)

		for v in vdir.videoList:
			self.saveVideoFile(v, f)
		f.write("}")

	def saveVideoFile(self, vf, f):
		pass

	def saveDVDShare(self, shr, f):
		f.write("DVDShare{ name=%s title=%s count=%d root=%s"
				% (shr.name, shr.title, shr.count, shr.root))
		self.saveOpts(shr.opts, f)
		vl = shr.getVList()
		self.saveDVDDir(vl[0])
		f.write("}")
	
	def saveDVDDir(self, vdir, f):
		f.write("DVDDir{ name=%s share=??? path=%s apath=%s title=%s sorrttxt=%s" % (vdir.name, vdir.path, vdir.apath, vdir.title, vdir.sorttext))
		self.saveOpts(vdir.opts, f)
		self.saveMeta(vdir.meta, f)
		for d in vdir.dirList:
			self.saveVideoDir(d, f)
			self.saveDVDDir(d, f)

		for v in vdir.videoList:
			self.saveVideoFile(v, f)
		f.write("}")

	def saveOpts(self, opts, f):
		pass

	def saveMeta(self, meta, f):
		pass

