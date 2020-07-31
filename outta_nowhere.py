# -*- encoding: utf-8 -*-
import discord
import asyncio
import logging
import sys
import os
from free_games import rss_updater


access_token= os.environ["ACCESS_TOKEN"]
logging.basicConfig(level=logging.INFO)

client = discord.Client()
voice = None
player = None

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.loop.create_task(rss_updater(client))

client.run(access_token)