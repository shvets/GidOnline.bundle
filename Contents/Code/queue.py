@route('/video/etvnet/add_items_to_queue')
def HandleAddItemsToQueue(id, name, thumb):
    media_info = MediaInfo(type='Container', id=id, name=name, thumb=thumb)

    service.queue.add(media_info)
    service.queue.save()

    return ObjectContainer(
        header=u'%s' % L(name),
        message=u'%s' % L('Container Added')
    )

@route('/video/etvnet/reomve_items_from_queue')
def HandleRemoveItemsFromQueue(id, name, thumb):
    media_info = MediaInfo(type='Container', id=id, name=name, thumb=thumb)

    service.queue.remove(media_info)
    service.queue.save()

    return ObjectContainer(
        header=u'%s' % L(name),
        message=u'%s' % L('Container Removed')
    )

@route('/video/etvnet/add_item_to_queue')
def HandleAddItemToQueue(id, name, thumb, rating_key, description, duration, year, on_air, files):
    media_info = MediaInfo(type='MediaObject', id=id, name=name, thumb=thumb, rating_key=rating_key,
                           description=description, duration=duration, year=year, on_air=on_air, files=files)

    service.queue.add(media_info)
    service.queue.save()

    return ObjectContainer(
        header=u'%s' % L(name),
        message=u'%s' % L('Media Added')
    )

@route('/video/etvnet/remove_item_from_queue')
def HandleRemoveItemFromQueue(id, name, thumb, rating_key, description, duration, year, on_air, files):
    media_info = MediaInfo(type='MediaObject', id=id, name=name, thumb=thumb, rating_key=rating_key,
                           description=description, duration=duration, year=year, on_air=on_air, files=files)

    service.queue.remove(media_info)
    service.queue.save()

    return ObjectContainer(
        header=u'%s' % L(name),
        message=u'%s' % L('Media Removed')
    )

@route('/video/etvnet/queue')
def GetQueue(title):
    oc = ObjectContainer(title2=title)

    # for media in archive.HandleMediaList(service.queue.data, in_queue=True):
    #     oc.add(media)

    return oc

def addItemsQueueControls(oc, id, name, thumb):
    if item_already_added_to_storage(id):
        select_key = Callback(HandleRemoveItemsFromQueue, id=id, name=name, thumb=thumb)

        oc.add(DirectoryObject(key=select_key, title=unicode(L('Remove from Queue')), thumb=R(REMOVE_ICON)))
    else:
        select_key = Callback(HandleAddItemsToQueue, id=id, name=name, thumb=thumb)

        oc.add(DirectoryObject(key=select_key, title=unicode(L('Add to Queue')), thumb=R(ADD_ICON)))

def addItemQueueControls(oc, id, name, thumb, rating_key, description, duration, year, on_air, files):
    if item_already_added_to_storage(id):
        select_key = Callback(HandleRemoveItemFromQueue, id=id, name=name, thumb=thumb, rating_key=rating_key,
            description=description, duration=duration, year=year, on_air=on_air, files=files)

        oc.add(DirectoryObject(key=select_key, title=unicode(L('Remove from Queue')), thumb=R(REMOVE_ICON)))
    else:
        select_key = Callback(HandleAddItemToQueue, id=id, name=name, thumb=thumb, rating_key=rating_key,
            description=description, duration=duration, year=year, on_air=on_air, files=files)

        oc.add(DirectoryObject(key=select_key, title=unicode(L('Add to Queue')), thumb=R(ADD_ICON)))

def item_already_added_to_storage(id):
    added = False

    for media in service.queue.data:
        if id == media['id']:
            added = True
            break

    return added