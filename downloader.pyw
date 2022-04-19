#!/usr/bin/env python
'''
Author: Joshua Noel
License: MIT
Current Build: v0.3
'''

import easygui as g
import pytube
from pytube import YouTube
from pytube import Playlist
import os
import sys

'''
TODO:
-Add support for higher quality youtube dowloads
-Set persistent download location
'''

def downloadVideo(url, fileFormat, downloadDir):
    #exception handling
    try:
        yt = YouTube(str(url)) #creates yt object to manipulate before downloading

    except pytube.exceptions.RegexMatchError:
        g.msgbox("Invalid url")
        return 0

    except pytube.exceptions.VideoUnavailable:
        g.msgbox("Video currently unavailable")
        return 0

    except pytube.exceptions.ExtractError:
        g.msgbox("An error has occured")
        return 0

    except pytube.exceptions.HTMLParseError:
        g.msgbox("An error has occured, press any key to continue...")
        return 0

    except pytube.exceptions.LiveStreamError(url):
        g.msgbox("Video is livestream")
        return 0

    except pytube.exceptions.MaxRetriesExceeded:
        g.msgbox("An error has occured")
        return 0

    else:
        #downloads either mp3 or mp4 based on user choice
        if fileFormat == "MP4":
            stream = yt.streams.filter(progressive= True).first() #downloads mp4 from url
            stream.download(downloadDir)

        elif fileFormat == "MP3":
            stream = yt.streams.filter(only_audio= True).first() #downloads mp3 from url
            stream.download(downloadDir)

        else:
            pass

def downloadPlaylist(url, fileFormat, downloadDir):
    p = Playlist(str(url)) #creates p object to manipulate before downloading

    for url in p.video_urls: #loops through all the videos in the playlist and downloads each
        downloadVideo(url, fileFormat, downloadDir)

#use below if above does not work
'''
def downloadPlaylist(url, fileFormat, downloadDir):
    p = Playlist(str(url)) #creates p object to manipulate before downloading

    #downloads either mp3 or mp4 based on user choice
    if fileFormat == "MP4":
        for url in p.video_urls: #loops through all the videos in the playlist and downloads each
            #exception handling
            try:
                yt = YouTube(str(url)) #creates yt object to manipulate before downloading

            except pytube.exceptions.VideoUnavailable:
                g.msgbox("Video currently unavailable")

            else:
                stream = yt.streams.filter(progressive= True).first() #downloads mp4 from url
                stream.download(downloadDir)  

    elif fileFormat == "MP3":
        for url in p.video_urls: #loops through all the videos in the playlist and downloads each
            #exception handling
            try:
                yt = YouTube(str(url)) #creates yt object to manipulate before downloading

            except pytube.exceptions.VideoUnavailable:
                g.msgbox("Video currently unavailable")

            else:   
                stream = yt.streams.filter(progressive= True).first() #downloads mp4 from url
                stream.download(downloadDir)

    else:
        pass
'''

def menu(logo, choices, downloadDir): #shortens main menu call
    return g.buttonbox("\t\tDownload Location: {}".format(downloadDir), "Youtube Video Downloader", image= logo, choices= choices) #returns which button is pressed

def main():
    downloadDir = os.path.expanduser("~\Downloads") #sets default download location

    logo = "logo.png"
    choices = ["Download Video", "Download Playlist", "Set Download Location", "Quit"] #choices for main menu buttons

    while True: #main program loop
        option = menu(logo, choices, downloadDir)

        if option is None: #built in exit button
            sys.exit(0)

        elif option == choices[0]: #download video button
            url = g.enterbox("Please enter the url of the video you wish to download")

            if url == None: #cancel button
                pass

            else:
                fileFormat = g.buttonbox("     Please choose the file type of the download MP4 = Video | MP3 = Audio", choices= ["MP4", "MP3"]) #spaces for formating
            
                if downloadVideo(url, fileFormat, downloadDir) == 0: #returns to menu if exception is thrown
                    pass

                else:
                    g.msgbox("Downloaded to {}".format(downloadDir))

        elif option == choices[1]: #download playlist button
            url = g.enterbox("Please enter the url of the playlist you wish to download")

            if url == None: #cancel button
                pass

            else:
                fileFormat = g.buttonbox("     Please choose the file type of the download MP4 = Video | MP3 = Audio", choices= ["MP4", "MP3"]) #spaces for formating
                downloadPlaylist(url, fileFormat, downloadDir)
                g.msgbox("Downloaded to {}".format(downloadDir))      

        elif option == choices[2]: #change download dir button
            downloadDir = g.diropenbox() #opens file explorer where new download location can be choosen

        elif option == choices[3]: #quit button
            sys.exit(0)

if __name__ == "__main__":
    main()