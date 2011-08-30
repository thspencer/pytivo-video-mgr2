from hme import *
from VideoDir import VideoDir
from DVDDir import DVDDir
from VideoFile import VideoFile
import os

from Config import ( detailViewXPos, detailViewWidth, detailDescHeight,
					detailDescWidth, detailDescXPos, detailDescYPos,
					thumbnailwidth, thumbnailheight, thumbnailxpos, thumbnailypos )

class DetailDisplayManager:
	def __init__(self, app, opts, tc):
		self.app = app
		self.opts = opts
		self.tc = tc
		self.imagemap = {}
		
		self.vwDetail = View(self.app, width=detailViewWidth, xpos = detailViewXPos)
		self.vwDetailDescription = View(self.app, height=detailDescHeight, width=detailDescWidth,
									ypos=detailDescYPos, xpos=detailDescXPos, parent=self.vwDetail)
		self.vwDetailThumb = View(self.app, width=thumbnailwidth, height=thumbnailheight, xpos=thumbnailxpos, ypos=thumbnailypos, parent=self.vwDetail)
		
				
	def cleanup(self):
		return
	
	def show(self, item):
		if item == None:
			self.vwDetailDescription.set_text("")
			self.vwDetailThumb.clear_resource()
			return
		
		meta = item.getMeta()
		if 'description' in meta:
			self.vwDetailDescription.set_text(meta['description'], font=self.app.myfonts.descfont,
						colornum=0xffffff,
						flags=RSRC_TEXT_WRAP + RSRC_HALIGN_LEFT + RSRC_VALIGN_TOP)
		else:
			self.vwDetailDescription.set_text("")
			
		if isinstance(item, VideoFile):
			p = item.getPath()
			fn = item.getFileName()
			mapkey = p + ':' + fn
			if mapkey in self.imagemap:
				thumb = self.imagemap[mapkey]
			else:
				thumb = self.getThumb(p, fn, item.isDVDVideo())
				if thumb:
					self.imagemap[mapkey] = thumb
					
			if thumb:
				self.vwDetailThumb.set_resource(thumb, flags=RSRC_VALIGN_TOP+self.opts['thumbjustify'])
			else:
				self.vwDetailThumb.clear_resource()
				
		elif isinstance(item, VideoDir) or isinstance(item, DVDDir):
			mapkey = item.getFullPath()
			if mapkey in self.imagemap:
				thumb = self.imagemap[mapkey]
			else:
				thumb = self.getDirThumb(mapkey, isinstance(item, DVDDir))
				if thumb:
					self.imagemap[mapkey] = thumb
					
			if thumb:
				self.vwDetailThumb.set_resource(thumb, flags=RSRC_VALIGN_TOP+self.opts['thumbjustify'])
			else:
				self.vwDetailThumb.clear_resource()
		else:
			self.vwDetailThumb.clear_resource()

	def getThumb(self, dir, name, isDVD):
		thumb = None
		defName = "folder.jpg"
		if isDVD: defName = "default.jpg"
		for tfn in [ os.path.join(dir, name + '.jpg'),
				os.path.join(dir, '.meta', name + '.jpg'),
				os.path.join(dir, defName),
				os.path.join(dir, '.meta', defName) ]:
			data = self.tc.getImageData(tfn)
			if data:
				thumb = Image(self.app, tfn, data=data)
				break
		return thumb
	
	def getDirThumb(self, dir, isDVD):
		thumb = None
		defName = "folder.jpg"
		if isDVD: defName = "default.jpg"
		for tfn in [ os.path.join(dir, defName),
				os.path.join(dir, '.meta', defName) ]:
			data = self.tc.getImageData(tfn)
			if data:
				thumb = Image(self.app, tfn, data=data)
				break
		return thumb
