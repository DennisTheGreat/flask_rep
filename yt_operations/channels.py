import json
import aiohttp
class ChannelOperationsMixin:
    async def _filter_channels(self, channels):
        result = []
        for channel_chunk in self.chunks(channels, size=50):
            self.quote += 3
            url = "https://www.googleapis.com/youtube/v3/channels"
            params = {
                "id": ",".join(channel_chunk),
                "part": "statistics",
                "key": self.api_key
            }
            response = None
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    response = await resp.text()

            filtered_channels = [channel for channel in
                                 json.loads(response).get('items', [])
                                 if int(channel.get('statistics', {})
                                        .get('subscriberCount', 0)) > 10000]

            result.extend(filtered_channels)

        return result

    async def _parse_channels(self, keyword):
        url = "https://www.googleapis.com/youtube/v3/search/"
        params = {
            "q": keyword,
            "type": "channel",
            "part": "id",
            "maxResults": 50,
            "key": self.api_key
        }
        response = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                response = await resp.text()

        channel_list = json.loads(response).get('items', []) \
            if response else []

        channel_list = [channel.get('id', {}).get('channelId')
                        for channel in channel_list]
        return channel_list
