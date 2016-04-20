# -*- coding: utf-8 -*-

import util
import constants

from plex_service import PlexService

service = PlexService()

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
    oc.add(DirectoryObject(key=Callback(main.HandleHistory), title=L("History")))
    oc.add(DirectoryObject(key=Callback(main.HandleQueue), title=L('Queue')))

    oc.add(InputDirectoryObject(key=Callback(main.HandleSearch), title=L("Search"), thumb=R(constants.SEARCH_ICON)))

    return oc
