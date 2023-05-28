import vk_api
from secret import *


class Session:

    def __init__(self, group_id):
        api = vk_api.VkApi(login=LOGIN, password=PASSWORD)
        api.auth()

        self._session = api.get_api()
        self._group_id = group_id

    def get_posts_and_comments(self, count):
        posts = list()
        for offset in range(0, count, 100):
            posts.extend([{'text': post['text'], 'id': post['id']} for post in self._session.wall.get(owner_id=self._group_id, offset=offset, count=min(count - offset, 100))['items']])
        for post in posts:
            post['comments'] = list()
            post['comments'].extend([{'id': com['id'], 'from_id': com['from_id'], 'text': com['text']} for com in self._session.wall.getComments(owner_id=self._group_id, post_id=post['id'], count=100)['items']])
        return posts

    def close(self):
        # self._session.close()
        pass
