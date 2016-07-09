# -*- coding: utf-8 -*-

from media_info import MediaInfo
import plex_util
from flow_builder import FlowBuilder
import pagination
import history

@route(PREFIX + '/sections')
def HandleSections(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    oc.add(DirectoryObject(key=Callback(HandleActors, title=unicode(L("By Actors"))), title=unicode(L("By Actors"))))
    oc.add(DirectoryObject(key=Callback(HandleDirectors, title=unicode(L("By Directors"))), title=unicode(L("By Directors"))))
    oc.add(DirectoryObject(key=Callback(HandleCountries, title=unicode(L("By Countries"))), title=unicode(L("By Countries"))))
    oc.add(DirectoryObject(key=Callback(HandleYears, title=unicode(L("By Years"))), title=unicode(L("By Years"))))

    return oc

@route(PREFIX + '/themes')
def HandleThemes(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    oc.add(DirectoryObject(key=Callback(HandleTopSeven, title=L("Top Seven")), title=unicode(L("Top Seven"))))
    oc.add(DirectoryObject(key=Callback(HandleNewMovies, title=L("New Movies")), title=unicode(L("New Movies"))))
    oc.add(DirectoryObject(key=Callback(HandlePremiers, title=L("Premiers")), title=unicode(L("Premiers"))))

    return oc

@route(PREFIX + '/movies')
def HandleMovies(title, path=None, page=1):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    document = service.fetch_document(service.get_page_url(path, page))

    response = service.get_movies(document, path)

    for movie in response['items']:
        name = movie['name']
        thumb = movie['thumb']

        new_params = {
            'id': movie['path'],
            'title': name,
            'name': name,
            'thumb': thumb
        }

        key = Callback(HandleMovieOrSerie, **new_params)

        oc.add(DirectoryObject(key=key, title=name, thumb=thumb))

    pagination.append_controls(oc, response, page=page, callback=HandleMovies, title=title, path=path)

    return oc

@route(PREFIX + '/genres')
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

@route(PREFIX + '/genres_group')
def HandleGenresGroup(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    document = service.fetch_document(service.URL)

    for index, genre in enumerate(service.get_genres(document, type=title)):
        path = genre['path']
        name = genre['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

    return oc

@route(PREFIX + '/top_seven')
def HandleTopSeven(title):
    oc = ObjectContainer(title2=unicode(title))

    document = service.fetch_document(service.URL)

    for genre in service.get_top_links(document):
        path = genre['path']
        name = genre['name']
        thumb = genre['thumb']

        new_params = {
            'type': 'movie',
            'id': path,
            'title': name,
            'name': name,
            'thumb': thumb
        }
        key = Callback(HandleMovie, **new_params)

        oc.add(DirectoryObject(key=key, title=name, thumb=thumb))

    return oc

@route(PREFIX + '/new_movies')
def HandleNewMovies(title):
    return HandleMovies(title, path='/new/')

@route(PREFIX + '/premiers')
def HandlePremiers(title):
    return HandleMovies(title, path='/premiers/')

@route(PREFIX + '/actors')
def HandleActors(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    for letter in service.CYRILLIC_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(
            key=Callback(HandleActorsLetter, title=name, letter=letter),
            title=unicode(letter)
        ))

    return oc

@route(PREFIX + '/actors_letter')
def HandleActorsLetter(title, letter):
    oc = ObjectContainer(title2=unicode(title))

    document = service.fetch_document(service.URL)

    for item in service.get_actors(document=document, letter=letter):
        path = item['path']
        name = item['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

    return oc

@route(PREFIX + '/directors')
def HandleDirectors(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    for letter in service.CYRILLIC_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(
            key=Callback(HandleDirectorsLetter, title=name, letter=letter),
            title=unicode(letter)
        ))

    return oc

@route(PREFIX + '/directors_letter')
def HandleDirectorsLetter(title, letter):
    oc = ObjectContainer(title2=unicode(title))

    document = service.fetch_document(service.URL)

    for item in service.get_directors(document=document, letter=letter):
        path = item['path']
        name = item['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

    return oc

@route(PREFIX + '/countries')
def HandleCountries(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    document = service.fetch_document(service.URL)

    for item in service.get_countries(document):
        path = item['path']
        name = item['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

    return oc

@route(PREFIX + '/years')
def HandleYears(title):
    oc = ObjectContainer(title2=unicode(title), view_group='List')

    document = service.fetch_document(service.URL)

    for item in service.get_years(document):
        path = item['path']
        name = item['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

    return oc

@route(PREFIX + '/movie_or_serie')
def HandleMovieOrSerie(**params):
    if service.is_serial(params['id']):
        params['type'] = 'serie'
        return HandleSerie(**params)
    else:
        params['type'] = 'movie'
        return HandleMovie(**params)

@route(PREFIX + '/serie')
def HandleSerie(operation=None, **params):
    oc = ObjectContainer(title2=unicode(params['title']))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    document = service.get_movie_document(params['id'])
    serial_info = service.get_serial_info(document)

    for season in sorted(serial_info['seasons'].keys()):
        season_name = serial_info['seasons'][season]
        rating_key = service.get_episode_url(params['id'], season, 0)
        source_title = unicode(L('Title'))

        new_params = {
            'type': 'season',
            'id': params['id'],
            'serieName': params['name'],
            'name': season_name,
            'thumb': params['thumb'],
            'season': season
        }
        oc.add(SeasonObject(
            key=Callback(HandleSeason, **new_params),
            title=unicode(season_name),
            rating_key=rating_key,
            index=int(season),
            source_title=source_title,
            thumb=params['thumb']
            # summary=data['summary']
        ))

    service.queue.append_bookmark_controls(oc, HandleSerie, media_info)

    return oc

@route(PREFIX + '/season', container=bool)
def HandleSeason(operation=None, container=False, **params):
    oc = ObjectContainer(title2=unicode(params['serieName'] + ': ' + params['name']))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    document = service.get_movie_document(params['id'], params['season'], 1)
    serial_info = service.get_serial_info(document)

    for index, episode in enumerate(sorted(serial_info['episodes'].keys())):
        episode_name = serial_info['episodes'][episode]

        new_params = {
            'type': 'episode',
            'id': params['id'],
            'serieName': params['serieName'],
            'name': episode_name,
            'thumb': params['thumb'],
            'season': params['season'],
            'episode': episode,
            'episodeNumber': index + 1
        }

        key = Callback(HandleMovie, container=container, **new_params)

        oc.add(DirectoryObject(key=key, title=unicode(episode_name)))

    service.queue.append_bookmark_controls(oc, HandleSeason, media_info)

    return oc

@route(PREFIX + '/movie', container=bool)
def HandleMovie(operation=None, container=False, **params):
    if 'season' in params:
        season = params['season']
    else:
        season = None

    if 'episode' in params:
        episode = params['episode']
    else:
        episode = None

    urls = service.retrieve_urls(params['id'], season=season, episode=episode)

    if not urls:
        return plex_util.no_contents()
    else:
        oc = ObjectContainer(title2=unicode(params['name']))

        media_info = MediaInfo(**params)

        service.queue.handle_bookmark_operation(operation, media_info)

        document = service.fetch_document(params['id'])
        data = service.get_media_data(document)

        if episode:
            media_info['type'] = 'episode'
            media_info['index'] = int(episode)
            media_info['season'] = int(season)
            media_info['content_rating'] = data['rating']
            # show=show,
        else:
            media_info['type'] = 'movie'
            media_info['year'] = data['year']
            media_info['genres'] = data['genres']
            media_info['countries'] = data['countries']
            media_info['genres'] = data['genres']
            # video.tagline = 'tagline'
            # video.original_title = 'original_title'

        url_items = []

        Log(urls)

        for url in urls:
            url_items.append(
                {
                    "url": url['url'],
                    "config": {
                        # "container": audio_container,
                        # "audio_codec": audio_codec,
                        "video_resolution": url['height'],
                        "width": url['width'],
                        "height": url['height'],
                        "bitrate": url['bandwidth'],
                        # "duration": duration
                    }
                })

        media_info['rating_key'] = service.get_episode_url(params['id'], season, 0)
        media_info['rating'] = data['rating']
        media_info['tags'] = data['tags']
        media_info['summary'] = data['summary']
        # media_info['thumb'] = data['thumb']
        # media_info['art'] = data['thumb']
        # media_info['season'] = season
        # media_info['episode'] = episode

        oc.add(MetadataObjectForURL(media_info, url_items=url_items, player=PlayVideo))

        if str(container) == 'False':
            history.push_to_history(Data, media_info)
            service.queue.append_bookmark_controls(oc, HandleMovie, media_info)

        return oc

@route(PREFIX + '/search')
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
        name = item['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

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
        name = item['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

def BuildSearchYears(oc, document, query):
    response = service.search_years(document=document, query=query)

    for item in response:
        path = item['path']
        name = item['name']

        key = Callback(HandleMovies, path=path, title=name)

        oc.add(DirectoryObject(key=key, title=name))

def BuildSearchMovies(oc, page, query):
    response = service.search(query=query, page=page)

    for movie in response['items']:
        name = movie['name']
        thumb = movie['thumb']

        new_params = {
            'id': movie['path'],
            'title': name,
            'name': name,
            'thumb': thumb
        }
        key = Callback(HandleMovieOrSerie, **new_params)

        oc.add(DirectoryObject(key=key, title=name, thumb=thumb))

    pagination.append_controls(oc, response, page=page, callback=HandleSearch, query=query)

@route(PREFIX + '/container')
def HandleContainer(**params):
    type = params['type']

    if type == 'movie':
        return HandleMovie(**params)
    elif type == 'episode':
        return HandleMovie(**params)
    elif type == 'season':
        return HandleSeason(**params)
    elif type == 'serie':
        return HandleSerie(**params)

@route(PREFIX + '/queue')
def HandleQueue():
    oc = ObjectContainer(title2=unicode(L('Queue')))

    service.queue.handle_queue_items(oc, HandleContainer, service.queue.data)

    if len(service.queue.data) > 0:
        oc.add(DirectoryObject(
            key=Callback(ClearQueue),
            title=unicode(L("Clear Queue"))
        ))

    return oc

@route(PREFIX + '/clear_queue')
def ClearQueue():
    service.queue.clear()

    return HandleQueue()

@route(PREFIX + '/history')
def HandleHistory():
    history_object = history.load_history(Data)

    oc = ObjectContainer(title2=unicode(L('History')))

    if history_object:
        data = sorted(history_object.values(), key=lambda k: k['time'], reverse=True)

        service.queue.handle_queue_items(oc, HandleContainer, data)

    return oc

def MetadataObjectForURL(media_info, url_items, player):
    metadata_object = FlowBuilder.build_metadata_object(media_type=media_info['type'], title=media_info['name'])

    metadata_object.key = Callback(HandleMovie, container=True, **media_info)

    metadata_object.title = media_info['name']
    metadata_object.rating_key = media_info['rating_key']
    metadata_object.rating = media_info['rating']
    metadata_object.thumb = media_info['thumb']
    metadata_object.art = media_info['thumb']
    metadata_object.tags = media_info['tags']
    metadata_object.summary = media_info['summary']
    # metadata_object.directors = data['directors']

    if 'duration' in media_info:
        metadata_object.duration = int(media_info['duration']) * 1000

    if 'artist' in media_info:
        metadata_object.artist = media_info['artist']

    metadata_object.items.extend(MediaObjectsForURL(url_items, player))

    return metadata_object

def MediaObjectsForURL(url_items, player):
    media_objects = []

    for item in url_items:
        url = item['url']
        config = item['config']

        play_callback = Callback(player, url=url)

        media_object = FlowBuilder.build_media_object(play_callback, config)

        media_objects.append(media_object)

    return media_objects

@indirect
@route(PREFIX + '/play_video')
def PlayVideo(url, live=True, play_list=True):
    if not url:
        return plex_util.no_contents()
    else:
        if str(play_list) == 'True':
            url = Callback(PlayList, url=url)

        if live:
            key = HTTPLiveStreamURL(url)
        else:
            key = RTMPVideoURL(url)

        return IndirectResponse(MovieObject, key)

@route(PREFIX + '/play_list.m3u8')
def PlayList(url):
    return service.get_play_list(url)
