import sys
import urllib
import json
from lxml import html

try:
    from urllib2 import Request, urlopen
except:
    from urllib.request import Request, urlopen

class HttpService():
    def __init__(self):
        self.proxy = None
        self.proxyType = None

    def build_url(self, path, **params):
        url = path

        for key, val in params.items():
            if val is not None:
                delimiter = ('?', '&')['?' in url]
                url = url + delimiter + '%s=%s' % (key, urllib.quote(str(val)))

        return url

    def set_proxy(self, proxy, proxyType):
        self.proxy = proxy
        self.proxyType = proxyType

    def http_request(self, url, headers=None, data=None, method=None):
        if data is not None:
            data = urllib.urlencode(data)
            request = Request(url, data)
        else:
            request = Request(url)

        if self.proxy is not None:
            request.set_proxy(self.proxy, self.proxyType)

        if method is not None:
            request.get_method = lambda: method

        if headers:
            for key, value in headers.items():
                request.add_header(key, value)

        return urlopen(request)

    def get_content(self, response):
        content = response.read()

        if sys.version_info.major == 3:
            return content.decode('utf-8')
        else:
            return content

    def get_base_url(self, url):
        path = url.split('/')
        path.pop()
        path = '/'.join(path)

        return path

    def get_play_list(self, url, base_url=None):
        if not base_url:
            base_url = self.get_base_url(url)

        lines = self.http_request(url).read().splitlines()

        new_lines = []

        for line in lines:
            if line[:1] == '#':
                new_lines.append(line)
            else:
                new_lines.append(base_url + '/' + line)

        return "\n".join(new_lines)

    def get_play_list_urls(self, url):
        play_list = self.get_play_list(url)

        lines = play_list.splitlines()

        urls = []

        for line in lines:
            if line[:1] != '#':
                urls.append(line)

        return urls

    def fetch_content(self, url, headers=None):
        return self.http_request(url, headers=headers).read()

    def fetch_document(self, url, headers=None):
        content = self.fetch_content(url, headers=headers)

        return self.to_document(content)

    def to_document(self, buffer):
        return html.fromstring(buffer)

    def to_json(self, buffer):
        if not buffer:
            buffer = "{}"

        return json.loads(buffer)