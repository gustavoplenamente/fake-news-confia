import json
import os

BASE_PATH = '../../Flávio/user_followers/'

if __name__ == '__main__':

    with open('user_followers.csv', 'w') as sheet:

        for _, _, files in os.walk(BASE_PATH):
            for file_name in files:
                file = os.path.join(BASE_PATH, file_name)
                with open(file) as user_file:
                    user_details = json.load(user_file)

                    user_id = str(user_details['user_id'])
                    followers = user_details['followers']

                    for follower_id in followers:
                        sheet.write('\t'.join([user_id, str(follower_id)]) + '\n')
