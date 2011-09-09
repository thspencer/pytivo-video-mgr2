from hme import RSRC_HALIGN_LEFT, RSRC_HALIGN_RIGHT, RSRC_HALIGN_CENTER

import os
import ConfigParser

screenHeight = 720
screenWidth = 1280

titleYPos = 36
subTitleYPos = 84

listViewSize = 14
listViewWidth = 640
listYStart = 121
listHeight = 40 
listXText = 150
listXIcon = 90 
listXCue = 30

detailViewXPos = 640
detailViewWidth = 640
detailDescHeight = 140
detailDescWidth = 590 
detailDescXPos = 10
detailDescYPos = 121

thumbnailxpos = 10
thumbnailypos = 270
thumbcachesize = 100
thumbnailheight = 450
thumbnailwidth = 620

infoHeight = 600
infoWidth = 1160

submenuheight = 166
submenuwidth = 260
submenulineheight = 30

DISP_NORMAL = 0
DISP_FILE = 1
DISP_EPTITLE = 2
DISP_EPNUMTITLE = 3

SORT_NORMAL = 0
SORT_FILE = 1
SORT_EPNUM = 2
SORT_DISPLAY = 3

MYKEY_PUSHRESUME = 0
MYKEY_PUSHCOMPLETE = 1
MYKEY_DELETECONFIRM = 10
MYKEY_DELETECOMPLETE = 11
MYKEY_DELETECANCEL = 12
MYKEY_REBUILDCACHE = 20

SHARETYPE_VIDEO = 0
SHARETYPE_DVD = 1

class ConfigError(Exception):
	pass	

def load(cfg):
	opts = {
			'goodexts' : ['.mp4', '.mpg', '.avi', '.wmv'],
			'metaignore' : ['isEpisode', 'isEpisodic'],
			'metafirst' : ['title', 'seriesTitle', 'episodeTitle', 'description' ],
			'metaspacebefore' : [],
			'metaspaceafter' : [],
			'metamergefiles' : True,
			'metamergelines' : False,
			'infolabelpercent' : 30,
			'inforightmargin' : 20,
			'descsize' : 20,
			'skin' : None,
			'deleteallowed' : True,
			'thumbjustify' : RSRC_HALIGN_LEFT,
			'dispopt' : DISP_NORMAL,
			'sortopt' : SORT_NORMAL
			}

	if cfg.has_section('vidmgr'):
		for opt, value in cfg.items('vidmgr'):
			lval = value.lower()
			# options for metadata on the info screen
			if opt == 'exts':
				opts['goodexts'] = value.split()

			elif opt == 'metaignore':
				opts['metaignore'] = value.split()

			elif opt == 'metafirst':
				opts['metafirst'] = value.split()

			elif opt == 'metaspacebefore':
				opts['metaspacebefore'] = value.split()
			
			elif opt == 'metaspace' or opt == 'metaspaceafter':
				opts['metaspaceafter'] = value.split()

			elif opt == 'metamergefiles':
				if lval == "false":
					opts['metamergefiles'] = False
			
			elif opt == 'metamergelines':
				if lval == "true":
					opts['metamergelines'] = True
			
			elif opt == 'infolabelpercent':
				n = int(value)
				if n < 0 or n > 70:
					raise ConfigError("Config error - infolabelpercent value out of bounds (0-70)")
				else:
					opts['infolabelpercent'] = n

			elif opt == 'inforightmargin':
				n = int(value)
				if n < 0 or n > 100:
					raise ConfigError("Config error - inforightmargin value out of bounds (0-100)")
				else:
					opts['inforightmargin'] = n
			
			elif opt == 'descsize':
				opts['descsize'] = int(value)

			elif opt == 'skin':
				opts['skin'] = value

			elif opt == 'deleteallowed':
				if lval == "false":
					opts['deleteallowed'] = False

			elif opt == 'thumbjustify':
				if lval == 'center':
					opts['thumbjustify'] = RSRC_HALIGN_CENTER
				elif lval == 'right':
					opts['thumbjustify'] = RSRC_HALIGN_RIGHT
				elif lval == 'left':
					opts['thumbjustify'] = RSRC_HALIGN_LEFT
				else:
					raise ConfigError("Config error - invalid value for thumbjustify (left, center, right)")

			elif opt == 'display':
				if (lval == 'episodetitle'):
					opts['dispopt'] = DISP_EPTITLE
				elif (lval == 'episodenumtitle'):
					opts['dispopt'] = DISP_EPNUMTITLE
				elif (lval == 'file'):
					opts['dispopt'] = DISP_FILE
				elif (lval == 'normal'):
					opts['dispopt'] = DISP_NORMAL
				else:
					raise ConfigError("Config error - Invalid display option (episodetitle, episodenumtitle, file, normal)")

			elif opt == 'sort':
				if (lval == 'episodenumber'):
					opts['sortopt'] = SORT_EPNUM
				elif (lval == 'file'):
					opts['sortopt'] = SORT_FILE
				elif (lval == 'normal'):
					opts['sortopt'] = SORT_NORMAL
				elif (lval == 'display'):
					opts['sortopt'] = SORT_DISPLAY
				else:
					raise ConfigError("Config error - Invalid sort option (episodenumber, file, display, normal)")

			else:
				raise ConfigError("Config error - unknown option (%s)" % opt)

	return opts

def addLocalOpts(opts, root, path):
	cfgfn = os.path.join(root, path, ".vidmgr.ini")
	cfg = ConfigParser.ConfigParser()
	if not cfg.read(cfgfn):
		return
	
	if cfg.has_section('vidmgr'):
		for opt, value in cfg.items('vidmgr'):
			lval = value.lower()
			if opt == 'deleteallowed':
				print "Changing delete allowed to %s" % value
				if lval == "false":
					opts['deleteallowed'] = False
				elif lval == "true":
					opts['deleteallowed'] = True
				else:
					print "Invalid value for deleteallowed in %s" % cfgfn

			elif opt == 'display':
				print "Changing display to %s" % value
				if (lval == 'episodetitle'):
					opts['dispopt'] = DISP_EPTITLE
				elif (lval == 'episodenumtitle'):
					opts['dispopt'] = DISP_EPNUMTITLE
				elif (lval == 'file'):
					opts['dispopt'] = DISP_FILE
				elif (lval == 'normal'):
					opts['dispopt'] = DISP_NORMAL
				else:
					print "Invalid value for display in %s" % cfgfn

			elif opt == 'sort':
				print "Changing sort to %s" % value
				if (lval == 'episodenumber'):
					opts['sortopt'] = SORT_EPNUM
				elif (lval == 'file'):
					opts['sortopt'] = SORT_FILE
				elif (lval == 'normal'):
					opts['sortopt'] = SORT_NORMAL
				elif (lval == 'display'):
					opts['sortopt'] = SORT_DISPLAY
				else:
					print "Invalid value for sort in %s" % cfgfn
			else:
				print "Invalid option (%s) in %s" % (opt, cfgfn)

