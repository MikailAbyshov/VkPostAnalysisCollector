from datetime import datetime
import requests


class PostAnalysisCollector:
    # Из ограничений VK API
    MAX_PARSE_VALUE = 100

    def __init__(self, TOKEN, DOMAIN, VERSION):
        self.TOKEN = TOKEN
        self.VERSION = VERSION
        self.DOMAIN = DOMAIN

    def __get_likes_count(self, post):
        return post["likes"]["count"]

    def __get_post_utc_time(self, post):
        date = datetime.fromtimestamp(post["date"])
        return date.strftime('%d - %m - %y')

    def __get_reposts_count(self, post):
        return post["reposts"]["count"]

    def __get_views_count(self, post):
        return post["views"]["count"]

    def __get_post_stats(self, post):
        return {"likes": self.__get_likes_count(post), "reposts": self.__get_reposts_count(post),
                "views": self.__get_views_count(post), "dateUTC": self.__get_post_utc_time(post)}

    def get_analysis_by_period(self):
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={'access_token': self.TOKEN,
                                        'domain': self.DOMAIN,
                                        'v': self.VERSION,
                                        'count': self.MAX_PARSE_VALUE,
                                        'filter': str('owner')
                                        })

        response = response.json()["response"]["items"]

        return [self.__get_post_stats(post) for post in response]


collector = PostAnalysisCollector(
    "vk1.a.W9u_U0QvOMhuW_WVLw3MfLHy9O7X2dziHDTYt2yOLtiXSvpCihODP_KHSzxpLArbKuvybK6S5kzC08pOVVfJzYLtGWErshvxuKMzo-aZU2BXozZXZJKAwtAoSCHyW1_0la9XDT2Bgqy3HkTbtYGBcyABNaAqFdbzbouEFyTmrDs5JIAqAErpmyMEvc6wdn7G",
    "fmf_ipmm", 5.199)

result = collector.get_analysis_by_period()

for i in result:
    print(i)
