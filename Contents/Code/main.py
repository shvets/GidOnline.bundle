# -*- coding: utf-8 -*-

import common
import util
import flow_builder
import pagination
import history

CYRILLIC_LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                    'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

@route(common.PREFIX + '/movies')
def HandleMovies(title, path=None, page=1):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    response = service.parse_movies_page(path, page)

    for movie in response['movies']:
        name = movie['name']
        thumb = movie['thumb']

        key = Callback(HandleContainer, path=movie['path'], title=name, thumb=thumb)

        oc.add(DirectoryObject(key=key, title=name, thumb=thumb))

    pagination.append_controls(oc, response, page=page, callback=HandleMovies, title=title, path=path)

    return oc

@route(common.PREFIX + '/top_seven')
def HandleTopSeven(title):
    oc = ObjectContainer(title2=unicode(title))

    for genre in service.get_top_links():
        path = genre['path']
        title = genre['name']
        thumb = genre['thumb']

        Log(path)
        key = Callback(HandleMovie, path=path, title=title, thumb=thumb)

        oc.add(DirectoryObject(key=key, title=title, thumb=thumb))

    return oc

@route(common.PREFIX + '/genres')
def HandleGenres(title):
    oc = ObjectContainer(title2=unicode(title))

    for genre in service.get_genres():
        path = genre['path']
        title = genre['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(common.PREFIX + '/new_movies')
def HandleNewMovies(title):
    return HandleMovies(title, path='/new/')

@route(common.PREFIX + '/premiers')
def HandlePremiers(title):
    return HandleMovies(title, path='/premiers/')

@route(common.PREFIX + '/actors')
def HandleActors(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    for letter in CYRILLIC_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(
            key=Callback(HandleActorsLetter, title=name, letter=letter),
            title=unicode(letter)
        ))

    return oc

@route(common.PREFIX + '/actors_letter')
def HandleActorsLetter(title, letter):
    oc = ObjectContainer(title2=unicode(title))

    for item in service.get_actors(letter):
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(common.PREFIX + '/directors')
def HandleDirectors(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    for letter in CYRILLIC_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(
            key=Callback(HandleDirectorsLetter, title=name, letter=letter),
            title=unicode(letter)
        ))

    return oc

@route(common.PREFIX + '/directors_letter')
def HandleDirectorsLetter(title, letter):
    oc = ObjectContainer(title2=unicode(title))

    for item in service.get_directors(letter):
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(common.PREFIX + '/countries')
def HandleCountries(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    for item in service.get_countries():
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(common.PREFIX + '/years')
def HandleYears(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    for item in service.get_years():
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(common.PREFIX + '/container')
def HandleContainer(path, title, thumb):
    document = service.get_movie_document(path)

    data = service.get_session_data(document)

    if data['content_type'] == 'serial':
        oc = ObjectContainer(title2=unicode(L('Seasons')))

        serial_info = service.get_serial_info(document)

        for season in sorted(serial_info['seasons'].keys()):
            name = serial_info['seasons'][season]
            key = Callback(HandleEpisodes, path=path, title=unicode(name), thumb=thumb, season=season)

            oc.add(DirectoryObject(key=key, title=unicode(name)))

        return oc

    else:
        return HandleMovie(path=path, title=title, thumb=thumb)

@route(common.PREFIX + '/movie', container=bool)
def HandleMovie(path, title, thumb, season=None, episode=None, container=False):
    oc = ObjectContainer(title2=unicode(title))

    media_info = {
        "path": path,
        "title": title,
        "thumb": thumb,
        "season": season,
        "episode": episode
    }

    oc.add(GetVideoObject(path=path, title=title, thumb=thumb, season=season, episode=episode))

    if str(container) == 'False':
        history.push_to_history(media_info)
        append_queue_controls(oc, media_info)

    return oc

def GetVideoObject(path, title, thumb, season, episode):
    video = MovieObject(title=unicode(title))

    data = service.get_media_data(path)

    video.rating_key = 'rating_key'
    video.rating = data['rating']
    video.thumb = data['thumb']
    video.year = data['year']
    video.tags = data['tags']
    video.duration = data['duration'] * 60 * 1000
    video.summary = data['description']
    # video.originally_available_at = originally_available_at(on_air)

    video.key = Callback(HandleMovie, path=path, title=title, thumb=thumb,
                         season=season, episode=episode, container=True)

    video.items = []

    play_callback = Callback(PlayVideo, url=path, season=season, episode=episode)

    video.items.extend(flow_builder.build_media_objects(play_callback))

    return video

@route(common.PREFIX + '/episodes', container=bool)
def HandleEpisodes(path, title, thumb, season, container=False):
    document = service.get_movie_document(path)
    serial_info = service.get_serial_info(document)

    oc = ObjectContainer(title2=unicode(title))

    for episode in sorted(serial_info['episodes'].keys()):
        name = serial_info['episodes'][episode]

        key = Callback(HandleMovie, path=path, title=unicode(name), thumb=thumb,
                       season=season, episode=episode, container=container)

        oc.add(DirectoryObject(key=key, title=unicode(name)))

    return oc

@indirect
@route(common.PREFIX + '/play_video')
def PlayVideo(url, season=None, episode=None):
    url = service.retrieve_url(url, season=season, episode=episode)

    if not url:
        util.no_contents()
    else:
        play_list = Callback(Playlist, url=url)

        return IndirectResponse(MovieObject, key=HTTPLiveStreamURL(play_list))

@route(common.PREFIX + '/Playlist.m3u8')
def Playlist(url):
    return service.get_play_list(url)

@route(common.PREFIX + '/search')
def Search(query=None, page=1):
    oc = ObjectContainer(title2=unicode(L('Search')))

    response = service.search(query=query, page=page)

    for movie in response['movies']:
        name = movie['name']
        thumb = movie['thumb']

        key = Callback(HandleContainer, path=movie['path'], title=name, thumb=thumb)

        oc.add(DirectoryObject(key=key, title=name, thumb=thumb))

    pagination.append_controls(oc, response, page=page, callback=Search, query=query)

    if len(oc) < 1:
        return util.no_contents('Search')

    return oc

@route(common.PREFIX + '/history')
def HandleHistory(title):
    history = Data.LoadObject(common.KEY_HISTORY)

    # if not history or not len(history):
    #     return util.no_contents()

    oc = ObjectContainer(title2=unicode(title))

    if history:
        for item in sorted(history.values(), key=lambda k: k['time'], reverse=True):
            oc.add(DirectoryObject(
                key=Callback(HandleMovie, **item),
                title=unicode(title),
                thumb=item['thumb']
            ))

    return oc

@route(common.PREFIX + '/queue')
def HandleQueue(title):
    oc = ObjectContainer(title2=unicode(title))

    for item in service.queue.data:
        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **item),
            title=unicode(title),
            thumb=item['thumb']
        ))

    return oc

def append_queue_controls(oc, media_info):
    try:
        bookmark = get_bookmark(media_info['path'])

        if bookmark:
            oc.add(DirectoryObject(
                key=Callback(HandleRemoveBookmark, **media_info),
                title=unicode(L('Remove Bookmark')),
                thumb=R(common.REMOVE_ICON)
            ))
        else:
            oc.add(DirectoryObject(
                key=Callback(HandleAddBookmark, **media_info),
                title=unicode(L('Add Bookmark')),
                thumb=R(common.ADD_ICON)
            ))
    except Exception as e:
      Log(e)



@route(common.PREFIX + '/add_bookmark')
def HandleAddBookmark(**params):
    add_bookmark(params)

    return ObjectContainer(header=unicode(L(params['title'])), message=unicode(L('Bookmark Added')))

@route(common.PREFIX + '/remove_bookmark')
def HandleRemoveBookmark(**params):
    remove_bookmark(params)

    return ObjectContainer(header=unicode(L(params['title'])), message=unicode(L('Bookmark Removed')))

def add_bookmark(media_info):
    service.queue.add(media_info)

    service.queue.save()

def remove_bookmark(media_info):
    service.queue.remove(media_info)

    service.queue.save()

def get_bookmark(path):
    Log(service.queue.data)

    found = None

    for item in service.queue.data:
        if 'path' in item:
            if item['path'] == path:
                found = item
                break

    return found