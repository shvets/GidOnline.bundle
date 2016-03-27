# -*- coding: utf-8 -*-

import common
import util
from flow_builder import FlowBuilder
import pagination
import history

builder = FlowBuilder()

CYRILLIC_LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                    'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

@route(common.PREFIX + '/movies')
def HandleMovies(title, path=None, page=1):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    response = service.get_movies(path, page)

    for movie in response['movies']:
        name = movie['name']
        thumb = movie['thumb']

        key = Callback(HandleContainer, path=movie['path'], title=name, name=name, thumb=thumb)

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

        key = Callback(HandleMovie, path=path, title=title, name=title, thumb=thumb)

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
def HandleContainer(path, title, name, thumb):
    document = service.get_movie_document(path)

    data = service.get_session_data(document)

    if data['content_type'] == 'serial':
        oc = ObjectContainer(title2=unicode(title))

        serial_info = service.get_serial_info(document)

        for season in sorted(serial_info['seasons'].keys()):
            season_name = serial_info['seasons'][season]
            key = Callback(HandleEpisodes, path=path,
                           title=unicode(name),
                           name=season_name,
                           thumb=thumb, season=season)

            oc.add(DirectoryObject(key=key, title=unicode(season_name)))

        service.queue.append_queue_controls(oc,
            {
                "path": path,
                "title": title,
                "name": title,
                "thumb": thumb
            },
            add_bookmark_handler=HandleAddBookmark,
            remove_bookmark_handler = HandleRemoveBookmark
        )

        return oc

    else:
        return HandleMovie(path=path, title=title, name=name, thumb=thumb)

@route(common.PREFIX + '/episodes', container=bool)
def HandleEpisodes(path, title, name, thumb, season, container=False):
    document = service.get_movie_document(path, season, 1)
    serial_info = service.get_serial_info(document)

    oc = ObjectContainer(title2=unicode(title + ': ' + name))

    for episode in sorted(serial_info['episodes'].keys()):
        episode_name = serial_info['episodes'][episode]

        key = Callback(HandleMovie, path=path,
                       title=unicode(title + ': ' + name + ': ' + episode_name),
                       name=title + ': ' + name,
                       thumb=thumb,
                       season=season, episode=episode, container=container)

        oc.add(DirectoryObject(key=key, title=unicode(episode_name)))

    service.queue.append_queue_controls(oc,
        {
            "path": path,
            "title": title,
            "name": title + ': ' + name,
            "thumb": thumb,
            "season": season
        },
        add_bookmark_handler=HandleAddBookmark,
        remove_bookmark_handler=HandleRemoveBookmark
    )

    return oc

@route(common.PREFIX + '/movie', container=bool)
def HandleMovie(path, title, name, thumb, season=None, episode=None, container=False, **params):
    oc = ObjectContainer(title2=unicode(name))

    media_info = {
        "path": path,
        "title": title,
        "name": name,
        "thumb": thumb,
        "season": season,
        "episode": episode
    }

    oc.add(GetVideoObject(path=path, title=title, name=name, thumb=thumb, season=season, episode=episode))

    if str(container) == 'False':
        history.push_to_history(media_info)
        service.queue.append_queue_controls(oc, media_info,
            add_bookmark_handler=HandleAddBookmark,
            remove_bookmark_handler = HandleRemoveBookmark
        )

    return oc

def GetVideoObject(path, title, name, thumb, season, episode):
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

    video.key = Callback(HandleMovie, path=path, title=title, name=name, thumb=thumb,
                         season=season, episode=episode, container=True)

    video.items = []

    play_callback = Callback(PlayVideo, url=path, season=season, episode=episode)

    video.items.extend(builder.build_media_objects(play_callback))

    return video

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

        key = Callback(HandleContainer, path=movie['path'], title=name, name=name, thumb=thumb)

        oc.add(DirectoryObject(key=key, title=name, thumb=thumb))

    pagination.append_controls(oc, response, page=page, callback=Search, query=query)

    if len(oc) < 1:
        return util.no_contents('Search')

    return oc

@route(common.PREFIX + '/history')
def HandleHistory(title):
    history = Data.LoadObject(common.KEY_HISTORY)

    oc = ObjectContainer(title2=unicode(title))

    if history:
        for item in sorted(history.values(), key=lambda k: k['time'], reverse=True):
            new_item = item.copy()
            del new_item['time']

            oc.add(DirectoryObject(
                key=Callback(HandleMovie, **new_item),
                title=unicode(item['title']),
                thumb=item['thumb']
            ))

    return oc

@route(common.PREFIX + '/queue')
def HandleQueue(title):
    oc = ObjectContainer(title2=unicode(title))

    for item in service.queue.data:
        if 'episode' in item:
            oc.add(DirectoryObject(
                key=Callback(HandleMovie, **item),
                title=unicode(item['title']),
                thumb=item['thumb']
            ))
        elif 'season' in item:
            oc.add(DirectoryObject(
                key=Callback(HandleEpisodes, **item),
                title=unicode(item['name']),
                thumb=item['thumb']
            ))
        else:
            oc.add(DirectoryObject(
                key=Callback(HandleContainer, **item),
                title=unicode(item['title']),
                thumb=item['thumb']
            ))

    return oc

@route(common.PREFIX + '/add_bookmark')
def HandleAddBookmark(**params):
    service.queue.add_bookmark(params)

    return ObjectContainer(header=unicode(L(params['title'])), message=unicode(L('Bookmark Added')))

@route(common.PREFIX + '/remove_bookmark')
def HandleRemoveBookmark(**params):
    service.queue.remove_bookmark(params)

    return ObjectContainer(header=unicode(L(params['title'])), message=unicode(L('Bookmark Removed')))