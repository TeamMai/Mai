"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import aiofiles
import asyncpraw
import asyncio
import pickle
import random

from discord.ext import tasks
from typing import List, Tuple


from asyncpraw import Reddit
from asyncpraw.models import Submission, Subreddit


from config.ext.parser import config


class RedditPostCacher:
    def __init__(self, subreddit_names: List[str], cache_location):
        self.subreddit_names = subreddit_names
        self.bot_name = config["BOT_NAME"]

        self.reddit = Reddit(
            client_id=config["PRAW_ID"],
            client_secret=config["PRAW_SECRET"],
            user_agent=f"{self.bot_name}/0.5",
        )

        self.file_path = cache_location

    async def cache_subreddit(
        self, subreddit: Subreddit
    ) -> Tuple[str, List[str]]:
        """Caches top posts from a subreddit
        Parameters
        ----------
        subreddit : Subreddit
            The subreddit to cache posts from
        Returns
        -------
        Tuple[str, List[str]]
            A tuple of subreddit name and list of post URLs
        """
        await subreddit.load()
        post_urls = [post.url async for post in subreddit.hot(limit=50)]
        allowed_extensions = (".gif", ".png", ".jpg", ".jpeg")
        post_urls = list(
            filter(
                lambda i: any(i.endswith(e) for e in allowed_extensions),
                post_urls,
            )
        )
        return (subreddit.display_name, post_urls)

    @tasks.loop(minutes=30)
    async def cache_posts(self) -> None:
        subreddits = [
            await self.reddit.subreddit(subreddit)
            for subreddit in self.subreddit_names
        ]
        tasks = tuple(
            self.cache_subreddit(subreddit) for subreddit in subreddits
        )
        all_sub_content = await asyncio.gather(*tasks)
        data_to_dump = dict(all_sub_content)

        async with aiofiles.open(self.file_path, mode="wb+") as f:
            await f.write(pickle.dumps(data_to_dump))

    async def get_random_post(self, subreddit: str) -> Submission:
        """Fetches a post from the internal cache
        Parameters
        ----------
        subreddit : str
            The name of the subreddit to fetch from
        Returns
        -------
        asyncpraw.models.Submission
            The randomly chosen submission
        Raises
        ------
        ValueError
            The subreddit was not in the internal cache
        """
        async with aiofiles.open(self.file_path, mode="rb") as f:
            cache = pickle.loads(await f.read())
            try:
                subreddit = cache[subreddit]
            except KeyError as e:
                raise ValueError("Subreddit not in cache!") from e
            else:
                random_post = random.choice(subreddit)
                return random_post
