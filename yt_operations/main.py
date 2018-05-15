import asyncio
from yt_operations import ChannelOperationsMixin
from yt_operations import VideoOperationsMixin
from yt_operations import YTUtilsMixin
from yt_operations import LangOperationsMixin


class YouTubeParser(ChannelOperationsMixin,
                    VideoOperationsMixin,
                    LangOperationsMixin,
                    YTUtilsMixin):
    api_key = 'AIzaSyBsQUYciMnQcLn1utCzx74VmiF9BONg3mM'
    collected_channels = []
    ioloop = asyncio.get_event_loop()
    tasks = []
    task_size = 2
    quote = 0

    def init_search_by_keyword(self, keyword_list):
        for kw in keyword_list:
            self.tasks.append(asyncio.ensure_future(self._main(kw)))
            self.quote += 100

            if len(self.tasks) > self.task_size:
                self.ioloop.run_until_complete(
                    asyncio.gather(*self.tasks)
                )
                self.tasks = []

        if len(self.tasks) > 0:
            self.ioloop.run_until_complete(
                asyncio.gather(*self.tasks)
            )

    async def _main(self, keyword):
        print('Performing channels search by keywords')
        channels = await self._parse_channels(keyword)

        print("{} channels collected".format(len(channels)))
        filtered_channels = await self._filter_channels(channels)

        print("{} remaining after filtration".format(len(filtered_channels)))
        filtered_channels_with_videos = await self._parse_channel_videos(filtered_channels)

        print('collecting channels videos and detecting language')
        filtered_channels_with_lang = await self._detect_channel_language(filtered_channels_with_videos)

        self.collected_channels.extend(filtered_channels_with_lang)

