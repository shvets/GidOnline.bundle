import re
import base64
import json

from http_service import HttpService

class MwService(HttpService):

    def get_session_data(self, content):
        session_data = re.compile(
            ('\$\.post\(\'/sessions\/create_session\', {((?:.|\n)+)}\)\.success')
        ).search(content, re.MULTILINE)

        if session_data:
            session_data = session_data.group(1).replace('condition_detected ? 1 : ', '')

            new_session_data = self.replace_keys('{%s}' % session_data,
                                                 ['partner', 'd_id', 'video_token', 'content_type', 'access_key', 'cd'])

            return json.loads(new_session_data)

    def get_content_data(self, content):
        data = re.compile(
            ('setRequestHeader\|([^|]+)')
        ).search(content, re.MULTILINE)

        if data:
            return base64.b64encode(data.group(1))

    def get_urls(self, headers, data):
        urls = []

        try:
            response = self.http_request(method='POST', url='http://moonwalk.cc/sessions/create_session',
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
                        {"url": line, "width": int(data.group(1)), "height": int(data.group(2)), "bandwith": int(data.group(3))})
        except:
            pass

        return urls

    def replace_keys(self, s, keys):
        s = s.replace('\'', '"')

        for key in keys:
            s = s.replace(key + ':', '"' + key + '":')

        return s