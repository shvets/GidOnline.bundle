import library_bridge

AudioStreamObject = library_bridge.bridge.objects['AudioStreamObject']
AudioCodec = library_bridge.bridge.objects['AudioCodec']
VideoCodec = library_bridge.bridge.objects['VideoCodec']
VideoStreamObject = library_bridge.bridge.objects['VideoStreamObject']
PartObject = library_bridge.bridge.objects['PartObject']
MediaObject = library_bridge.bridge.objects['MediaObject']
EpisodeObject = library_bridge.bridge.objects['EpisodeObject']
TVShowObject = library_bridge.bridge.objects['TVShowObject']
MovieObject = library_bridge.bridge.objects['MovieObject']
TrackObject = library_bridge.bridge.objects['TrackObject']
VideoClipObject = library_bridge.bridge.objects['VideoClipObject']
Container = library_bridge.bridge.objects['Container']

class FlowBuilder():
    @staticmethod
    def build_media_object(play_callback, config):
        if config is None:
            config = {}

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

        # if 'width' in config.keys():
        #     media_object.width = config['width']
        #
        # if 'height' in config.keys():
        #     media_object.height = config['height']

        part_object = FlowBuilder.build_part_object(config)
        part_object.key = play_callback

        media_object.parts = [part_object]

        return media_object

    @staticmethod
    def build_part_object(config):
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


        if 'width' in config.keys():
            video_stream.width = config['width']

        if 'height' in config.keys():
            video_stream.height = config['height']

        part_object = PartObject(
            streams=[audio_stream, video_stream]
        )

        return part_object

    @staticmethod
    def build_metadata_object(media_type, title):
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

    @staticmethod
    def get_plex_config(format):
        container = None
        video_codec = None
        audio_codec = None

        if format == 'mp3':
            container = Container.MP3
            audio_codec = AudioCodec.MP3

        elif format == 'flac':
            container = Container.FLAC
            audio_codec = AudioCodec.FLAC

        elif format == 'ogg':
            container = Container.OGG
            audio_codec = AudioCodec.VORBIS

        elif format == 'm4a':
            container = Container.MP4
            audio_codec = AudioCodec.AAC

        elif format == 'mp4':
            container = Container.MP4
            video_codec = VideoCodec.H264
            audio_codec = AudioCodec.AAC

        elif format == 'avi':
            container = Container.AVI
            video_codec = 'mpeg4'
            audio_codec = AudioCodec.MP3

        elif format == 'ogv':
            container = Container.OGG
            video_codec = VideoCodec.THEORA
            audio_codec = AudioCodec.VORBIS

        elif format == 'wmv':
            container = 'wmv'
            video_codec = 'wmv3'
            audio_codec = 'wmvav2'

        elif format == 'mkv':
            container = Container.MKV
            video_codec = VideoCodec.H264
            audio_codec = AudioCodec.AAC

        if container:
            return {
                'container': container,
                'video_codec': video_codec,
                'audio_codec': audio_codec

            }
        else:
            return None