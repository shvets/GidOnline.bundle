class FlowBuilder():
    def build_media_object(self, play_callback, config):
        if config is None:
            config = {}
        audio_stream = AudioStreamObject()

        audio_stream.channels = 2

        if 'audio_codec' in config.keys():
            audio_stream.codec = config['audio_codec']
        else:
            audio_stream.codec = AudioCodec.AAC

        if 'bitrate' in config.keys():
            audio_stream.bitrate = config['bitrate']

        if 'duration' in config.keys():
            audio_stream.bitrate = config['duration']

        video_stream = VideoStreamObject()

        if 'video_codec' in config.keys():
            video_stream.codec = config['video_codec']
        # else:
        #     video_stream.codec = VideoCodec.H264

        part_object = PartObject(
            key=play_callback,
            streams=[audio_stream, video_stream]
        )

        media_object = MediaObject()

        if 'optimized_for_streaming' in config.keys():
            media_object.protocol = config['optimized_for_streaming']
        else:
            media_object.optimized_for_streaming = True

        if 'protocol' in config.keys():
            media_object.protocol = config['protocol']
        # else:
        #     media_object.protocol = Protocol.HLS

        if 'container' in config.keys():
            media_object.container = config['container']
        # else:
        #     media_object.container = Container.MPEGTS

        if 'video_resolution' in config.keys():
            media_object.video_resolution = config['video_resolution']

        if 'width' in config.keys():
            media_object.video_resolution = config['width']

        if 'height' in config.keys():
            media_object.video_resolution = config['height']

        media_object.parts = [part_object]

        return media_object

    def build_metadata_object(self, media_type, title):
        if media_type == 'episode':
            metadata_object = EpisodeObject()

            metadata_object.show = title

        elif media_type == 'tv_show':
            metadata_object = TVShowObject()

        elif media_type == 'movie':
            metadata_object = MovieObject()

            metadata_object.title = title

        elif media_type == 'track':
            metadata_object = TrackObject()

            metadata_object.title = title

        else:
            metadata_object = VideoClipObject()

            metadata_object.title = title

        return metadata_object