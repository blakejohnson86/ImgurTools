import urllib, urllib2
import re
import os
import magic
from BeautifulSoup import BeautifulSoup

DownloadLocationBase = os.path.expanduser('~/Desktop/ImgurDump/r/')

Subreddits = {
    'EarthPorn',
    'waterporn',
    'funny'
    }

ImgurSubredditURLBase = 'http://imgur.com/r/'

for Subreddit in Subreddits:
    print "=== Parsing /r/" + Subreddit + " ==="
   
    DownloadLocation = DownloadLocationBase + Subreddit + "/"
    ImgurSubredditURL = ImgurSubredditURLBase + Subreddit
    
    if not os.path.exists(DownloadLocation):
        os.makedirs(DownloadLocation)
    
    ImgurConnection = urllib2.urlopen(ImgurSubredditURL)
    ImgurSubbredditSource = ImgurConnection.read()
    ImgurConnection.close()
    
    PageSource = BeautifulSoup(ImgurSubbredditSource)
    
    for Image in PageSource.findAll('img'):        
        if re.match('^http://i\.imgur\.com/.*b\.(jpg|gif|png)$', Image['src']):
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
    
print "Completed."