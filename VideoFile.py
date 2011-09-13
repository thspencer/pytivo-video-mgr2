'''
Created on Aug 3, 2011
'''
import os

from DVDDir import DVDDir

class VideoFile:
	def __init__(self, opts, dir, fn, fid):
		self.opts = opts.copy()
		self.filename = fn
		self.title = fn
		self.fileID = fid
		self.path = dir
		self.vRef = []
		self.meta = {}
		self.metaRef = []
		self.index = None
	
	def flatten(self, index):
		self.index = index
		self.vRef = []
		self.metaRef = []

	def unflatten(self, node):
		self.index = None
		self.vRef.append(node)

	def getIndex(self):
		return self.index
	
	def getOpts(self):
		return self.opts

	def addVideoRef(self, dir):
		self.vRef.append(dir)
		
	def getFileID(self):
		return self.fileID

	def getVideoRef(self):
		return(self.vRef)

	def getRefCount(self):
		return len(self.vRef)
	
	def isDeletable(self):
		if self.isDVDVideo():
			return False

		# prevent deletes if more that one link to this file
		if len(self.vRef) > 1:
			return False
		
		return self.opts['deleteallowed']
	
	def isDVDVideo(self):
		for d in self.vRef:
			rc = isinstance(d, DVDDir)
			if rc: return True

		return False
	
	def delVideo(self):
		if not self.isDeletable():
			return
		
		for d in self.vRef:
			d.delVideo(self)
			
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
		if len(self.vRef) == 0:
			return None

		return os.path.join(self.vRef[0].getPath(), self.vRef[0].getName(), self.getFileName())
	
	def getShare(self):
		if len(self.vRef) == 0:
			return None
		
		return self.vRef[0].getShare();
	
	def setMeta(self, meta):
		self.meta = meta
		self.formatDisplayText(self.opts['dispopt'])
		
	def formatDisplayText(self, fmt):
		result = ""

		if fmt != None:
			for f in fmt:
				if f in self.meta:
					if len(result) > 0:
						result += ' ' + self.opts['dispsep'] + ' '
					data = self.meta[f]
					if type(data) is list:
						result += ', '.join(data)
					else:
						result += data

				elif f == 'file':
					if len(result) > 0:
						result += ' ' + self.opts['dispsep'] + ' '
					result += self.getFileName()
			
		if len(result) == 0:
			if 'title' in self.meta:
				result = self.meta['title']
			else:
				result = self.getFileName()
			
		return result


	def formatSortText(self, fmt):
		result = ""
		terms = 0
		for f in fmt:
			if f in self.meta:
				data = self.meta[f]
				if type(data) is list:
					result += ','.join(data)
				else:
					result += data
				terms += 1
			elif f == 'file':
				result = result + self.getFileName()
				terms += 1
				
			result += ":"
			
		if len(result) > 0:
			result = result[:-1]
			
		if terms == 0:
			result = self.getFileName()

		return result
			
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
					
