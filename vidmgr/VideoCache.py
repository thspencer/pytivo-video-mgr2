'''
Created on Aug 3, 2011

@author: Jeff
'''
import os
import sys
sys.path.append(os.path.dirname(__file__))

from VideoShare import VideoShare
from DVDShare import DVDShare
from VideoFile import VideoFile
from VideoDir import VideoDir
from Meta import MetaHarvester
from DVDDir import DVDDir
import ConfigParser
import cPickle as pickle
from Node import Node
from Config import ConfigError, SHARETYPE_VIDEO, SHARETYPE_DVD, TYPE_VIDDIR, TYPE_DVDDIR, TYPE_VIDSHARE, TYPE_DVDSHARE, TYPE_NODE

CACHEFILE = "video.cache"
OPTSECT = 'vidmgr'
NESTLIMIT = 10000

class CacheError(Exception):
	pass	

def flatten(node, vfl):
	if node == None:
		return
	
	otype = node.getObjType()
	if otype in [TYPE_VIDDIR, TYPE_DVDDIR, TYPE_NODE]:
		nvl = []
		for v in node.getVideoList():
			i = v.getIndex()
			if i == None:
				i = len(vfl)
				vfl.append(v)
				v.flatten(i)
				
			nvl.append(i)
			
		node.setVideoList(nvl)
		
		for v in node.getDirList():
			flatten(v, vfl)

	elif otype in [TYPE_VIDSHARE, TYPE_DVDSHARE]:
		flatten(node.getVideoDir(), vfl)

	else:
		raise CacheError("Encountered unknown object type while flattening")

def unflatten(node, vfl):
	if node == None:
		return
	
	otype = node.getObjType()
	if otype in [TYPE_VIDDIR, TYPE_DVDDIR, TYPE_NODE]:
		nvl = []
		for v in node.getVideoList():
			if v >= len(vfl):
				raise CacheError("Video index (%d) greater than video array size (%d)" %(v, len(vfl)))
			
			vf = vfl[v]
			vf.unflatten(node)
			nvl.append(vf)
			
		node.setVideoList(nvl)
		
		for v in node.getDirList():
			unflatten(v, vfl)

	elif otype in [TYPE_VIDSHARE, TYPE_DVDSHARE]:
		unflatten(node.getVideoDir(), vfl)

	else:
		raise CacheError("Encountered unknown object type while unflattening")

class VideoList:
	def __init__(self):
		self.list = []

	def addVideo(self, vf):
		self.list.append(vf)
			
	def findVideo(self, fid):
		for v in self.list:
			if v.getFileID() == fid:
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
		self.opts = opts.copy()
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
				self.cache, vfl = pickle.load(f)
				unflatten(self.cache, vfl)
				self.built = False
			except CacheError:
				raise
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
				
				key = "pytivo" + str(i) + ".skip"
				skip = []
				if cfg.has_option(section, key):
					sk = cfg.get(section, key).split(",")
					skip = [s.strip() for s in sk]
					print "skipping shares (", skip, ") from pyTivo number %d" % i
				
				shares.extend(self.loadPyTivoShares(cfgfile, skip))
				
		return shares
					
	def loadPyTivoShares(self, cf, skip):
		shares = []
		pyconfig = ConfigParser.ConfigParser()
		if not pyconfig.read(cf):
			raise ConfigError("ERROR: pyTivo config file " + cf + " does not exist.")

		for section in pyconfig.sections():
			if not section in skip:
				if (pyconfig.has_option(section, "type") and pyconfig.get(section, "type") == "video" and 
					pyconfig.has_option(section, 'path')):
					path = pyconfig.get(section, 'path')
					shares.append([section, path, SHARETYPE_VIDEO])
					
				elif (pyconfig.has_option(section, "type") and pyconfig.get(section, "type") == "dvdvideo" and 
					pyconfig.has_option(section, 'path')):
					path = pyconfig.get(section, 'path')
					shares.append([section, path, SHARETYPE_DVD])
				
		return shares

	def build(self):
		def cmpHarvesters(a, b):
			ta = a.formatDisplayText(None)
			tb = b.formatDisplayText(None)
			return cmp(ta, tb)
		
		title = "Main Menu"
		sharepage = True

		harvesters = []

		if self.cfg.has_option(OPTSECT, 'sharepage'):
			v = self.cfg.get(OPTSECT, 'sharepage')
			if v.lower() == 'false':
				sharepage = False

		if self.cfg.has_option(OPTSECT, 'topsubtitle'):
			title = self.cfg.get(OPTSECT, 'topsubtitle')
			
		for section in self.cfg.sections():
			if section not in [OPTSECT, 'tivos', 'pytivos']:
				lopts = self.opts.copy()
				if self.cfg.has_option(section, 'sort'):
					lopts['sortopt'] = self.cfg.get(section,'sort').split()
				elif self.cfg.has_option(section, 'sortdirection'):
					lval = self.cfg.get(section, 'sortdirection').lower()
					if lval == 'down':
						lopts['sortup'] = False
					elif lval == 'up':
						lopts['sortup'] = True
					else:
						raise ConfigError("Error in buildcache.ini - sortdirection must be up or down")
						
				elif self.cfg.has_option(section, 'display)'):
					lopts['dispopt'] = self.cfg.get(section, 'display').split()
				elif self.cfg.has_option(section, 'displaysep'):
					lopts['dispsep'] = self.cfg.get(section, 'displaysep')

				elif self.cfg.has_option(section, 'groupby'):
					lopts['group'] = self.cfg.get(section, 'groupby')					
				
				if not(self.cfg.has_option(section, 'tags') or self.cfg.has_option(section, 'values')):
					raise ConfigError("Error in ini file.  Section %s needs tags or values option" % section)
					
				elif self.cfg.has_option(section, 'tags'):
					h = MetaHarvester(section, lopts)
					h.setKeySet(self.cfg.get(section,'tags').split())
					harvesters.append(h)
					
				else:  # self.cfg.has_option(section, 'values'):
					if self.cfg.get(section, 'values').lower() == 'all':
						h = MetaHarvester(section, lopts)
						h.setAll()
						harvesters.append(h)
					else:
						terms = self.cfg.get(section, 'values').split('/')
						vdict = {}
						for t in terms:
							v = t.split(':')
							if len(v) != 2:
								raise ConfigError("Error in ini file - syntax on values statement in section %s" % section)

							tag = v[0]
							vals = v[1].split(',')
							vdict[tag] = vals
							
						h = MetaHarvester(section, lopts)
						h.setKeyVal(vdict)
						harvesters.append(h)

		sl = self.loadShares()
		if len(sl) == 0:
			raise ConfigError("Error - no shares are defined")

		root = Node(title, self.opts)

		if sharepage:
			shares = Node("Browse Shares", self.opts)
			for name, path, type in sl:
				if type == SHARETYPE_VIDEO:
					print "Processing video share " + name
					s = VideoShare(self.opts, name, path, self.vidlist, harvesters)
					print "%d Videos found" % s.VideoCount()
				else: # type == SHARETYPE_DVD
					print "Processing DVD share " + name
					s = DVDShare(self.opts, name, path, self.vidlist, harvesters)
					print "%d DVD Videos found" % s.VideoCount()
					
				shares.addDir(s)
			root.addDir(shares)
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

				root.addDir(s)

		for h in sorted(harvesters, cmpHarvesters):
			title = h.formatDisplayText(None)
			nd = h.getNode()
			vc, gc = h.videoCount()
			if gc == None:
				print "%s count: %d videos" % (title, vc)
			else:
				print "%s count: %d videos in %d groups" % (title, vc, gc)
			root.addDir(nd)

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
				vfl = []
				flatten(self.cache, vfl)
				pickle.dump((self.cache, vfl), f)
			except CacheError:
				pass
			except:
				f.close()