# -*- coding: utf-8 -*-

import library_bridge

library_bridge.bridge.export_object('R', R)
library_bridge.bridge.export_object('Log', Log)
library_bridge.bridge.export_object('Datetime', Datetime)
library_bridge.bridge.export_object('Core', Core)
library_bridge.bridge.export_object('Callback', Callback)
library_bridge.bridge.export_object('AudioCodec', AudioCodec)
library_bridge.bridge.export_object('AudioStreamObject', AudioStreamObject)
library_bridge.bridge.export_object('VideoStreamObject', VideoStreamObject)
library_bridge.bridge.export_object('DirectoryObject', DirectoryObject)
library_bridge.bridge.export_object('PartObject', PartObject)
library_bridge.bridge.export_object('MediaObject', MediaObject)
library_bridge.bridge.export_object('EpisodeObject', EpisodeObject)
library_bridge.bridge.export_object('TVShowObject', TVShowObject)
library_bridge.bridge.export_object('MovieObject', MovieObject)
library_bridge.bridge.export_object('TrackObject', TrackObject)
library_bridge.bridge.export_object('VideoClipObject', VideoClipObject)

import util
import constants

from gid_online_plex_service import GidOnlinePlexService

service = GidOnlinePlexService()

import main

def Start():
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')
    Plugin.AddViewGroup('MediaPreview', viewMode='MediaPreview', mediaType='items')

    DirectoryObject.art = R(constants.ART)

    VideoClipObject.art = R(constants.ART)

    HTTP.CacheTime = CACHE_1HOUR

    util.validate_prefs()

@handler(constants.PREFIX, 'GidOnline', thumb=constants.ICON, art=constants.ART, allow_sync=True)
def MainMenu():
    oc = ObjectContainer(title1=unicode(L('Title')), art=R(constants.ART))

    oc.http_cookies = HTTP.CookiesForURL(service.URL)

    oc.add(DirectoryObject(key=Callback(main.HandleMovies, title=L("Movies")), title=unicode(L("Movies"))))
    oc.add(DirectoryObject(key=Callback(main.HandleGenres, title=L("Genres")), title=unicode(L("Genres"))))
    oc.add(DirectoryObject(key=Callback(main.HandleSections, title=L("Sections")), title=unicode(L("Sections"))))
    oc.add(DirectoryObject(key=Callback(main.HandleThemes, title=L("Themes")), title=unicode(L("Themes"))))
    oc.add(DirectoryObject(key=Callback(main.HandleHistory), title=unicode(L("History"))))
    oc.add(DirectoryObject(key=Callback(main.HandleQueue), title=unicode(L('Queue'))))

    oc.add(InputDirectoryObject(key=Callback(main.HandleSearch), title=unicode(L("Search")), thumb=R(constants.SEARCH_ICON)))

    return oc
