#!/usr/bin/env python

import urllib, urllib2
import re
import os
from BeautifulSoup import BeautifulSoup

DownloadLocationBase = os.path.expanduser('~/Desktop/ImgurDump/Users/')

Users = {
    'User1',
    'User2'
    }


for User in Users:
    UserURLBase = 'http://' + User + '.imgur.com/'

    #print UserURLBase
    print "=== Parsing " + User + "'s Albums ==="
   
    DownloadLocation = DownloadLocationBase + User + "/"
    
    UserConnection = urllib2.urlopen(UserURLBase)
    UserSource = UserConnection.read()
    UserConnection.close()
    
    UserPageSource = BeautifulSoup(UserSource)
    
    for Album in UserPageSource.findAll('a'):
        if re.match('^//imgur\.com/a/.*$', Album['href']):
            AlbumURL = "http:" + Album['href'] + "/all"
            print "====== Parsing Album: " + AlbumURL + " ======"
            
            AlbumConnection = urllib2.urlopen(AlbumURL)
            AlbumSource = AlbumConnection.read()
            AlbumConnection.close()
            
            AlbumPageSource = BeautifulSoup(AlbumSource)
            
            for Image in AlbumPageSource.findAll('img'):
                try:
                    if re.match('^http://i\.imgur\.com/.*s\.(jpg|gif|png)$', Image['src']):
                        if not os.path.exists(DownloadLocation):
                           os.makedirs(DownloadLocation)
                        
                        ImageURLName, ImageURLExt = os.path.splitext(Image['src'])
                        ImageURLName = ImageURLName[:-1]
            
                        FullImage = ImageURLName + ImageURLExt
            
                        FileDownloadPath = DownloadLocation + os.path.basename(FullImage)
                                    
                        if not os.path.isfile(DownloadLocation + os.path.basename(FullImage)):
                            print "Downloading... \"" + FullImage + "\" to \"" + FileDownloadPath + "\""
                            if urllib.urlretrieve(FullImage, FileDownloadPath):
                                print "[OK]"
                            else:
                                print "[FAIL]"
                except:
                    pass
                    
print "Completed."