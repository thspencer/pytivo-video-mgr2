'''
Created on Aug 3, 2011

@author: Jeff
'''
import sys
sys.path.append('..')

from VideoCache import VideoCache
import Config

cfg = Config.Config()
opts = cfg.load()
cp = cfg.getConfigParser()

c = VideoCache(opts, cp)
c.build()
c.save(True)
