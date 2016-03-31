import re
import base64
import json
from lxml.etree import tostring

from http_service import HttpService

class MwService(HttpService):

    def get_session_data(self, document):
        body = tostring(document.xpath('body')[0])

        session_data = re.compile(
            ('\$\.post\(\'/sessions\/create_session\', {((?:.|\n)+)}\)\.success')
        ).search(body, re.MULTILINE)

        if session_data:
            session_data = session_data.group(1).replace('condition_detected ? 1 : ', '')

            new_session_data = self.replace_keys('{%s}' % session_data,
                                                 ['partner', 'd_id', 'video_token', 'content_type', 'access_key', 'cd'])

            return json.loads(new_session_data)

    def get_content_data(self, document):
        body = tostring(document.xpath('body')[0])

        data = re.compile(
            ('setRequestHeader\|([^|]+)')
        ).search(body, re.MULTILINE)

        if data:
            return base64.b64encode(data.group(1))

    # def get_cookies(self, response):
    #     return None
    #
    # def get_csrf_token(self):
    #     return None

    def get_cookie_info(self, url):
        response = self.http_request(url)
        document = self.to_document(response.read())

        cookie = response.headers['Set-Cookie']

        index = cookie.index(';')

        cookie = cookie[0: index + 1]

        csrf_token = document.xpath('//meta[@name="csrf-token"]/@content')[0]

        return {'cookie': str(cookie), 'csrf-token': str(csrf_token)}

    def get_urls(self, headers, data):
        response = self.http_request(method='POST', url='http://moonwalk.cc/sessions/create_session',
                                     headers=headers, data=data)

        data = json.loads(response.read())

        manifest_url = data['manifest_m3u8']

        response2 = self.http_request(manifest_url)

        data2 = response2.read()

        #url2 = [line for line in data2.splitlines() if line].pop()

        lines = data2.splitlines()

        urls = []

        for index, line in enumerate(lines):
            if line.startswith('#EXTM3U'):
                continue
            elif not line.startswith('#EXT-X-STREAM-INF'):
                data = re.search("#EXT-X-STREAM-INF:RESOLUTION=(\d+)x(\d+),BANDWIDTH=(\d+)", lines[index-1])

                urls.append({"url": line, "width": data.group(1), "height": data.group(2), "bandwith": data.group(3)})

        return urls

    def replace_keys(self, s, keys):
        s = s.replace('\'', '"')

        for key in keys:
            s = s.replace(key + ':', '"' + key + '":')

        return s