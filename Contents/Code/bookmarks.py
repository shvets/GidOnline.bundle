import common

def append_controls(oc, **params):
    bookmark = service.get_bookmark(params['id'])

    if bookmark:
        oc.add(DirectoryObject(
                key=Callback(HandleRemoveBookmark, **params),
                title=unicode(L('Remove Bookmark')),
                thumb=R(REMOVE_ICON)
        ))
    else:
        oc.add(DirectoryObject(
                key=Callback(HandleAddBookmark, **params),
                title=unicode(L('Add Bookmark')),
                thumb=R(ADD_ICON)
        ))

@route(common.PREFIX + '/add_bookmark')
def HandleAddBookmark(**params):
    service.add_bookmark(params['id'])

    return ObjectContainer(header=unicode(L(params['name'])), message=unicode(L('Bookmark Added')))

@route(common.PREFIX + '/remove_bookmark')
def HandleRemoveBookmark(**params):
    service.remove_bookmark(params['id'])

    return ObjectContainer(header=unicode(L(params['name'])), message=unicode(L('Bookmark Removed')))

@route(common.PREFIX + '/bookmarks')
def GetBookmarks():
    oc = ObjectContainer(title2=unicode(L('Bookmarks')))

    # response = service.get_bookmarks()
    #
    # for media in archive.HandleMediaList(response['data']['bookmarks']):
    #     oc.add(media)

    return oc
