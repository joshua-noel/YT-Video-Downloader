#!/usr/bin/env python

'''
Author: Joshua Noel
License: MIT
Current Build: v0.6
'''

from easysettings import EasySettings
import PySimpleGUI as sg
import pytube
from pytube import YouTube
from pytube import Playlist
import os
import sys
import time

'''
TODO:
-Add error handling for file type
-Make download image a button
'''

#settings file setup
settings = EasySettings("config.conf")

def progress(stream, chunk, bytes_remaining):
    window['-PROGRESS-'].update(100 - round(bytes_remaining / stream.filesize * 100))

def complete(stream, file_path):
    window['-PROGRESS-'].update(0) #resets bar

def downloadVideo(url, fileFormat, qual, downloadDir):
    #exception handling
    try:
        yt = YouTube(str(url), on_progress_callback= progress, on_complete_callback= complete) #creates yt object to manipulate before downloading

    except pytube.exceptions.RegexMatchError:
        sg.popup("Invalid Url Entered", title= "Error")
        return 0

    except pytube.exceptions.VideoUnavailable:
        sg.popup("Video Currently Unavailable", title= "Error")
        return 0

    except pytube.exceptions.ExtractError:
        sg.popup("An Error has Occured", title= "Error")
        return 0

    except pytube.exceptions.HTMLParseError:
        sg.popup("An Error has Occured", title= "Error")
        return 0

    except pytube.exceptions.LiveStreamError(url):
        sg.popup("Video is Livestream", title= "Error")
        return 0

    except pytube.exceptions.MaxRetriesExceeded:
        sg.popup("An Error has Occured", title= "Error")
        return 0

    else:
        window["-CURRENT-"].update(f"Downloading: {url}")

        if fileFormat == "MP4": #downloads mp4 from url
            avaliable = yt.streams.filter(progressive= True).get_by_resolution(str(qual))

            if avaliable == None:
                sg.popup_auto_close("Quality not avaliable, downloading next highest quality", title= "Quality unavailable")
                stream = yt.streams.filter(progressive= True).get_highest_resolution()
                filesize = yt.streams.first().filesize
                title = yt.streams.first().title
                stream.download(downloadDir)

            else:
                title = yt.streams.first().title
                filesize = yt.streams.first().filesize * 100
                avaliable.download(downloadDir)

        elif fileFormat == "MP3": #downloads mp3 from url
            stream = yt.streams.filter(get_audio_only= True).first()
            filesize = yt.streams.first().filesize
            title = yt.streams.first().title
            stream.download(downloadDir)

        else:
            pass

def downloadPlaylist(url, fileFormat, qual, downloadDir):
    p = Playlist(str(url)) #creates p object to manipulate before downloading

    #exception handling
    try:
        p.video_urls[0]

    except KeyError:
        sg.popup("Invalid url entered", title= "Error")
        return 0

    except IndexError:
        sg.popup("Playlist private or empty", title= "Error")
        return 0

    for url in p.video_urls: #loops through all the videos in the playlist and downloads each
        downloadVideo(url, fileFormat, qual, downloadDir)

def main():
    sg.theme("DarkGrey5")
    downloadDir = settings.get("downloadDir")
    url = ""

    mainMenu = [    [sg.Text(f"Download Location: {downloadDir}", key= '-DLLOC-')],
                    [sg.Image("logo.png", key= "-IMAGE-")],
                    [sg.Button("Download Video", key= "-DLVIDEO-"), sg.Button("Download Playlist", key= "-DLPLAYLIST-"), sg.Button("Set Download Location", key= "-SETDIR-"), sg.Button("Quit", key= "-QUIT-")],
                    [sg.Text(f"Downloading: {url}", key= "-CURRENT-")],
                    [sg.Progress(100, orientation='h', size=(20, 20), key='-PROGRESS-', expand_x = True)]]

    downloadVideoMenu = [   [sg.Text("Please enter the url of the video you wish to download")],
                            [sg.InputText("", key= "-URL-")],
                            [sg.Text("File Format: MP4 = Video | MP3 = Audio")],
                            [sg.Combo(["MP4", "MP3"], key= "-FILEFORMAT-")],
                            [sg.Text("Quality (Highest to lowest)")],
                            [sg.Combo(["720p", "480p", "360p", "240p", "144p"], key= "-QUAL-")],
                            [sg.Button("Download", key= "-DL-"), sg.Button("Cancel", key= "-CANCEL-")]]

    downloadPlaylistMenu = [    [sg.Text("Please enter the url of the playlist you wish to download")],
                                [sg.InputText("", key= "-URL-")],
                                [sg.Text("File Format: MP4 = Video | MP3 = Audio")],
                                [sg.Combo(["MP4", "MP3"], key= "-FILEFORMAT-")],
                                [sg.Text("Quality (Highest to lowest)")],
                                [sg.Combo(["720p", "480p", "360p", "240p", "144p"], key= "-QUAL-")],
                                [sg.Button("Download", key= "-DL-"), sg.Button("Cancel", key= "-CANCEL-")]]

    #window management
    global window
    window = sg.Window("Youtube Video Downloader", mainMenu, icon= "icon.ico", element_justification= "c")

    window2 = sg.Window("Download a Video", downloadVideoMenu, element_justification= "c", finalize= True)
    window2.Hide()

    window3 = sg.Window("Download a Playlist", downloadPlaylistMenu, element_justification= "c", finalize= True)
    window3.Hide()

    #main program loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "-QUIT-":
            break

        elif event == "-DLVIDEO-":
            window2.UnHide()

            while True:
                event2, values2 = window2.read()

                if event2 == sg.WIN_CLOSED or event2 == "-CANCEL-":
                    window2.Hide()
                    break

                elif event2 == "-DL-":
                    window2.Hide()

                    if downloadVideo(values2["-URL-"], values2["-FILEFORMAT-"], values2["-QUAL-"], downloadDir) == 0:
                        break

                    else:
                        window["-CURRENT-"].update("Downloading:")
                        sg.popup("Download Complete")
                        break

        elif event == "-DLPLAYLIST-":
            window3.UnHide()

            while True:
                event3, values3 = window3.read()

                if event3 == sg.WIN_CLOSED or event3 == "-CANCEL-":
                    window3.Hide()
                    break

                elif event3 == "-DL-":
                    window3.Hide()

                    if downloadPlaylist(values3["-URL-"], values3["-FILEFORMAT-"], values3["-QUAL-"], downloadDir) == 0:
                        break

                    else:
                        window["-CURRENT-"].update("Downloading:")
                        sg.popup("Download Complete")
                        break

        elif event == "-SETDIR-":
            downloadDir = sg.popup_get_folder(f"Current: {downloadDir}", "Set a new download location")
            settings.setsave("downloadDir", downloadDir)
            window["-DLLOC-"].Update(downloadDir)

    window.close()

if __name__ == "__main__":
    main()
