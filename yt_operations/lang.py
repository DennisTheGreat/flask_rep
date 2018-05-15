import langid
from itertools import groupby as g


class LangOperationsMixin:
    @staticmethod
    def most_common_language(L):
        if L:
            return max(g(sorted(L)), key=lambda p: (lambda x, y: (len(list(y)), -L.index(x)))(*p))[0]

    async def _detect_channel_language(self, channels):
        for channel in channels:
            print('Detecting language for channel {}'.format(channel.get('id')))
            videos_lang = []
            for video in channel.get('video_ids', []):
                videos_lang.append(
                    langid.classify(video.get('snippet', {}).get('title', '') +
                                    video.get('snippet', {}).get('description', ''))[0]
                )
            channel_lang = self.most_common_language(videos_lang)
            print('langiage detected its {}'.format(channel_lang))
            channel['language'] = channel_lang
        return channels
