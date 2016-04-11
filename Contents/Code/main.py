# -*- coding: utf-8 -*-

import constants
import util
from flow_builder import FlowBuilder
import pagination
import history
import flow_builder

builder = FlowBuilder()

CYRILLIC_LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                    'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

@route(constants.PREFIX + '/sections')
def HandleSections(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    oc.add(DirectoryObject(key=Callback(HandleActors, title=unicode(L("By Actors"))), title=unicode(L("By Actors"))))
    oc.add(DirectoryObject(key=Callback(HandleDirectors, title=unicode(L("By Directors"))), title=unicode(L("By Directors"))))
    oc.add(DirectoryObject(key=Callback(HandleCountries, title=unicode(L("By Countries"))), title=unicode(L("By Countries"))))
    oc.add(DirectoryObject(key=Callback(HandleYears, title=unicode(L("By Years"))), title=unicode(L("By Years"))))

    return oc

@route(constants.PREFIX + '/themes')
def HandleThemes(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    oc.add(DirectoryObject(key=Callback(HandleTopSeven, title=unicode(L("Top Seven"))), title=unicode(L("Top Seven"))))
    oc.add(DirectoryObject(key=Callback(HandleNewMovies, title=unicode(L("New Movies"))), title=unicode(L("New Movies"))))
    oc.add(DirectoryObject(key=Callback(HandlePremiers, title=unicode(L("Premiers"))), title=unicode(L("Premiers"))))

    return oc

@route(constants.PREFIX + '/movies')
def HandleMovies(title, path=None, page=1):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    document = service.fetch_document(service.get_page_url(path, page))

    response = service.get_movies(document, path)

    for movie in response['movies']:
        name = movie['name']
        thumb = movie['thumb']

        key = Callback(HandleContainer, path=movie['path'], title=name, name=name, thumb=thumb)

        oc.add(DirectoryObject(key=key, title=name, thumb=thumb))

    pagination.append_controls(oc, response, page=page, callback=HandleMovies, title=title, path=path)

    return oc

@route(constants.PREFIX + '/genres')
def HandleGenres(title):
    oc = ObjectContainer(title2=unicode(title))

    groups = [
        "Family",
        "Crime",
        "Fiction",
        "Education"
    ]

    for name in groups:
        key = Callback(HandleGenresGroup, title=name)

        oc.add(DirectoryObject(key=key, title=unicode(L(name))))

    return oc

@route(constants.PREFIX + '/genres_group')
def HandleGenresGroup(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    document = service.fetch_document(service.URL)

    for index, genre in enumerate(service.get_genres(document, type=title)):
        path = genre['path']
        name = genre['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

    return oc

@route(constants.PREFIX + '/top_seven')
def HandleTopSeven(title):
    oc = ObjectContainer(title2=unicode(title))

    document = service.fetch_document(service.URL)

    for genre in service.get_top_links(document):
        path = genre['path']
        title = genre['name']
        thumb = genre['thumb']

        key = Callback(HandleMovie, path=path, title=title, name=title, thumb=thumb)

        oc.add(DirectoryObject(key=key, title=title, thumb=thumb))

    return oc

@route(constants.PREFIX + '/new_movies')
def HandleNewMovies(title):
    return HandleMovies(title, path='/new/')

@route(constants.PREFIX + '/premiers')
def HandlePremiers(title):
    return HandleMovies(title, path='/premiers/')

@route(constants.PREFIX + '/actors')
def HandleActors(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    for letter in CYRILLIC_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(
            key=Callback(HandleActorsLetter, title=name, letter=letter),
            title=unicode(letter)
        ))

    return oc

@route(constants.PREFIX + '/actors_letter')
def HandleActorsLetter(title, letter):
    oc = ObjectContainer(title2=unicode(title))

    document = service.fetch_document(service.URL)

    for item in service.get_actors(document=document, letter=letter):
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(constants.PREFIX + '/directors')
def HandleDirectors(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    for letter in CYRILLIC_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(
            key=Callback(HandleDirectorsLetter, title=name, letter=letter),
            title=unicode(letter)
        ))

    return oc

@route(constants.PREFIX + '/directors_letter')
def HandleDirectorsLetter(title, letter):
    oc = ObjectContainer(title2=unicode(title))

    document = service.fetch_document(service.URL)

    for item in service.get_directors(document=document, letter=letter):
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(constants.PREFIX + '/countries')
def HandleCountries(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    document = service.fetch_document(service.URL)

    for item in service.get_countries(document):
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(constants.PREFIX + '/years')
def HandleYears(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    document = service.fetch_document(service.URL)

    for item in service.get_years(document):
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route(constants.PREFIX + '/container')
def HandleContainer(path, title, name, thumb):
    if service.is_serial(path):
        return HandleSeasons(path=path, title=title, name=name, thumb=thumb)
    else:
        return HandleMovie(path=path, title=title, name=name, thumb=thumb)

def HandleSeasons(path, title, name, thumb):
    oc = ObjectContainer(title2=unicode(title))

    document = service.get_movie_document(path)
    serial_info = service.get_serial_info(document)

    for season in sorted(serial_info['seasons'].keys()):
        season_name = serial_info['seasons'][season]
        rating_key = service.get_episode_url(path, season, 0)
        source_title = unicode(L('Title'))

        oc.add(SeasonObject(
            key=Callback(HandleEpisodes, path=path, title=name, name=season_name, thumb=thumb, season=season),
            title=unicode(season_name),
            rating_key=rating_key,
            index=int(season),
            source_title=source_title,
            thumb=thumb,
            # summary=data['summary']
        ))

    media_info = {
        "path": path,
        "title": title,
        "name": title,
        "thumb": thumb
    }

    service.queue.append_queue_controls(oc, media_info,
        add_bookmark_handler=HandleAddBookmark,
        remove_bookmark_handler=HandleRemoveBookmark
    )

    return oc

@route(constants.PREFIX + '/episodes', container=bool)
def HandleEpisodes(path, title, name, thumb, season, container=False):
    oc = ObjectContainer(title2=unicode(title + ': ' + name))

    document = service.get_movie_document(path, season, 1)
    serial_info = service.get_serial_info(document)

    for episode in sorted(serial_info['episodes'].keys()):
        episode_name = serial_info['episodes'][episode]

        key = Callback(HandleMovie, path=path,
                       title=unicode(title + ': ' + name + ': ' + episode_name),
                       name=title + ': ' + name,
                       thumb=thumb,
                       season=season, episode=episode, container=container)

        oc.add(DirectoryObject(key=key, title=unicode(episode_name)))

    media_info = {
        "path": path,
        "title": title,
        "name": title + ': ' + name,
        "thumb": thumb,
        "season": season
    }

    service.queue.append_queue_controls(oc, media_info,
        add_bookmark_handler=HandleAddBookmark,
        remove_bookmark_handler=HandleRemoveBookmark
    )

    return oc

@route(constants.PREFIX + '/movie', container=bool)
def HandleMovie(path, title, name, thumb, season=None, episode=None, container=False, **params):
    urls = service.retrieve_urls(path, season=season, episode=episode)

    if not urls:
        return util.no_contents()
    else:
        media_info = {
            "path": path,
            "title": title,
            "name": name,
            "thumb": thumb,
            "season": season,
            "episode": episode
        }

        oc = ObjectContainer(title2=unicode(name))

        oc.add(MetadataObjectForURL(path=path, title=title, name=name, thumb=thumb,
                                    season=season, episode=episode, urls=urls))

        if str(container) == 'False':
            history.push_to_history(media_info)
            service.queue.append_queue_controls(oc, media_info,
                add_bookmark_handler=HandleAddBookmark,
                remove_bookmark_handler=HandleRemoveBookmark
            )

        return oc

@route(constants.PREFIX + '/search')
def HandleSearch(query=None, page=1):
    oc = ObjectContainer(title2=unicode(L('Search')))

    document = service.fetch_document(service.URL)

    BuildSearchActors(oc, document, query)
    BuildSearchDirectors(oc, document, query)
    BuildSearchCountries(oc, document, query)
    BuildSearchYears(oc, document, query)
    BuildSearchMovies(oc, page, query)

    return oc

def BuildSearchActors(oc, document, query):
    response = service.search_actors(document=document, query=query)

    for item in response:
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

def BuildSearchDirectors(oc, document, query):
    response = service.search_directors(document=document, query=query)

    for item in response:
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

def BuildSearchCountries(oc, document, query):
    response = service.search_countries(document=document, query=query)

    for item in response:
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

def BuildSearchYears(oc, document, query):
    response = service.search_years(document=document, query=query)

    for item in response:
        path = item['path']
        title = item['name']

        key = Callback(HandleMovies, path=path, title=title)

        oc.add(DirectoryObject(key=key, title=title))

def BuildSearchMovies(oc, page, query):
    response = service.search(query=query, page=page)

    for movie in response['movies']:
        name = movie['name']
        thumb = movie['thumb']

        key = Callback(HandleContainer, path=movie['path'], title=name, name=name, thumb=thumb)

        oc.add(DirectoryObject(key=key, title=name, thumb=thumb))

    pagination.append_controls(oc, response, page=page, callback=HandleSearch, query=query)


@route(constants.PREFIX + '/history')
def HandleHistory():
    history_object = history.load_history()

    oc = ObjectContainer(title2=unicode(L('History')))

    if history_object:
        for item in sorted(history_object.values(), key=lambda k: k['time'], reverse=True):
            path = item['path']
            title = item['title']
            thumb = service.get_thumb(item['thumb'])

            oc.add(DirectoryObject(
                key=Callback(HandleContainer, path=path, title=title, name=title, thumb=thumb),
                title=unicode(title),
                thumb=thumb
            ))

    return oc

@route(constants.PREFIX + '/queue')
def HandleQueue():
    oc = ObjectContainer(title2=unicode(L('Queue')))

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

@route(constants.PREFIX + '/add_bookmark')
def HandleAddBookmark(**params):
    service.queue.add_bookmark(params)

    return ObjectContainer(header=unicode(L(params['title'])), message=unicode(L('Bookmark Added')))

@route(constants.PREFIX + '/remove_bookmark')
def HandleRemoveBookmark(**params):
    service.queue.remove_bookmark(params)

    return ObjectContainer(header=unicode(L(params['title'])), message=unicode(L('Bookmark Removed')))

def MetadataObjectForURL(path, title, name, thumb, season, episode, urls):
    params = {}

    document = service.fetch_document(path)
    data = service.get_media_data(document)

    if episode:
        media_type = 'episode'
        params['index'] = int(episode)
        params['season'] = int(season)
        params['content_rating'] = data['rating']
        # show=show,
    else:
        media_type = 'movie'
        params['year'] = data['year']

    video = builder.build_metadata_object(media_type=media_type, **params)

    video.title = title
    video.rating_key = service.get_episode_url(path, season, 0)
    video.rating = data['rating']
    video.thumb = data['thumb']
    video.tags = data['tags']
    video.duration = data['duration'] * 60 * 1000
    video.summary = data['description']

    video.key = Callback(HandleMovie, path=path, title=title, name=name, thumb=thumb,
                         season=season, episode=episode, container=True)

    video.items.extend(MediaObjectsForURL(urls))

    return video

def MediaObjectsForURL(urls):
    items = []

    for item in urls:
        url = item['url']

        play_callback = Callback(PlayVideo, url=url)

        media_object = builder.build_media_object(play_callback, video_resolution=item['width'])

        items.append(media_object)

    return items

@indirect
@route(constants.PREFIX + '/play_video')
def PlayVideo(url):
    if not url:
        return util.no_contents()
    else:
        play_list = Callback(Playlist, url=url)

        return IndirectResponse(MovieObject, key=HTTPLiveStreamURL(play_list))

@route(constants.PREFIX + '/Playlist.m3u8')
def Playlist(url):
    return service.get_play_list(url)
