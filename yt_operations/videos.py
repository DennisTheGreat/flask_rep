import json
import aiohttp


class VideoOperationsMixin:
    async def _parse_channel_videos(self, filtered_channels):
        for channel in filtered_channels:
            channel_id = channel.get('id', None)
            if not channel_id:
                continue
            parsing_channel_url = "https://www.googleapis.com/youtube/v3/search"
            parsing_channel_header = {'cache-control': "no-cache"}
            parsing_channel_query_string = {
                'part': 'id,snippet',
                'maxResults': '50',
                'order': 'date',
                'channelId': channel_id,
                'key': self.api_key
            }
            parsing_channel = None
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(parsing_channel_url,
                                       headers=parsing_channel_header,
                                       params=parsing_channel_query_string, ) as resp:
                    parsing_channel = await resp.read()
            parsing_channel_videos = json.loads(parsing_channel).get("items")
            channel['video_ids'] = [item for item in parsing_channel_videos
                                    if item.get('id', {}).get('videoId', None) is not None]
        return filtered_channels
