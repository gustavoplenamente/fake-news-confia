import json

from scripts.utils import get_files, get_file

BASE_PATH = '../../user_followers/'


def count_followers_per_user():
    sheet = open('../../datasets/followers_count.csv', 'w')

    files = get_files(BASE_PATH)
    for file_name in files:
        full_file_name = get_file(BASE_PATH, file_name)
        file = open(full_file_name)
        user_details = json.load(file)

        user_id = str(user_details['user_id'])
        followers = user_details['followers']

        entry = map(str, [user_id, len(followers)])

        sheet.write('\t'.join(entry) + '\n')

        file.close()
    sheet.close()


if __name__ == '__main__':
    count_followers_per_user()
