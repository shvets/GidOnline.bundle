import urllib
import re
import operator

from mw_service import MwService

class GidOnlineService(MwService):
    URL = "http://gidonline.club"

    def get_genres(self):
        response = self.http_request(self.URL)
        document = self.to_document(response.read())

        list = []

        links = document.xpath('//div[@id="catline"]//li/a')

        for link in links:
            path = link.xpath('@href')[0]
            name = unicode(link.xpath('text()')[0])

            list.append({"path": path, "name": name[0] + name[1:].lower()})

        return list

    def get_top_links(self):
        response = self.http_request(self.URL)
        document = self.to_document(response.read())

        list = []

        links = document.xpath('//div[@id="topls"]/a[@class="toplink"]')

        for link in links:
            path = link.xpath('@href')[0]
            name = unicode(link.xpath('text()')[0])
            thumb = self.URL + (link.xpath('img')[0].xpath("@src"))[0]

            list.append({"path": path, "name": name, "thumb": thumb})

        return list

    def get_actors(self, letter=None):
        response = self.http_request(self.URL)
        document = self.to_document(response.read())

        all_actors = self.fix_name(self.get_category('actors-dropdown', document))

        all_actors = sorted(all_actors, key=operator.itemgetter("name"))

        if letter:
            actors = filter(lambda x: x['name'][0] == letter.decode('utf-8'), all_actors)
        else:
            actors = all_actors

        return self.fix_path(actors)

    def get_directors(self, letter=None):
        response = self.http_request(self.URL)
        document = self.to_document(response.read())

        all_directors = self.fix_name(self.get_category('director-dropdown', document))

        all_directors = sorted(all_directors, key=operator.itemgetter("name"))

        if letter:
            directors = filter(lambda x: x['name'][0] == letter.decode('utf-8'), all_directors)
        else:
            directors = all_directors

        return self.fix_path(directors)

    def get_countries(self):
        response = self.http_request(self.URL)
        document = self.to_document(response.read())

        return self.fix_path(self.get_category('country-dropdown', document))

    def get_years(self):
        response = self.http_request(self.URL)
        document = self.to_document(response.read())

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

    def get_movies(self, path=None, page=1):
        url = self.URL

        if path:
            url = url + path

        if page > 1:
            url = url + "/page/" + str(page) + '/'

        response = self.http_request(url).read()
        document = self.to_document(response)

        result = {'movies': []}

        links = document.xpath('//div[@id="main"]/div[@id="posts"]/a[@class="mainlink"]')

        for link in links:
            href = link.xpath('@href')[0]
            name = unicode(link.xpath('span')[0].text_content())
            thumb = self.URL + (link.xpath('img')[0].xpath("@src"))[0]

            result['movies'].append({"path": href, "name": name, "thumb": thumb})

        if len(result['movies']) > 0:
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

    def find_pages(self, path, link):
        search_mode = (path and path.find('/?s=') >= 0)

        if path:
            if search_mode:
                pattern = self.URL + '/page/'
            else:
                pattern = self.URL + path + 'page/'
        else:
            pattern = self.URL + '/page/'

        data = re.search('(' + pattern + ')(\d*)/', link)

        return int(data.group(2))

    def get_movie_details(self, url):
        response = self.http_request(url).read()

        list = []

        links = self.to_document(response).xpath('//div[@id="main"]/div[@id="face"]//div[@class="t-row"]//div[@class="rl-1"]')

        for link in links:
            details = {}
            details['text'] = link.xpath("text()")

            list.append(details)

        return list

    def get_gateway_url(self, url):
        response = self.http_request(url)
        document = self.to_document(response.read())

        frame_block = document.xpath('//div[@class="tray"]')[0]

        urls = frame_block.xpath('iframe[@class="ifram"]/@src')

        return urls[0]

    def get_movie_document(self, url, season=None, episode=None):
        iframe_url = self.get_gateway_url(url)

        new_url = iframe_url

        if season:
            new_url = '%s?season=%d&episode=%d' % (iframe_url, int(season), int(episode))

        response = self.http_request(new_url)

        return self.to_document(response.read())

    def retrieve_url(self, url, season=None, episode=None):
        document = self.get_movie_document(url, season=season, episode=episode)

        data = self.get_session_data(document)

        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': url,
            'Content-Data': self.get_content_data(document)
            # 'Cookie': cookie_info['cookie'],
            # 'X-CSRF-Token': cookie_info['csrf-token']
        }

        return self.get_url(headers, data)

    def get_media_data(self, path):
        data = {}

        response = self.http_request(path)
        document = self.to_document(response.read())

        block = document.xpath('//div[@id="face"]')[0]

        thumb = block.xpath('div/img[@class="t-img"]')[0].get("src")

        data['thumb'] = self.URL + thumb

        items1 = block.xpath('div/div[@class="t-row"]/div[@class="r-1"]//div[@class="rl-2"]')
        items2 = block.xpath('div/div[@class="t-row"]/div[@class="r-2"]//div[@class="rl-2"]')

        data['title'] = items1[0].text_content()
        data['country'] = items1[1].text_content()
        data['duration'] = self.convert_duration(items1[2].text_content())
        data['year'] = int(items2[0].text_content())
        data['tags'] = items2[1].text_content().split(',')

        description_block = document.xpath('//div[@class="description"]')[0]

        data['description'] = unicode(description_block.xpath('div[@class="infotext"]')[0].text_content())

        data['rating'] =float(document.xpath('//div[@class="nvz"]/meta')[1].get('content'))

        return data

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
        params = urllib.urlencode({
            's': query
        })

        if page > 1:
            path = "/page/" + str(page) + "/?" + params
        else:
            path = "/?" + params

        return self.get_movies(path)

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

        return hours * 60 + minutes

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