from VideoFile import VideoFile
from VideoDir import VideoDir
from DVDDir import DVDDir
from FileID import fileId
import Config
import os
import metadata
import re

regex = re.compile(r'Title\s*(\d+)')

class DVDShare:
	def __init__(self, opts, name, root, vidlist, harvesters):
		self.name = name
		self.title = name
		self.opts = opts.copy()
		self.count = 0
		self.root = root

		self.vlist = VideoDir(self.opts, "", "", root, name)
		
		shareopts = {"": self.opts}
		sharedirs = {"": self.vlist}

		tree = os.walk(root)

		for path, dirs, files in tree:
			rpath = path[len(root):]
			if rpath.startswith(os.path.sep): rpath = rpath[1:]

			if rpath not in sharedirs: continue
			vdir = sharedirs[rpath]
			lopts = shareopts[rpath]
			Config.addLocalOpts(lopts, root, rpath)

			if self.isDvdDir(path):
				p, deftitle = os.path.split(path)
				meta, titles = self.loadDvdMeta(path, lopts, "default", deftitle, False)
				fid = fileId(os.path.join(path, "default.txt"))
				for (title, file, tn) in titles:
					if fid != None:		
						vf = vidlist.findVideo((fid, tn))
					else:
						vf = None
						
					if vf == None:
						vf = VideoFile(lopts, path, file, (fid, tn))
						vidlist.addVideo(vf)

						meta, t = self.loadDvdMeta(path, lopts, file, title, True)
						meta['title'] = title
						vf.setMeta(meta)

						for h in harvesters:
							h.harvest(vf)

					vdir.addVideo(vf)
					self.count += 1
			else:
				for dir in dirs:
					if dir.startswith("."): continue

					cdir = os.path.join(path, dir)
					if self.isDvdDir(cdir):
						meta, tnames = self.loadDvdMeta(cdir,
							lopts,
							"default",
							dir,
							False)
					
						d = DVDDir(lopts, dir, rpath, path, self.name)
					else:
						meta = metadata.from_text(
							os.path.join(path, dir, "folder"),
							lopts['metamergefiles'],
							lopts['metamergelines'])

						d = VideoDir(lopts, dir, rpath, path, self.name)
						
					d.setMeta(meta)
					vdir.addDir(d)
					sharedirs[os.path.join(rpath, dir)] = d
					shareopts[os.path.join(rpath, dir)] = lopts.copy()
			vdir.sort()

	def isDvdDir(self, dir):
		dvddir = os.path.join(dir, "VIDEO_TS")
		return os.path.isdir(dvddir)

	def loadDvdMeta(self, metadir, opts, basefn, deftitle, singleDVDtitle):
		metapath = os.path.join(metadir, basefn)
		meta = metadata.from_text(metapath, opts['metamergefiles'], opts['metamergelines'])
		if (not 'title' in meta) or (meta['title'] == basefn):
			meta['title'] = deftitle

		titles = []
		kl = meta.keys()
		for k in kl:
			x = regex.search(k)
			if x:
				tn = int(x.group(1))
				if meta[k].lower().startswith("ignore"):
					del(meta[k])
				else:
					filename = "__T%02d.mpg" % tn
					titles.append((meta[k], filename, tn))

					if (singleDVDtitle):
						del(meta[k])

		if len(titles) == 0:
			titles.append((meta['title'], "__T00.mpg", 0))
			
		return (meta, titles)

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
