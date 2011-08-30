'''
Created on Aug 3, 2011

@author: Jeff
'''
import sys
sys.path.append('..')

from VideoCache import VideoCache
import ConfigParser
import os
import Config

fn = os.path.join("..", "config.ini")

hmeconfig = ConfigParser.ConfigParser()
if not hmeconfig.read(fn):
	print "ERROR: HME config file does not exist."
	exit(1) 

opts = Config.load(hmeconfig)

c = VideoCache(opts, hmeconfig)
c.build()
c.save(True)
