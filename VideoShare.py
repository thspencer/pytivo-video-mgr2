'''
Created on Aug 3, 2011

@author: Jeff
'''
from VideoFile import VideoFile
from VideoDir import VideoDir
import Config
import os
import metadata
from FileID import fileId

class VideoShare:
	def __init__(self, opts, name, root, vidlist, harvesters):
		self.name = name
		self.title = name
		self.opts = opts.copy()
		self.count = 0
		self.root = root
		self.vlist = VideoDir(opts, "", "", root, name)
		
		tree = os.walk(root)
		
		sharedirs = {"": self.vlist}
		shareopts = {"": self.opts}

		for path, dirs, files in tree:
			rpath = path[len(root):]
			if rpath.startswith(os.path.sep): rpath = rpath[1:]
			if rpath not in sharedirs: continue
			vl = sharedirs[rpath]
			lopts = shareopts[rpath]
			Config.addLocalOpts(lopts, root, rpath)
			
			for name in dirs:
				if name.startswith("."): continue
				meta = metadata.from_text(os.path.join(path, name, "folder"),
							lopts['metamergefiles'],
							lopts['metamergelines'])
				d = VideoDir(lopts, name, rpath, path, self.name)
				d.setMeta(meta)
				vl.addDir(d)
				sharedirs[os.path.join(rpath, name)] = d
				shareopts[os.path.join(rpath, name)] = lopts.copy()
			
			for name in files:
				if name.startswith("."): continue
				if os.path.splitext(name)[1].lower() in lopts['goodexts']:
					fid = fileId(os.path.join(path, name))
					if fid != None:		
						vf = vidlist.findVideo(fid)
					else:
						vf = None
						
					if vf == None:
						vf = VideoFile(lopts, path, name, fid)
						vidlist.addVideo(vf)

						meta = metadata.from_text(os.path.join(path, name),
												lopts['metamergefiles'],
												lopts['metamergelines'])
						if not 'title' in meta:
							meta = metadata.basic(os.path.join(path, name))
						vf.setMeta(meta)

						for h in harvesters:
							h.harvest(vf)

					vl.addVideo(vf)
					self.count += 1
			vl.sort()
						

	def __iter__(self):
		return self.vlist.__iter__()
	
	def __len__(self):
		return self.vlist.__len__()
	
	def getMeta(self):
		return self.vlist.getMeta()
	
	def getItem(self, x):
		return self.vlist.getItem(x)
	
	def getTitle(self):
		return self.title
	
	def getFullTitle(self):
		return self.title
					
	def getVList(self):
		return self.vlist
	
	def VideoCount(self):
		return self.count

	def __str__(self):
		s = "Name: " + self.name + "\n" + "Root: " + self.root + "\n" + str(self.vlist)
		return s
