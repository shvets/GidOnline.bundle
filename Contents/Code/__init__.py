# -*- coding: utf-8 -*-

PREFIX = '/video/gidonline'

ART = 'art-default.jpg'
ICON = 'icon-default.png'
SEARCH_ICON = 'icon-search.png'

import library_bridge

library_bridge.bridge.export_object('L', L)
library_bridge.bridge.export_object('R', R)
library_bridge.bridge.export_object('Log', Log)
library_bridge.bridge.export_object('Resource', Resource)
library_bridge.bridge.export_object('Datetime', Datetime)
library_bridge.bridge.export_object('Core', Core)
library_bridge.bridge.export_object('Prefs', Prefs)
library_bridge.bridge.export_object('Locale', Locale)
library_bridge.bridge.export_object('Callback', Callback)
library_bridge.bridge.export_object('AudioCodec', AudioCodec)
library_bridge.bridge.export_object('VideoCodec', VideoCodec)
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
library_bridge.bridge.export_object('MessageContainer', MessageContainer)
library_bridge.bridge.export_object('Container', Container)

import plex_util

from gid_online_plex_service import GidOnlinePlexService

service = GidOnlinePlexService()

import main

def Start():
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')
    Plugin.AddViewGroup('MediaPreview', viewMode='MediaPreview', mediaType='items')

    DirectoryObject.art = R(ART)

    VideoClipObject.art = R(ART)

    HTTP.CacheTime = CACHE_1HOUR

    plex_util.validate_prefs()

@handler(PREFIX, 'GidOnline', thumb=ICON, art=ART, allow_sync=True)
def MainMenu():
    oc = ObjectContainer(title1=unicode(L('Title')), art=R(ART))

    oc.http_cookies = HTTP.CookiesForURL(service.URL)

    oc.add(DirectoryObject(key=Callback(main.HandleMovies, title=L("Movies")), title=unicode(L("Movies"))))
    oc.add(DirectoryObject(key=Callback(main.HandleGenres, title=L("Genres")), title=unicode(L("Genres"))))
    oc.add(DirectoryObject(key=Callback(main.HandleSections, title=L("Sections")), title=unicode(L("Sections"))))
    oc.add(DirectoryObject(key=Callback(main.HandleThemes, title=L("Themes")), title=unicode(L("Themes"))))
    oc.add(DirectoryObject(key=Callback(main.HandleHistory), title=unicode(L("History"))))
    oc.add(DirectoryObject(key=Callback(main.HandleQueue), title=unicode(L('Queue'))))

    oc.add(InputDirectoryObject(key=Callback(main.HandleSearch), title=unicode(L("Search")), thumb=R(SEARCH_ICON)))

    return oc
