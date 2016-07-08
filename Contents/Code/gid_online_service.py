# -*- coding: utf-8 -*-

import base64
import json
import urlparse
import re
import operator
from lxml.etree import tostring
from operator import itemgetter

from http_service import HttpService

class GidOnlineService(HttpService):
    URL = "http://gidonline.club"
    SESSION_URL = 'http://pandastream.cc/sessions/new'

    CYRILLIC_LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                        'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

    def get_page_url(self, path, page=1):
        url = self.URL

        if path:
            url = url + path

        if page > 1:
            url = url + "/page/" + str(page) + '/'

        return url

    def get_genres(self, document, type=None):
        list = []

        links = document.xpath('//div[@id="catline"]//li/a')

        for link in links:
            path = link.xpath('@href')[0]
            name = unicode(link.xpath('text()')[0])

            list.append({"path": path, "name": name[0] + name[1:].lower()})

        family_group = [
            list[14],
            list[15],
            list[12],
            list[8],
            list[10],
            list[5],
            list[13]
        ]

        crime_group = [
            list[4],
            list[9],
            list[2],
            list[0]
        ]

        fiction_group = [
            list[20],
            list[19],
            list[17],
            list[18]
        ]

        education_group = [
            list[1],
            list[7],
            list[3],
            list[6],
            list[11],
            list[16]
        ]

        if type == 'Family':
            return family_group
        elif type == 'Crime':
            return crime_group
        elif type == 'Fiction':
            return fiction_group
        elif type == 'Education':
            return education_group
        else:
            return family_group + crime_group + fiction_group + education_group

    def get_top_links(self, document):
        list = []

        links = document.xpath('//div[@id="topls"]/a[@class="toplink"]')

        for link in links:
            path = link.xpath('@href')[0]
            name = unicode(link.xpath('text()')[0])
            thumb = self.URL + (link.xpath('img')[0].xpath("@src"))[0]

            list.append({"path": path, "name": name, "thumb": thumb})

        return list

    def get_actors(self, document, letter=None):
        all_list = self.fix_name(self.get_category('actors-dropdown', document))

        all_list = sorted(all_list, key=operator.itemgetter("name"))

        if letter:
            list = filter(lambda x: x['name'][0] == letter.decode('utf-8'), all_list)
        else:
            list = all_list

        return self.fix_path(list)

    def get_directors(self, document, letter=None):
        all_list = self.fix_name(self.get_category('director-dropdown', document))

        all_list = sorted(all_list, key=operator.itemgetter("name"))

        if letter:
            list = filter(lambda x: x['name'][0] == letter.decode('utf-8'), all_list)
        else:
            list = all_list

        return self.fix_path(list)

    def get_countries(self, document):
        return self.fix_path(self.get_category('country-dropdown', document))

    def get_years(self, document):
        return self.fix_path(self.get_category('year-dropdown', document))

    def get_seasons(self, path):
        return self.get_category('season', self.get_movie_document(self.URL + path))

    def get_episodes(self, path):
        return self.get_category('episode', self.get_movie_document(self.URL + path))

    def get_category(self, id, document):
        list = []

        links = document.xpath('//select[@id="' + id + '"]/option')

        for link in links:
            path = link.xpath('@value')[0]
            name = unicode(link.text_content())

            if name:
                list.append({"path": path, "name": name})

        return list

    def find_pages(self, path, link):
        search_mode = (path and path.find('?s=') >= 0)

        if path:
            if search_mode:
                pattern = self.URL + '/page/'
            else:
                pattern = self.URL + path + 'page/'
        else:
            pattern = self.URL + '/page/'

        data = re.search('(' + pattern + ')(\d*)/', link)

        return int(data.group(2))

    def get_gateway_url(self, document):
        gateway_url = None

        frame_block = document.xpath('//div[@class="tray"]')[0]

        urls = frame_block.xpath('iframe[@class="ifram"]/@src')

        if len(urls) > 0:
            gateway_url = urls[0]
        else:
            url = self.URL + '/trailer.php'

            data = {
                'id_post': document.xpath('head/meta[@id="meta"]')[0].get('content')
            }
            response = self.http_request(url, method='POST', data=data)

            content = response.read()

            document = self.to_document(content)

            urls = document.xpath('//iframe[@class="ifram"]/@src')

            if len(urls) > 0:
                gateway_url = urls[0]

        return gateway_url

    def get_media_data(self, document):
        data = {}

        block = document.xpath('//div[@id="face"]')[0]

        thumb = block.xpath('div/img[@class="t-img"]')[0].get("src")

        data['thumb'] = self.URL + thumb

        items1 = block.xpath('div/div[@class="t-row"]/div[@class="r-1"]//div[@class="rl-2"]')
        items2 = block.xpath('div/div[@class="t-row"]/div[@class="r-2"]//div[@class="rl-2"]')

        data['title'] = items1[0].text_content()
        data['countries'] = items1[1].text_content().split(',')
        data['duration'] = self.convert_duration(items1[2].text_content())
        data['year'] = int(items2[0].text_content())
        data['tags'] = items2[1].text_content().split(',')
        data['genres'] = items2[1].text_content().split(',')

        description_block = document.xpath('//div[@class="description"]')[0]

        data['summary'] = unicode(description_block.xpath('div[@class="infotext"]')[0].text_content())

        data['rating'] = float(document.xpath('//div[@class="nvz"]/meta')[1].get('content'))

        return data

    def retrieve_urls(self, url, season=None, episode=None):
        if url.find(self.URL) < 0:
            url = self.URL + url

        document = self.get_movie_document(url, season=season, episode=episode)
        content = tostring(document.xpath('body')[0])

        data = self.get_session_data(content)

        content_data = self.get_content_data(content)

        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Encoding-Pool': content_data
        }

        return sorted(self.get_urls(headers, data), key=itemgetter('bandwidth'), reverse=True)

    def get_movie_document(self, url, season=None, episode=None):
        gateway_url = self.get_gateway_url(self.fetch_document(url))

        if season:
            movie_url = '%s?season=%d&episode=%d' % (gateway_url, int(season), int(episode))
        else:
            movie_url = gateway_url

        if movie_url.find('//www.youtube.com') > -1:
            movie_url = movie_url.replace('//', 'http://')

        return self.fetch_document(movie_url, self.get_headers(url))

    def get_serial_info(self, document):
        ret = {}

        ret['seasons'] = {}
        ret['episodes'] = {}

        for item in document.xpath('//select[@id="season"]/option'):
            value = int(item.get('value'))
            ret['seasons'][value] = unicode(item.text_content())
            if item.get('selected'):
                ret['current_season'] = int(value)

        for item in document.xpath('//select[@id="episode"]/option'):
            value = int(item.get('value'))
            ret['episodes'][value] = unicode(item.text_content())
            if item.get('selected'):
                ret['current_episode'] = int(value)

        return ret

    def search(self, query, page=1):
        url = self.build_url(self.get_page_url(None, page), s=query)

        response = self.http_request(url)
        content = response.read()
        document = self.to_document(content)

        movies = self.get_movies(document, url)

        if len(movies['items']) > 0:
            return movies
        else:
            document = self.fetch_document(response.url)

            media_data = self.get_media_data(document)

            return {'items': [
                {
                    'path': url,
                    'name': media_data['title'],
                    'thumb': media_data['thumb']
                }
            ]}

    def get_movies(self, document, path=None):
        result = {'items': []}

        links = document.xpath('//div[@id="main"]/div[@id="posts"]/a[@class="mainlink"]')

        for link in links:
            href = link.xpath('@href')[0]
            name = unicode(link.xpath('span')[0].text_content())
            thumb = self.URL + (link.xpath('img')[0].xpath("@src"))[0]

            result['items'].append({"path": href, "name": name, "thumb": thumb})

        if len(result['items']) > 0:
            result["pagination"] = self.extract_pagination_data(document, path)

        return result

    def extract_pagination_data(self, document, path):
        pagination_root = document.xpath('//div[@id="page_navi"]/div[@class="wp-pagenavi"]')

        if pagination_root:
            pagination_block = pagination_root[0]
            page = int(pagination_block.xpath('span[@class="current"]')[0].text_content())

            last_block = pagination_block.xpath('a[@class="last"]')

            if len(last_block) > 0:
                pages_link = last_block[0].get('href')

                pages = self.find_pages(path, pages_link)
            else:
                page_block = pagination_block.xpath('a[@class="page larger"]')
                pages_len = len(page_block)

                if pages_len == 0:
                    pages = page
                else:
                    pages_link = page_block[pages_len - 1].get('href')

                    pages = self.find_pages(path, pages_link)
        else:
            page = 1
            pages = 1

        return {
            "page": page,
            "pages": pages,
            "has_previous": page > 1,
            "has_next": page < pages,
        }

    def search_actors(self, document, query):
        return self.search_in_list(self.get_actors(document), query)

    def search_directors(self, document, query):
        return self.search_in_list(self.get_directors(document), query)

    def search_countries(self, document, query):
        return self.search_in_list(self.get_countries(document), query)

    def search_years(self, document, query):
        return self.search_in_list(self.get_years(document), query)

    def search_in_list(self, list, query):
        new_list = []

        for item in list:
            if item['name'].lower().find(query.decode('utf-8').lower()) >= 0:
                new_list.append(item)

        return new_list

    def fix_path(self, list):
        for item in list:
            item['path'] = item['path'][len(self.URL):]

        return list

    def fix_name(self, list):
        for item in list:
            name = item['name']

            names = name.split(' ')

            if len(names) > 1:
                item['name'] = " ".join(names[len(names) - 1:]) + ', ' + names[:len(names) - 1][0]

        return list

    def is_serial(self, path):
        document = self.get_movie_document(path)

        content = tostring(document.xpath('body')[0])

        data = self.get_session_data(content)

        return data and data['content_type'] == 'serial' or self.hasSeasons(path)

    def hasSeasons(self, url):
        path = urlparse.urlparse(url).path

        return len(self.get_seasons(path)) > 0

    def get_episode_url(self, url, season, episode):
        if season:
            return '%s?season=%d&episode=%d' % (url, int(season), int(episode))

        return url

    def get_thumb(self, path):
        if path.find(self.URL) < 0:
            thumb = self.URL + path
        else:
            thumb = path

        return thumb

    def convert_duration(self, s):
        tokens = s.split(' ')

        result = []

        for token in tokens:
            data = re.search('(\d+)', token)

            if data:
                result.append(data.group(0))

        if len(result) == 2:
            hours = int(result[0])
            minutes = int(result[1])
        else:
            hours = 0
            minutes = int(result[0])

        return hours * 60 * 60 + minutes * 60

    @staticmethod
    def get_headers(referer):
        return {
            'User-Agent': 'Plex-User-Agent',
            "Referer": referer
        }

    def get_session_data(self, content):
        path = urlparse.urlparse(self.SESSION_URL).path
        session_data = re.compile(
            ('\$\.post\(\'' + path + '\', {((?:.|\n)+)}\)\.success')
        ).search(content, re.MULTILINE)

        if session_data:
            session_data = session_data.group(1).replace('condition_detected ? 1 : ', '')

            new_session_data = self.replace_keys('{%s}' % session_data,
                                                 ['partner', 'd_id', 'video_token', 'content_type', 'access_key', 'cd'])

            return json.loads(new_session_data)

    def get_content_data(self, content):
        data = re.compile(
            ('setRequestHeader\|\|([^|]+)')
        ).search(content, re.MULTILINE)

        if data:
            return base64.b64encode(data.group(1))

    def get_urls(self, headers, data):
        urls = []

        try:
            response = self.http_request(method='POST', url=self.SESSION_URL,
                                         headers=headers, data=data)

            data = json.loads(response.read())

            manifest_url = data['manifest_m3u8']

            response2 = self.http_request(manifest_url)

            data2 = response2.read()

            lines = data2.splitlines()

            for index, line in enumerate(lines):
                if line.startswith('#EXTM3U'):
                    continue
                elif len(line.strip()) > 0 and not line.startswith('#EXT-X-STREAM-INF'):
                    data = re.search("#EXT-X-STREAM-INF:RESOLUTION=(\d+)x(\d+),BANDWIDTH=(\d+)", lines[index - 1])

                    urls.append(
                        {"url": line, "width": int(data.group(1)), "height": int(data.group(2)), "bandwidth": int(data.group(3))})
        except:
            pass

        return urls

    def replace_keys(self, s, keys):
        s = s.replace('\'', '"')

        for key in keys:
            s = s.replace(key + ':', '"' + key + '":')

        return s