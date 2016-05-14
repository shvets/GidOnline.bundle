class MediaInfo(dict):
    def __init__(self, type='movie', **params):
        super(MediaInfo, self).__init__()

        self['type'] = type

        for key, value in params.iteritems():
            self[key] = value

    def value(self, name):
        if name  in self:
            return self[name]
