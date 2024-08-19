from datetime import datetime
import requests


class PostAnalysisCollector:
    # Из ограничений VK API
    MAX_PARSE_VALUE = 100

    # VERSION - желательно 5.199, ибо протестировано
    def __init__(self, TOKEN, DOMAIN, VERSION):
        self.TOKEN = TOKEN
        self.VERSION = VERSION
        self.DOMAIN = DOMAIN

    def __get_likes_count(self, post):
        return post["likes"]["count"]

    def __get_post_utc_time(self, post, date_time_format):
        date = datetime.fromtimestamp(post["date"])
        return date.strftime(date_time_format)

    def __get_reposts_count(self, post):
        return post["reposts"]["count"]

    def __get_post_timestamp(self, post):
        return post['date']

    def __get_views_count(self, post):
        return post["views"]["count"]

    def __get_comments_count(self, post):
        return post["comments"]["count"]

    def __get_posts_in_time_period(self, start_date, end_date, date_time_format):
        start_date = datetime.strptime(start_date, date_time_format)
        end_date = datetime.strptime(end_date, date_time_format)

        earliest_post_date = datetime.max
        current_offset = 0
        needed_posts = []

        while earliest_post_date >= start_date:

            response = requests.get('https://api.vk.com/method/wall.get',
                                    params={'access_token': self.TOKEN,
                                            'domain': self.DOMAIN,
                                            'v': self.VERSION,
                                            'count': self.MAX_PARSE_VALUE,
                                            'offset': current_offset,
                                            'filter': str('owner')
                                            }).json()['response']['items']

            for post in response:
                post_date = datetime.fromtimestamp(post['date'])

                if post_date < earliest_post_date:
                    earliest_post_date = post_date

                if start_date <= post_date <= end_date:
                    needed_posts.append(post)

            current_offset += self.MAX_PARSE_VALUE

            if len(response) < self.MAX_PARSE_VALUE:
                break

        return needed_posts

    def __get_post_stats(self, post, date_time_format):
        return {"likes": self.__get_likes_count(post),
                "reposts": self.__get_reposts_count(post),
                "views": self.__get_views_count(post),
                "comments": self.__get_comments_count(post),
                "dateUTC": self.__get_post_utc_time(post, date_time_format=date_time_format),
                "timestamp": self.__get_post_timestamp(post)}

    def get_analysis_by_period(self, start_date, end_date, date_time_format='%d/%m/%Y'):
        post_statistic = [self.__get_post_stats(post, date_time_format=date_time_format) for post
                          in self.__get_posts_in_time_period(start_date, end_date, date_time_format=date_time_format)]

        return sorted(post_statistic, key=lambda post: post['timestamp'])


collector = PostAnalysisCollector(
    "vk1.a.W9u_U0QvOMhuW_WVLw3MfLHy9O7X2dziHDTYt2yOLtiXSvpCihODP_KHSzxpLArbKuvybK6S5kzC08pOVVfJzYLtGWErshvxuKMzo-aZU2BXozZXZJKAwtAoSCHyW1_0la9XDT2Bgqy3HkTbtYGBcyABNaAqFdbzbouEFyTmrDs5JIAqAErpmyMEvc6wdn7G",
    "fmf_ipmm", 5.199)

result = collector.get_analysis_by_period('13/05/2024', '16/08/2024')

for i in result:
    print(i)
