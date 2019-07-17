import os
import json
import random
import asyncio
import logging
from discord.ext import commands


data_file = 'data.json'

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
log.addHandler(handler)


def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']
    return base


class Synonym(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, case_insensitive=True, description=None)
        self.log = log
        self.bg_task = self.loop.create_task(self.background_task())


    async def on_ready(self):
        self.log.info(f'Ready: {self.user} (ID: {self.user.id})')


    async def background_task(self):
        while not self.is_ready():
            await asyncio.sleep(1)
        while not self.is_closed():
            await self.change_nickname()
            rand_hour = random.randint(5,24)
            sleep_time = rand_hour * 3600 # turn the number into hours
            self.log.info(f"Sleeping for {rand_hour} hours before executing again")
            await asyncio.sleep(sleep_time)


    async def change_nickname(self):
        guild_id = os.environ['GUILD_ID']
        user_id = os.environ['USER_ID']

        guild = self.get_guild(int(guild_id))
        member = guild.get_member(int(user_id))

        with open(data_file) as f:
            dictionary = json.load(f)
            words = dictionary['nouns']
            total_words = len(words)
            word_number = random.randint(0, total_words-1)
            new_nickname = words[word_number]
        del dictionary
        del words

        try:
            await member.edit(nick=new_nickname)
        except Exception as e:
            self.log.error(e)


if __name__ == "__main__":
    token = os.environ['CLIENT_TOKEN']
    bot = Synonym()
    bot.run(token)
