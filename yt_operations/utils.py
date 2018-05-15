class YTUtilsMixin:
    def chunks(self, channels_list, size):
        for i in range(0, len(channels_list), size):
            yield channels_list[i:i + size]

    def save_results(self):
        with open('search_result.csv', 'a') as file:
            for channel in self.collected_channels:
                file.write(f"{channel.get('id')},"
                           f"{channel.get('statistics', {}).get('subscriberCount', 0)},\n"
                           f"{channel.get('language',[])}\n")
