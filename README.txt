PyTivo Video Manager - Version 2.0- README.txt

see changelog.txt for a history of changes

what it is
==========

PyTivo video manager (vidmgr) is an HME application that allows you to request that videos in your 
library be "Pushed" to your tivo instead of the normal pull.  Since it's an HME app, this request
can be made from your easy chair with your tivo remote.  Pushing allows videos that are in a
compatible MP4 format to be transferred as is - saving time and space - instead of the transcoding
that a pull will always cause (although a push can also be requested for a video format that requires
transcoding).  vidmgr can also be used to delete videos from your library.

Version 2.0 is a complete rewrite of the application with better, more object-oriented code.  Among the
improvements that will be visible to users:
	1.) The video information is obtained from a cache instead of being read from the disk.  The cache
	    can be built when the program starts up, or ahead of time - at your choice.  The advantage of
	    building the cache ahead of time is that you can get more complex in terms of the way the 
	    cache is built.  The cache supports the ability to search through your videos with any meta data
	    item YOU deem is significant.  As packaged, the cache builds an index based on actors and genre,
	    but if you want to add directors, etc, you can easily do so.  You can even create an index for all
	    videos that have "John Wayne" in them.  It's even possible to build a complex cache at thread start
	    time if you are willing to tolerate a small delay.  My small ARM-based NAS builds my cache containing
	    ~400 videos, including the meta data indexes I mentioned above, in less than 5 seconds.
	    
	2.) You now have the ability to change options on a directory by directory basis.  You want this
	    directory sorted on episode number and that one sorted on show title - no problem.  sorting can now
	    be done based on ANY combinations of strings from the metadata
	    
    3.) the user interface was cleaned up - there is no longer a menu choice for push/delete.  Pushing is
        accomplished by pressing the select button - if you have multiple tivos a dialog box will pop-up
        over the display so you can choose the proper target.  Delete is accomplished by pressing clear.  
        Again, a dialog box will pop-up asking for confirmation.
        
There are many other changes as well, but they are more subtle and/or are not visible to a user.

There is one limitation over the original program - This is for HD only.  If the application finds that
your tivo does not support an HD resolution, it simply exits.  One implication of this - if you plan on 
retaining any of your HD files from the previous version of Vidmgr, then the "HD" needs to be removed
from the file name.

vidmgr is a TiVo HME application designed to operate under wmcbrine's hme for python
framework.  It is NOT a stand-alone application.  Please install the pyhme package (I have tested with version 0.19)
and make sure it is running before you install vidmgr.

Vidmgr is designed to operate in conjunction with the PyTivo transcoding server - If you are not 
using pytivo, then there is no point in installing vidmgr.  I have tested vidmgr with the mcbrine
fork of pytivo.  I am not familiar with the other forks to know whether or not it will run there.

====================================================================================================

installation/setup
==================

First a caveat: I have had difficulties getting this to run under python 2.6 on Linux.  2.5 is just fine.  I'm
not sure what the cause is yet, but until this is determined, I would recommend that you use 2.5.  I have
no empirical data yet for later releases or for versions under windows.

If you've gotten this far, you must want to install this.  It's very simple:

1. Go to the directory where you have pyhme installed.  There should be a lot of subdirectories here,
one per application.  Create a new directory here named "vidmgr"

2. Copy the contents of the vidmgr directory tree from this package into this new directory.  This should
include several .py files and a directory named skins.  Within the skins directory, there will be a
collection of .png files.   

3. Copy config.merge from this package into the pyhme main directory.   

4. Configure - you will need to merge the config.merge file that was delivered with this package with
your config.ini file that you are currently using.  If you have a config.ini from a previous version
of vidmgr, there are impacts to the skin, sort, and display options.  Also, there are several new options as
well as options on where to place additional config files.

There are four areas you need to pay attention to when editing config.ini:  

	a) You may or may not have an "apps" line under the heading [hmeserver].  If you do not, then
the hmeserver will start all apps that it finds.  If you do, then it will only start the named apps.
So if you do have this line and you do want to run vidmgr, add the word "vidmgr" to this line - no quotes
or commas or other punctuation.

	b) you can specify various vidmgr options by putting entries in the [vidmgr] section of the config.ini
as follows:

[vidmgr]
exts=.mpg .mp4 .avi .wmv .m4v

   this names the file extensions you are interested in
      
descsize=20
   this gives the font point size that will be used for the description text.  20 is the default
   
skin=name
   this is the name of the directory under skins that contains all of the png files that are used
   to draw the screen.  default is None.  If you want to create your own skin, create a directory
   under skins, and put whatever png files you are changing there.  Be careful to retain the same
   image size.  The files that you do NOT provide will be obtained from the skins directory, so you
   do not need to duplicate any files you are not changing.
   
deleteallowed=true
   this determines whether or not deletion of videos is permitted.  Default is true, set to false
   if you do not want this capability,  Deletes are never allowed for DVD Video shares
   
sort=value
   determines how listings are sorted.  This is simply a list of metadata tags upon which the sort
   is to be based.  All of the specified fields are concatenated together (with a : in between) in the
   specified order to build the sort key.  If a particular video contains no matching metadata items,
   the sort key defaults to the title metadata item.  If there it no title, the file name is used.
   In addition to any of the metadata tags, including any YOU might create yourself, the following
   special tags are allowed: file - indicates the file name, and titleNumber - indicates the title
   number for DVD titles.  The default value for sort is "title episodeTitle"
  
sortdirection=up
   specifies whether sorts should be ascending (up - the default value) or descending (down)

display=value
   determines what metadata is used for display on the TV.  This is simply a list of metadata tags
   that are contatenated together (with separator in between - see below).  If a video contains no matching items,
   then the title metadata item is used.  If there is no title, then the file name is used.  "file"
   and "titleNumber" and any user-defined tags are available here as they are for the sort value above. 
  
displaysep=string
   string to use as the separator when concatenating metadata items above.  Default is " : "

metafirst = title seriesTitle episodeTitle description
metaignore = isEpisode isEpisodic
   these two items determine which metadata is displayed first in the info screen and which is ignored. 
   Spelling and case are significant - the name must match exactly.  The default values are those
   values given above
metaspace = name name
metaspaceafter = name name
metaspacebefore = name name
   determines that there should be a blank line in the display before or after the indicated metadata items.  The
   default is an empty list so there will be no blank lines.  metaspace and metaspaceafter are synonyms
metamergefiles = False or True (default = True)
metamergelines = False or True (default = False)
   If there are multiple metafiles that correspond to a video file, these two options control how the data is to be merged.
   metamergefiles = False indicates that the files are not to be merged at all - only the more specific file is to be used.
   If metamergefiles if True, the default value, data from the less specific files is over-written/replaced with data from more
   specific files depending on the value for metamergelines.  If metamergelines is False (the default) then a repeating metadata
   key will REPLACE any previous value read.  If it is true, the new data will be concatenated to the old value separated
   by a space.  Note that metamergelines has NO effect on metadata items that start with a 'v' (vActor, etc).  These data
   items will continue to be processed as arrays.
   
   Metadata files are searched for/processed in the following order:
   	1) .meta/default.txt
   	2) default.txt
   	3) .meta/<title>.txt
   	4) <title>.txt
   Where <title> is the base name of the video file - or "folder" for directories.  DVDVideo shares have a few other
   quirks concerning metadata - see below.
   
infolabelpercent=30
   specifies the width, in percentage of the label field on the info screen.  Default is 30, but I have found that 
   20 works well for HD screens
   
inforightmargin=20
   specifies the width, in pixels of pad area on the right side of the info screen.  Default is 20. 0-100 allowed

thumbjustify=left
   specifies how thumbnail images should be justified.  default = left, can be center or right


	c) You need to tell vidmgr about your Tivos.  For each tivo, you need to specify the name and
the TSN.  The format for this is:
[tivos]
tivo1.name=Family Room
tivo1.tsn=TSN1
tivo2.name=Master Bedroom
tivo2.tsn=TSN2

You can have an arbitrary number of Tivos, but as soon as vidmgr detects a gap in the numbering
sequence it will stop parsing.  Make sure the TSN's are accurate as this is how pytivo knows which
tivo to push to.

	d) You need to tell vidmgr about your PyTivo instances.  There are 5 possible pytivo parameters:
		- config is mandatory and is the fully qualified name of the pytivo config file. 
vidmgr reads this file to determine the share names and locations.  
		- You may specify an ip address for the machine on which this instance of pytivo is running.
If you do not specify one, the local IP address is used.
		- If the pytivo config file names a port in the server section, then vidmgr will
use that port number.  Otherwise you need to specify the port number here.
		- if you do not wish to include ALL shares in the vidmgr listing, then specify the share name(s)
that you wish to skip.  If this line is missing, all shares are included
		-Finally, if your hme server is running in a different host environment than this
instance of pytivo, then you need to specify the directory separator character for the pytivo environment.

format for specifying pytivo information:
[pytivos]
pytivo1.config=/usr/local/pytivo/pyTivo.conf
pytivo1.ip=192.168.1.201
pytivo1.skip=share1, share2, ...
pytivo1.port=9032
pytivo1.sep=/

You can have an arbitrary number of pytivos, but as soon as vidmgr detects a gap in the numbering
sequence it will stop parsing.

A note about the separator:  If you are running both vidmgr and pytivo on the same machine, then this
is not required.  However, if (as was happening while I was developing) you are running vidmgr
in a Windows environment (where the directory separator is unfortunately a backslash '\') and 
you are running pytivo in a linux environment (where the separator is a forward slash '/') then
you need to specify "pytivox.sep=/".  Otherwise, vidmgr will happily send its requests to 
pytivo using a backslash in the paths and this will cause pytivo to choke.

You can provide local configuration files to change behavior for a particular directory and its complete
subtree.  In any of your share directories, you can create a file namesd ".vidmgr.ini" and put local changes
into it.  These changes will override the config.ini file in that directory and in all subdirectories
below that point.  You can only do this with a subset of configuration parameters:

	deleteallowed		changes whether delete are allowed in this directory.  For example, I have
						deleteallowed = false everywhere, but I have it set to true in my podcasts 
						directory - otherwise these directories quickly become cluttered
						
	sort				change the metadata tags for constructing sort keys for this directory.  For
						episodic shows you might want to sort on episodeNumber and for
						non-episodic shows, you might want to sort on title
						
	sortdirection		up or down - should sorts be ascending or descending
						
	display				change the metadata tags for constructing the display text.  This allows different
						metadata elements to be used in the display in different shares.  
						
	displaysep			change the separator to use in the formatting of the display strings
	
=======================================================================================================

Usage
=====

Vidmgr presents a directory tree to you.  You can step into and out of directories using the normal
tivo navigation keys.  The root directory of this tree is controlled by how you build your cache - see below.

while browsing this tree, you can also navigate using the number keys.  1 takes you 10% of the
way through the list, 5 = 50%, 7 = 70%, etc.  0 alternately takes you to the end of the list and then to the
beginning of the list

Vidmgr will also show video artwork on the right hand side of the screen.  Vidmgr looks for
the following file:  <full-video-file-name-including-extension>.jpg or, if this doesn't exist, folder.jpg.
The view into which this graphic is placed is 620 pixels wide by 450 pixels high.  If your graphic exceeds
those dimensions it will be scaled while maintaining the aspect ratio.  Folder.jpg will also be the thumbnail
used for the enclosing folder or share.  Also, if there is a folder.txt file in a directory, or in the
subtending .meta directory, its contents - notably the description field will be shown on the display
above the thumbnail.

For dvdvideo shares, vidmgr is totally dependent on accurate metadata.  Metadata (and thumbnails) all belong
in the directory containing the VIDEO_TS directory or in a subtending .meta directory.  Metadata is processed
as follows.  default.txt contains the DVD metadata.  __Txx.mpg.txt contains the metadata for title xx.  The
title-specific metadata is overlaid on top of the DVD metadata according to the metamergefiles and metamergefiles
configuration parameters.  The thumbnail for the DVD is in a file named folder.jpg.  In addition, it is
possible to have a thumbnail for a specific title;  the name should be __Txx.mpg.jpg.  If there is no metadata
for a dvdvideo share, vidmgr assumes that there is only 1 title, and its title is the directory name.

If you press select while on a video file, you will initiate the push operation.  If you only have one tivo, the
file will simply be pushed.  If you have multiple tivos, a pop-up menu will ask you to choose the proper target.

If you are positioned on a video file and press clear, you will have initiated the delete operation.  If deletes
are not allowed or if this is a dvd video, you will simply receive a BONK sound.  Otherwise, you will be asked to
press thumbs-up to confirm and when you do, the file and its associated metadata and artwork will be deleted.  Note
the folder-level metadata or artwork (folder.jpg, default.txt) will NOT be deleted.  If you press ANYTHING other
than thumbs-up, the delete is cancelled.  The following video files cannot be deleted: 1) those for which deleteallowed
is set to false, 2) and video that is part of a DVD since these are virtual files constructed on the fly from the VOB
files, and 3) videos that have multiple file system links since vidmgr cannot follow these links to make sure that
all references are properly updated.

At any time on any list you can press the info button to see a complete list of the metadata.  You can control
which metadata items appear at the front of this display and which are ignored (see configuration above).  On
the info display, you can press left, clear, or info to return to the screen you came from.  If the information
does not fit on one page, you will see paging cues and you can use either up/down or channel up/down to traverse
the pages.

=======================================================================================================

Building The Cache
==================

When the application first receives control, it will attempt to open the cache.  If it does not find it, it will attempt 
to build it dynamically.  Depending on the size of your video library, this could take some time - so you may want to
build it ahead of time.  To build the cache yourself, simply change into the vidmgr directory and run the following
command: "python BuildCache.py".  If thereafter you want to go back to dynamically built caches, delete the file 
"video.cache" from the same directory.

If the cache is built dynamically, it is NEVER written back to disk.  This way, each time you start up, it will be rebuilt.

If the cache if built ahead of time, it will be written back to disk at program exit if it has changed.  Basically this
means if you have deleted a video, since this is the only change possible through the HME interface.  If you build 
your cache ahead of time, you are responsible for keeping it up to date as you add/delete videos.  This is the way
mine is configured, and I rebuild my cache each night through a cron job.

As a convenience, you can also trigger a rebuild of the cache with the remote control by hitting Thumbs-Down three
times in succession.  The app will be non-responsive while the cache is rebuilding.  After it is done, it will
restart at the top of the tree.

There are options you can specify for building the cache.  These are specified in the "buildcache.ini" file in the
vidmgr directory.  Here is an example buildcache.ini file:

[options]
sharepage=False
topsubtitle=Main Menu

[Browse by Genre]
sort = metadata keys for sorting this virtual share
tags = vProgramGenre vSeriesGenre

[Browse by Actor]
sort = metadata keys for sorting this virtual share
display= metadata keys to be displayed for this virtual share
displaysep=-
sortdirection=down
tags = vActor

[Arnie and Duke]
values = vActor:John Wayne, Arnold Schwarzenegger

[Series]
values = isEpisodic:true,True,TRUE
groupby = seriesTitle



The options section contains the following options:
	sharepage = True or False
		This controls whether the top screen of the navigation tree simply contains a "Browse Shares" link (sharepage=true)
		that takes you to a page consisting of all of the shares you have defined, or if each share is a separate item on
		the root page (sharepage=false).  For example, if you have share a and share b, and sharepage=true, the root page
		would be:
				browse shares
				
		if, on the other hand, sharepage was false, the root page would be:
				share a
				share b
				
		There will be other items on the root page too, depending on what types on metadata you are indexing.
				
	topsubtitle="text"
		What text appears as a subtitle on the top-most (root) page.  The default is "Main Menu"
		
		
The remainder of the ini file indicates what entries you want to have on the root screen, and what metadata tag(s) these
should be based on.  In the above example, I will have four additional choices on the root screen.  The first two produce
virtual directory structures based on the Genre and on the Actors.  Under the Genre folder will be a list of all of the Genre
found in the metadata, and under Actor will be found all the actor names found in the metadata:
	Browse by Genre
		is based on the metadata tags 'vProgramGenre' and 'vSeriesGenre'
		
	Browse by Actor
		is based on the metadata tags 'vActor'
		
The third and fourth examples ahow how a virtual share can be built based on whether or not a particular metadata tag contains
one of a set of values.  In the first example, only videos that have either "John Wayne" or "Arnold Schwarzenegger" in the vActor
field.  The last example contains only videos whose isEpisodic value is set to True (or true or TRUE).  You can specify
multiple metadata expressions on the same line, separated by a forward slash (/).  Use NO unnecessary spaces; spaces are
significant (as shown by the actor names above) and if you put spaces around the slashes (or commas) then they will be part
of the matching criteria.  If you have multiple expressions on the same line, the ALL must be satisfied by the matching 
algorithm in order for a video to be included in the virtual share.  The general syntax is:
values=tag:value,value,value/tag:value,value/ ...

A special value "values=all" will include EVERY video.  This allows you to do alternate grouping and/or sorting
		
You can add any number of such entries.  If the tag(s) you specify do not exist for any particular video, that video will
not be part of that index. 

As shown above, you can have a sort, sortdirection, display, or displaysep specification for each of these "virtual shares".
These are optional.  If missing, the corresponding values from config.ini will be used.

You can Also have a groupby option - this is ANY single metadata tag.   The value of that metadata tag for each matching video
will be used to create a virtual folder within the virtual share.  In the example above, under "Series", there will be a 
separate "folder" for each value of seriesTitle - and the videos will appear within this "folder".  Otherwise, ALL of the
matching videos will show up in a single flat folder.  Any video that does not have the "groupby" metadata tag will be 
placed into the root folder of that virtual share.  Groupby is probably more useful for the values= type of virtual share,
but it is also available for tags= shares.
