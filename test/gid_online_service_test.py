# -*- coding: utf-8 -*-

import test_helper

import json
import re

import unittest

from gid_online_service import GidOnlineService

class GidOnlineServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = GidOnlineService()

    def test_get_genres(self):
        result = self.service.get_genres()

        print(json.dumps(result, indent=4))

    def test_get_top_links(self):
        result = self.service.get_top_links()

        print(json.dumps(result, indent=4))

    def test_get_actors(self):
        result = self.service.get_actors()

        print(json.dumps(result, indent=4))

    def test_get_actors_by_letter(self):
        result = self.service.get_actors(letter='А')

        print(json.dumps(result, indent=4))

    def test_get_directors(self):
        result = self.service.get_directors()

        print(json.dumps(result, indent=4))

    def test_get_directors_by_letter(self):
        result = self.service.get_directors(letter='В')

        print(json.dumps(result, indent=4))

    def test_get_countries(self):
        result = self.service.get_countries()

        print(json.dumps(result, indent=4))

    def test_get_years(self):
        result = self.service.get_years()

        print(json.dumps(result, indent=4))

    def test_get_seasons(self):
        result = self.service.get_seasons('/2016/03/strazhi-galaktiki/')

        print(json.dumps(result, indent=4))

    def test_get_episodes(self):
        result = self.service.get_episodes('/2016/03/strazhi-galaktiki')

        print(json.dumps(result, indent=4))

    def test_parse_movies_page(self):
        result = self.service.parse_movies_page()

        print(json.dumps(result, indent=4))

    def test_get_movies_on_genre_page(self):
        result = self.service.parse_movies_page('/genre/vestern/')

        print(json.dumps(result, indent=4))

    def test_retrieve_movie_url(self):
        movies = self.service.parse_movies_page()['movies']

        movie_url = movies[1]['path']

        print(movie_url)

        url = self.service.retrieve_url(movie_url)

        print(url)

    def test_retrieve_serials_url(self):
        movie_url = 'http://gidonline.club/2016/03/strazhi-galaktiki/'

        url = self.service.retrieve_url(movie_url)

        print(url)

        document = self.service.get_movie_document(movie_url)

        serial_info = self.service.get_serial_info(document)

        print(json.dumps(serial_info, indent=4))

    def test_get_play_list(self):
        movies = self.service.parse_movies_page()['movies']

        movie_url = movies[0]['path']

        url = self.service.retrieve_url(movie_url)

        play_list = self.service.get_play_list(url)

        print(play_list)

    def test_get_media_data(self):
        movies = self.service.parse_movies_page()['movies']

        movie_url = movies[0]['path']

        data = self.service.get_media_data(movie_url)

        print(json.dumps(data, indent=4))

    def test_get_serials_info(self):
        movie_url = 'http://gidonline.club/2016/03/strazhi-galaktiki/'

        document = self.service.get_movie_document(movie_url)

        serial_info = self.service.get_serial_info(document)

        print(json.dumps(serial_info, indent=4))

        # for number, name in serial_info['seasons'].iteritems():
        #     print(number)
        #     print(name)

        for number in sorted(serial_info['seasons'].keys()):
            print(number)
            print(serial_info['seasons'][number])

    def test_re(self):
        s = "http://gidonline.club/page/772/"

        data = re.search('(' + self.service.URL + '/page/)(\d*)/', s)

        print(data.group(2))

    def test_search(self):
        query = 'папа'

        result = self.service.search(query)

        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    unittest.main()
