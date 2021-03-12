# encoding=utf-8

import os
import json
import re

BASE_PATH = '../../fakenewsnet_dataset1/'


def get_news_id(news_folder_name):
    return re.search(r'\d+', news_folder_name).group()


def write_news_file(path):
    news_path = BASE_PATH + path
    file_name = f"news-{path.replace('/', '-')}.csv"
    news_folders = next(os.walk(news_path))[1]

    with open(file_name, 'w') as news_file:
        for news_folder in news_folders:
            news_id = get_news_id(news_folder)
            news_file.write(news_id + '\n')


def write_news_with_authors_file(path):
    news_path = BASE_PATH + path
    file_name = f"news-authors-{path.replace('/', '-')}.csv"
    news_folders = next(os.walk(news_path))[1]

    with open(file_name, 'w') as news_file:
        for news_folder in news_folders:
            news_id = get_news_id(news_folder)
            news_folder_path = os.path.join(news_path, news_folder)
            for path, subdirs, files in os.walk(news_folder_path):
                if 'news content.json' not in files and 'tweets' not in subdirs:
                    continue
                if 'news content.json' in files:
                    news_content_file = os.path.join(news_path, news_folder, files[0])
                    with open(news_content_file) as news_content:
                        news_data = json.load(news_content)
                        authors = news_data['authors']
                        authors_text = "\t".join(authors)
                        news_file.write(f"{news_id}\t"+authors_text+"\n")
                else:
                    news_file.write(f"{news_id}\n")


def write_news_with_authors_number_file(path):
    news_path = BASE_PATH + path
    file_name = f"news-authors-{path.replace('/', '-')}.csv"
    news_folders = next(os.walk(news_path))[1]
    count = 0

    with open(file_name, 'w') as news_file:
        for news_folder in news_folders:
            news_id = get_news_id(news_folder)
            news_folder_path = os.path.join(news_path, news_folder)
            for path, subdirs, files in os.walk(news_folder_path):
                if 'news content.json' not in files and 'tweets' not in subdirs:
                    continue
                if 'news content.json' in files:
                    news_content_file = os.path.join(news_path, news_folder, files[0])
                    with open(news_content_file) as news_content:
                        news_data = json.load(news_content)
                        authors_number = len(news_data['authors'])
                        count += 1
                        news_file.write(f"{news_id}\t{authors_number}\n")
                else:
                    news_file.write(f"{news_id}\t0\n")

    print(f"count: {count}")


def write_news_with_tweets_folder(path):
    news_path = BASE_PATH + path
    file_name = f"news-tweets-{path.replace('/', '-')}.csv"
    news_folders = next(os.walk(news_path))[1]

    with open(file_name, 'w') as news_file:
        for news_folder in news_folders:
            news_id = get_news_id(news_folder)
            news_folder_path = os.path.join(news_path, news_folder)
            for path, subdirs, files in os.walk(news_folder_path):
                if 'news content.json' not in files and 'tweets' not in subdirs:
                    continue
                has_tweets = 'tweets' in subdirs
                news_file.write(f"{news_id}\t{has_tweets}\n")


def write_users_file(path):
    news_path = BASE_PATH + path
    file_name = f"users-{path.replace('/', '-')}.csv"
    news_folders = next(os.walk(news_path))[1]

    with open(file_name, 'w') as users_file:
        for news_folder in news_folders:
            tweets_folder_path = os.path.join(news_path, news_folder, 'tweets')
            for path, subdirs, tweets_files in os.walk(tweets_folder_path):
                for tweet_file in tweets_files:
                    tweet_file = os.path.join(news_path, news_folder, 'tweets',
                                              tweet_file)
                    with open(tweet_file) as tweet_json:
                        tweet_data = json.load(tweet_json)
                        user_id = tweet_data['user']['id']
                        users_file.write(f"{user_id}\n")


def write_news_users_date_file(path, total_tweets):
    news_path = BASE_PATH + path
    file_name = f"news-user-date-{path.replace('/', '-')}.csv"

    with open(file_name, 'w') as news_user_date_file:

        news_folders = next(os.walk(BASE_PATH + path))[1]

        tweet_counter = 0
        counter = 0

        for news_folder in news_folders:
            news_id = get_news_id(news_folder)

            tweets_folder_path = os.path.join(news_path, news_folder, 'tweets')
            for path, subdirs, tweets_files in os.walk(tweets_folder_path):

                total = len(tweets_files)
                tweet_counter += counter
                counter = 0

                for tweet_file in tweets_files:
                    tweet_file = os.path.join(news_path, news_folder, 'tweets',
                                              tweet_file)

                    counter += 1
                    progress = 100*tweet_counter/total_tweets
                    print(f"{news_id}: {counter}/{total}\t{round(progress, 2)}%")

                    with open(tweet_file) as tweet_json:
                        tweet_data = json.load(tweet_json)
                        user_id = tweet_data['user']['id']
                        created_at = tweet_data['created_at']
                        news_user_date_file.write(
                            f"{news_id}\t{user_id}\t{created_at}\n"
                        )


def get_news():
    # write_news_file(get_news_path())

    # write_users_frequency_file(get_news_path())

    # write_users_file(get_news_path())

    write_news_with_authors_number_file('gossipcop/fake')
    write_news_with_authors_number_file('gossipcop/real')
    write_news_with_authors_number_file('politifact/fake')
    write_news_with_authors_number_file('politifact/real')

    # write_news_users_date_file('gossipcop/real', 815013)
    # write_news_users_date_file('gossipcop/fake', 815013)
    # write_news_users_date_file('politifact/real', 815013)
    # write_news_users_date_file('politifact/fake', 815013)
    # write_users_file('gossipcop/fake')
    # write_users_file('politifact/real')
    # write_users_file('politifact/fake')


if __name__ == '__main__':
    get_news()
