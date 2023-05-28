import vk_api
from secret import *

import pandas as pd
from tqdm import tqdm

import argparse
import os


class Downloader:

    def __init__(self, group_id, posts_count, comments_count, post_offset=0):
        api = vk_api.VkApi(login=LOGIN, password=PASSWORD)
        api.auth()

        self._session = api.get_api()
        self._group_id = group_id
        self._pc = posts_count
        self._cc = comments_count
        self._po = post_offset

    def download(self, folder):

        if not os.path.exists(os.path.join(folder, str(self._group_id))):
            os.mkdir(os.path.join(folder, str(self._group_id)))

        all_posts = list()
        for offset in tqdm(range(0, self._pc, 100), desc='posts: '):
            posts_raw = self._session.wall.get(owner_id=self._group_id,
                                               offset=offset + self._po,
                                               count=min(self._pc - offset, 100))['items']
            for post in posts_raw:
                post = {**_only_keys(post, {'id', 'owner_id', 'date', 'text'}),
                        'likes': post.get('likes', {'count': 0})['count'],
                        'reposts': post.get('reposts', {'count': 0})['count'],
                        'views': post.get('views', {'count': 0})['count']}
                post['text'] = post['text'].replace('\n', '\\n')
                all_posts.append(post)
        posts_df = pd.DataFrame(all_posts, columns=['id', 'owner_id', 'date', 'views', 'likes', 'reposts', 'text'])
        posts_df.to_csv(os.path.join(folder, str(self._group_id), f'posts_{self._po}-{self._po + self._pc}.csv'), index=False)

        all_comments = list()
        for post in tqdm(all_posts, desc='comments: '):
            for offset in range(0, self._cc, 100):
                comments_raw = self._session.wall.getComments(owner_id=self._group_id,
                                                              post_id=post['id'],
                                                              need_likes=1,
                                                              count=min(self._cc - offset, 100),
                                                              offset=offset)['items']
                for comment in comments_raw:
                    comment = {**_only_keys(comment, {'id', 'from_id', 'date', 'text'}),
                               'likes': comment.get('likes', {'count': 0})['count'],
                               'post_id': post['id']}
                    comment['text'] = comment['text'].replace('\n', '\\n')
                    all_comments.append(comment)
                if len(comments_raw) < 100:
                    break
        comments_df = pd.DataFrame(all_comments, columns=['id', 'post_id', 'from_id', 'date', 'likes', 'text'])
        comments_df.to_csv(os.path.join(folder, str(self._group_id), f'comments_{self._po}-{self._po + self._pc}.csv'), index=False)

        uids = list(set(comments_df['from_id'].values) - {0})

        all_users = list()
        basic_fields = ['id', 'first_name', 'last_name', 'deactivated', 'is_closed']
        optional_fields = ['bdate', 'city', 'country', 'followers_count', 'has_photo',
                           'home_town', 'is_no_index', 'sex', 'verified']
        for i in tqdm(range(0, len(uids), 1000), desc='users: '):
            users = self._session.users.get(user_ids=uids[i:i + 1000],
                                            fields=optional_fields)
            all_users += [{**_only_keys(user, set(basic_fields + optional_fields) - {'city', 'country'}),
                           'city': user.get('city', {'title': ''})['title'],
                           'country': user.get('country', {'title': ''})['title']} for user in users]

        result_df = pd.DataFrame(all_users, columns=basic_fields + optional_fields)
        result_df.to_csv(os.path.join(folder, str(self._group_id), f'users_{self._po}-{self._po + self._pc}.csv'), index=False)

    def close(self):
        # self._session.close()
        pass


def _only_keys(d, key_set):
    return {k: d[k] for k in d.keys() & key_set}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('group_id', type=int, help='VK Group ID from which posts and comments must be downloaded.')
    parser.add_argument('posts_count', type=int, help='Number of posts to be downloaded.')
    parser.add_argument('comments_count', type=int, help='Maximum number of comments to download from each post.')
    parser.add_argument('-o', '--offset', type=int, default=0, help='Number of posts to skip before downloading.')
    parser.add_argument('-f', '--folder', type=str, default='', help='Folder that will contain results.')
    args = parser.parse_args()

    downloader = Downloader(args.group_id,
                            posts_count=args.posts_count,
                            comments_count=args.comments_count,
                            post_offset=args.offset)
    downloader.download(args.folder)
