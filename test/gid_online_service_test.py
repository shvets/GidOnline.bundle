# -*- coding: utf-8 -*-

import test_helper

import json
import re

import unittest

from gid_online_service import GidOnlineService

service = GidOnlineService()

document = service.fetch_document(service.URL)
all_movies = service.get_movies(document)['items']

class GidOnlineServiceTest(unittest.TestCase):
    def test_get_genres(self):
        result = service.get_genres(document)

        print(json.dumps(result, indent=4))

    def test_get_top_links(self):
        result = service.get_top_links(document)

        print(json.dumps(result, indent=4))

    def test_get_actors(self):
        result = service.get_actors(document)

        print(json.dumps(result, indent=4))

    def test_get_actors_by_letter(self):
        result = service.get_actors(document, letter='А')

        print(json.dumps(result, indent=4))

    def test_get_directors(self):
        result = service.get_directors(document)

        print(json.dumps(result, indent=4))

    def test_get_directors_by_letter(self):
        result = service.get_directors(document, letter='В')

        print(json.dumps(result, indent=4))

    def test_get_countries(self):
        result = service.get_countries(document)

        print(json.dumps(result, indent=4))

    def test_get_years(self):
        result = service.get_years(document)

        print(json.dumps(result, indent=4))

    def test_get_seasons(self):
        result = service.get_seasons('/2016/03/strazhi-galaktiki/')

        print(json.dumps(result, indent=4))

    def test_get_episodes(self):
        result = service.get_episodes('/2016/03/strazhi-galaktiki')

        print(json.dumps(result, indent=4))

    def test_parse_movies_page(self):
        print(json.dumps(all_movies, indent=4))

    def test_get_movies_on_genre_page(self):
        document = service.fetch_document(service.URL + '/genre/vestern/')

        result = service.get_movies(document, '/genre/vestern/')

        print(json.dumps(result, indent=4))

    def test_retrieve_movie_url(self):
        # movie_url = all_movies[1]['path']
        #
        # print(movie_url)

        movie_url = 'http://gidonline.club/2016/05/lyubov-ne-po-razmeru/'

        urls = service.retrieve_urls(movie_url)

        print(json.dumps(urls, indent=4))

    def test_retrieve_serials_url(self):
        movie_url = 'http://gidonline.club/2016/03/strazhi-galaktiki/'

        document = service.get_movie_document(movie_url)

        serial_info = service.get_serial_info(document)

        print(json.dumps(serial_info, indent=4))

    def test_get_play_list(self):
        #movie_url = all_movies[0]['path']
        movie_url = 'http://gidonline.club/2016/05/lyubov-ne-po-razmeru/'

        urls = service.retrieve_urls(movie_url)

        print(json.dumps(urls, indent=4))

        play_list = service.get_play_list(urls[2]['url'])

        print(play_list)

    def test_get_media_data(self):
        movie_url = all_movies[0]['path']

        document = service.fetch_document(movie_url)

        data = service.get_media_data(document)

        print(json.dumps(data, indent=4))

    def test_get_serials_info(self):
        movie_url = 'http://gidonline.club/2016/03/strazhi-galaktiki/'

        document = service.get_movie_document(movie_url)

        serial_info = service.get_serial_info(document)

        print(json.dumps(serial_info, indent=4))

        # for number, name in serial_info['seasons'].iteritems():
        #     print(number)
        #     print(name)

        for number in sorted(serial_info['seasons'].keys()):
            print(number)
            print(serial_info['seasons'][number])

    def test_re(self):
        s = "http://gidonline.club/page/772/"

        data = re.search('(' + service.URL + '/page/)(\d*)/', s)

        print(data.group(2))

    def test_search(self):
        query = 'день выборов 2'

        result = service.search(query)

        print(json.dumps(result, indent=4))

    def test_search_actors(self):
        query = 'Аллен'

        result = service.search_actors(document, query)

        print(json.dumps(result, indent=4))

    def test_search_director(self):
        query = 'Люк'

        result = service.search_directors(document, query)

        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    unittest.main()
