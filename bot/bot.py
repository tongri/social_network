import random

import aiohttp
import asyncio
from time import time
from conf import users_amount, max_posts_per_user, max_likes_per_user, SIGNUP_URL, OBTAIN_TOKEN_URL, POST_URL, LIKE_URL

posts_id = []
requests_amount = []


class User:
    def __init__(self, username):
        self.username = username
        self.password = username
        self.token = ''
        self.headers = {}

    def set_headers(self):
        self.headers = {'Authorization': f'Bearer {self.token}'}

    async def signup(self, session, signup_url):
        data = {'username': self.username, 'password': self.password}
        async with session.post(signup_url, data=data) as result_awaitable:
            await result_awaitable.json()
            requests_amount.append(None)

    async def get_token(self, session, login_url):
        data = {'username': self.username, 'password': self.password}
        async with session.post(login_url, data=data) as result_awaitable:
            result_jsoned = await result_awaitable.json()
            self.token = result_jsoned.get('access')
            self.set_headers()
            requests_amount.append(None)

    async def multiple_posts(self, session, post_url):
        post_creation = [self.__posts(session, post_url) for _ in range(random.randint(1, max_posts_per_user))]
        await asyncio.gather(*post_creation)

    async def __posts(self, session, post_url):
        data = {'title': f'post from {self.username}', 'text': f'text from {self.username}'}
        async with session.post(post_url, data=data, headers=self.headers) as result_awaitable:
            result_jsoned = await result_awaitable.json()
            posts_id.append(result_jsoned.get('id'))
            requests_amount.append(None)

    async def multiple_likes(self, session, like_url):
        posts_amount = len(posts_id)
        posts_to_be_liked = [random.randint(1, posts_amount-1) for _ in range(max_likes_per_user)]
        likes_creation = [self.__like(session, like_url, post_to_be_liked) for post_to_be_liked in posts_to_be_liked]
        await asyncio.gather(*likes_creation)

    async def __like(self, session, like_url, post_id):
        data = {'post': post_id}
        async with session.post(like_url, data=data, headers=self.headers) as result_awaitable:
            await result_awaitable.text()
            requests_amount.append(None)


async def tasks_factory(users, task, *args, **kwargs):
    """awaits list of tasks for user."""
    async with aiohttp.ClientSession() as session:
        tasks = [task(user, *args, **kwargs, session=session) for user in users]
        await asyncio.gather(*tasks)


async def chain():
    """chain of async tasks to be performed."""
    users = [User(i) for i in range(users_amount)]
    await tasks_factory(users, User.signup, signup_url=SIGNUP_URL)
    await tasks_factory(users, User.get_token, login_url=OBTAIN_TOKEN_URL)
    await tasks_factory(users, User.multiple_posts, post_url=POST_URL)
    await tasks_factory(users, User.multiple_likes, like_url=LIKE_URL)


if __name__ == '__main__':
    start = time()
    asyncio.run(chain())
    print(f' it costed {time() - start} seconds to make {len(requests_amount)} requests')
