# encoding=utf-8
import json
import os
from datetime import datetime, timedelta
from typing import List

from src.user_news import get_news_id

BASE_PATH = '../../Flávio/news/News/'


def write_news_users_date_file(path):
    news_path = BASE_PATH + path
    file_name = f"news-temporal-series-{path.replace('/', '-')}.csv"

    with open(file_name, 'w') as news_temporal_series_file:

        header = '\t'.join(
            ['news_id', 'retweets', 'favourites', 'total tweets', '12h', '24h', '48h', '7 days', 'rest'])
        news_temporal_series_file.write(header + '\n')

        news_folders = next(os.walk(BASE_PATH + path))[1]

        for news_folder in news_folders:
            news_id = get_news_id(news_folder)

            news_details_path = os.path.join(news_path, news_folder)
            tweets_folder_path = os.path.join(news_details_path, 'tweets')

            news_retweets = 0
            news_favourites = 0
            tweet_instants = []

            for path, subdirs, tweets in os.walk(tweets_folder_path):

                for tweet in tweets:
                    tweet_path = os.path.join(news_path, news_folder, 'tweets',
                                              tweet)

                    with open(tweet_path) as tweet_json:
                        tweet_data = json.load(tweet_json)
                        created_at = datetime.strptime(tweet_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
                        tweet_instants.append(created_at)
                        favourite_count = tweet_data['favorite_count']

                        retweets_path = os.path.join(news_details_path, 'retweets')
                        retweet = tweet

                        retweet_file_name = os.path.join(retweets_path, retweet)

                        with open(retweet_file_name) as retweet_file:
                            retweets = json.load(retweet_file)['retweets']
                            retweet_count = len(retweets)

            news_retweets += retweet_count
            news_favourites += favourite_count
            news_tweets = len(tweets)
            news_date_ranges = get_classified_dates(tweet_instants)

            line = f"{news_id}\t{news_retweets}\t{news_favourites}\t{news_tweets}" \
                   f"\t{news_date_ranges['12h']}\t{news_date_ranges['24h']}" \
                   f"\t{news_date_ranges['48h']}\t{news_date_ranges['7 days']}" \
                   f"\t{news_date_ranges['rest']}"

            news_temporal_series_file.write(line + '\n')


def get_classified_dates(dates: List[datetime]):
    first = min(dates)

    buckets = {
        '12h': 0,
        '24h': 0,
        '48h': 0,
        '7 days': 0,
        'rest': 0
    }

    for date in dates:
        if date - first < timedelta(hours=12):
            buckets['12h'] += 1
        elif date - first < timedelta(days=1):
            buckets['24h'] += 1
        elif date - first < timedelta(days=2):
            buckets['48h'] += 1
        elif date - first < timedelta(days=7):
            buckets['7 days'] += 1
        else:
            buckets['rest'] += 1

    return buckets


if __name__ == '__main__':
    write_news_users_date_file('fake')
    write_news_users_date_file('notFake')
