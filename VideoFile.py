'''
Created on Aug 3, 2011
'''
import os
from Config import DISP_NORMAL, DISP_FILE, DISP_EPTITLE, DISP_EPNUMTITLE, SORT_NORMAL, SORT_FILE, SORT_EPNUM

from DVDDir import DVDDir

class VideoFile:
	def __init__(self, opts, dir, fn):
		self.opts = opts.copy()
		self.filename = fn
		self.title = fn
		self.sorttext = fn
		self.path = dir
		self.vdir = None
		self.meta = {}
		self.metaRef = []

	def setVideoDir(self, dir):
		self.vdir = dir

	def getVideoDir(self):
		return(self.vdir)
	
	def isDeletable(self):
		if self.isDVDVideo():
			return False
		
		return self.opts['deleteallowed']
	
	def isDVDVideo(self):
		return isinstance(self.vdir, DVDDir)
	
	def delVideo(self):
		if self.isDVDVideo():
			return
		
		if self.vdir:
			self.vdir.delVideo(self)
			
		for m in self.metaRef:
			m.delVideo(self)
			
		self.removeFiles()
	
	def getFileName(self):
		return self.filename

	def getPath(self):
		return self.path
	
	def getFullPath(self):
		return os.path.join(self.getPath(), self.getFileName())
	
	def getRelativePath(self):
		return os.path.join(self.vdir.getPath(), self.vdir.getName(), self.getFileName())
	
	def getShare(self):
		if self.vdir == None:
			return None
		
		return self.vdir.getShare();
	
	def setTitle(self, t):
		self.title = t

	def setSortText(self, t):
		self.sorttext = t
		
	def getTitle(self):
		return self.title
	
	def getSortText(self):
		return self.sorttext
	
	def setMeta(self, meta):
		self.meta = meta
		opt = self.opts['dispopt']
		if opt == DISP_FILE:
			self.setTitle(self.getFileName())
		else:
			if 'episodeTitle' in meta:
				if opt == DISP_EPTITLE or opt == DISP_EPNUMTITLE:
					if 'episodeNumber' in meta and opt == DISP_EPNUMTITLE:
						self.setTitle(meta['episodeNumber'] + ':' + meta['episodeTitle'])
					else:
						self.setTitle(meta['episodeTitle'])
				else:
					if 'title' in meta:
						self.setTitle(meta['title'] + ':' + meta['episodeTitle'])
					else:
						self.setTitle(meta['episodeTitle'])
			elif 'title' in meta:
				self.setTitle(meta['title'])
			else:
				self.setTitle(self.getFileName())

		opt = self.opts['sortopt']
		if opt == SORT_FILE:
			self.setSortText(self.getFileName())
		else:
			usedEpisodeNum = False
			if opt == SORT_EPNUM:
				if 'episodeNumber' in meta:
					usedEpisodeNum = True
					if 'title' in meta:
						self.setSortText(meta['title'] + ':' + meta['episodeNumber'])
					else:
						self.setTitle(meta['episodeNumber'])

			if not usedEpisodeNum:
				if 'episodeTitle' in meta:
					if 'title' in meta:
						self.setSortText(meta['title'] + ':' + meta['episodeTitle'])
					else:
						self.setSortText(meta['episodeTitle'])
				elif 'title' in meta:
					self.setSortText(meta['title'])
				else:
					self.setSortText(self.getFileName())
		
	def getMeta(self):
		return self.meta

	def addMetaRef(self, mr):
		self.metaRef.append(mr)
		
	def removeFiles(self):
		path = self.getPath()
		fn = self.getFileName()
		fullname = os.path.join(path, fn)
		
		for f in [ fullname,
				fullname + ".txt",
				os.path.join(path, ".meta", fn + '.txt'),
				fullname + ".jpg",
				os.path.join(path, ".meta", fn + '.jpg') ]:
			try:
				print "Attempting to delete (%s)" % f
				os.remove(f)
			except:
				print "delete failed"
					
