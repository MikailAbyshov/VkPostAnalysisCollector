from datetime import datetime
import requests
from typing import Any
from collections import namedtuple


class PostAnalysisCollector:
    # Из ограничений VK API
    MAX_PARSE_VALUE = 100

    # VERSION - желательно 5.199, ибо протестировано
    def __init__(self, TOKEN: str, DOMAIN: str, VERSION: str = '5.199'):
        self.TOKEN: str = TOKEN
        self.DOMAIN: str = DOMAIN
        self.VERSION: str = VERSION

    def __get_likes_count(self, post: dict[str, Any]) -> int:
        return post["likes"]["count"]

    def __get_post_utc_time(self, post: dict[str, Any]) -> str:
        date = datetime.fromtimestamp(post["date"])
        return date.strftime("%d/%m/%Y")

    def __get_reposts_count(self, post: dict[str, Any]) -> int:
        return post["reposts"]["count"]

    def __get_post_timestamp(self, post: dict[str, Any]) -> int:
        return post['date']

    def __get_views_count(self, post: dict[str, Any]) -> int:
        return post["views"]["count"]

    def __get_comments_count(self, post: dict[str, Any]) -> int:
        return post["comments"]["count"]

    def __get_posts_in_time_period(self, start_date: datetime, end_date: datetime) -> list[dict[str, Any]]:

        earliest_post_date = datetime.max
        current_offset = 0
        needed_posts = []

        with requests.Session() as session:
            while earliest_post_date >= start_date:
                response = session.get('https://api.vk.com/method/wall.get',
                                       params={'access_token': self.TOKEN,
                                               'domain': self.DOMAIN,
                                               'v': self.VERSION,
                                               'count': self.MAX_PARSE_VALUE,
                                               'offset': current_offset,
                                               'filter': 'owner'
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

    def __get_post_stats(self, post: dict[str, Any]) \
            -> namedtuple(typename="PostStats",
                          field_names=['likes', 'reposts', 'views', 'comments', 'dateUTC', 'timestamp']):

        PostStats = namedtuple('PostStats',
                               ['likes', 'reposts', 'views', 'comments', 'dateUTC', 'timestamp'])

        return PostStats(
            likes=self.__get_likes_count(post),
            reposts=self.__get_reposts_count(post),
            views=self.__get_views_count(post),
            comments=self.__get_comments_count(post),
            dateUTC=self.__get_post_utc_time(post),
            timestamp=self.__get_post_timestamp(post)
        )

    def get_analysis_by_period(self, start_date: datetime, end_date: datetime) \
            -> list[namedtuple(typename="PostStats",
                               field_names=['likes', 'reposts', 'views', 'comments', 'dateUTC', 'timestamp'])]:

        post_statistic = [
            self.__get_post_stats(post)
            for post in self.__get_posts_in_time_period(start_date, end_date)
        ]

        return sorted(post_statistic, key=lambda post: post.timestamp)
