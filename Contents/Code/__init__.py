# -*- coding: utf-8 -*-

import util
import common

from plex_service import PlexService

service = PlexService()

import main

def Start():
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')
    Plugin.AddViewGroup('MediaPreview', viewMode='MediaPreview', mediaType='items')

    DirectoryObject.art = R(common.ART)

    VideoClipObject.art = R(common.ART)

    HTTP.CacheTime = CACHE_1HOUR

    util.validate_prefs()

@handler(common.PREFIX, 'GidOnline', thumb=common.ICON, art=common.ART, allow_sync=True)
def MainMenu():
    oc = ObjectContainer(title1=unicode(L('Title')), art=R(common.ART))

    oc.http_cookies = HTTP.CookiesForURL(service.URL)

    oc.add(DirectoryObject(key=Callback(main.HandleMovies, title=unicode(L("Movies"))), title=unicode(L("Movies"))))
    oc.add(DirectoryObject(key=Callback(main.HandleGenres, title=unicode(L("Genres"))), title=unicode(L("Genres"))))
    oc.add(DirectoryObject(key=Callback(main.HandleActors, title=unicode(L("Actors"))), title=unicode(L("Actors"))))
    oc.add(DirectoryObject(key=Callback(main.HandleDirectors, title=unicode(L("Directors"))), title=unicode(L("Directors"))))
    oc.add(DirectoryObject(key=Callback(main.HandleCountries, title=unicode(L("Countries"))), title=unicode(L("Countries"))))
    oc.add(DirectoryObject(key=Callback(main.HandleYears, title=unicode(L("Years"))), title=unicode(L("Years"))))
    oc.add(DirectoryObject(key=Callback(main.HandleTopSeven, title=unicode(L("Top Seven"))), title=unicode(L("Top Seven"))))
    oc.add(DirectoryObject(key=Callback(main.HandleNewMovies, title=unicode(L("New Movies"))), title=unicode(L("New Movies"))))
    oc.add(DirectoryObject(key=Callback(main.HandlePremiers, title=unicode(L("Premiers"))), title=unicode(L("Premiers"))))
    oc.add(DirectoryObject(key=Callback(main.HandleQueue, title=unicode(L('Queue'))), title=unicode(L('Queue'))))
    oc.add(DirectoryObject(key=Callback(main.HandleHistory, title=unicode(L("History"))), title=unicode(L("History"))))
    oc.add(InputDirectoryObject(key=Callback(main.HandleSearch), title=unicode(L("Search")), thumb=R(common.SEARCH_ICON)))

    return oc
