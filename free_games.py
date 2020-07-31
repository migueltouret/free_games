import asyncio
import feedparser

async def rss_updater(client):

	#while(True):
	await client.wait_until_ready()
	iterator = 0
	print("start of loop: ", iterator)
	await find_channels(client)
	print("end of loop: ", iterator)
	iterator = iterator + 1
	await client.logout()
		

#//////////////////////////////////////////aux//////////////////////////


async def parse_free():
	NewsFeed = feedparser.parse("https://isthereanydeal.com/rss/specials/eu2/").entries
	free = [x for x in NewsFeed if ("[giveaway]" in x.title and "Twitch Prime" not in x.title and "IndieGala" not in x.title and "Humble Monthly Subscribers" not in x.title and "GOG Connect" not in x.title and "Humble Choice Subscribers" not in x.title)]
	free = free[::-1]
	return free

async def find_channels(client):
	guilds = []
	
	sopas = client.get_guild(152057225316270081)
	if (sopas):
		guilds.append(sopas)
	
	testchannel = client.get_guild(333689821241278465)
	if (testchannel):
		guilds.append(testchannel)
	
	for guild in guilds:
		created_channel=0
		for channel in guild.channels:
			if("free-games" in channel.name):
				created_channel=1
				await print_giveaway(channel)
				# break
		if (created_channel==0):
			#FIXME need to chech permission  manage_channels
			#channel = await guild.create_text_channel("free-games")
			#await print_giveaway(channel)
			print("channel:", guild.name, "has no free-games")

async def print_giveaway(channel):
	free = await parse_free()
	history =await channel.history(limit=None).flatten()
	clean_history = [i.content.split("\n")[1] for i in history]
	for message in free:
		await send_new(message, clean_history, channel)
	history =await channel.history(limit=None).flatten()
	await clean_old(free, history, channel)  
		


async def send_new(message, clean_history, channel):
	title = message.title[11:].strip()
	link = message.link

	

	if not(title in clean_history):
		message = "____________"  + "\n" + title + "\n" + link
		print("channel name:", channel.name)
		print(message)
		await channel.send(message)

async def clean_old(free, history, channel):
	free = [i.title[11:].strip() for i in free]
	for i in history:
		message = i.content.split("\n")
		first = message[0]
		second = message[1]
		third = message[2]
		if(first == "____________"):
			if not(second in free):
				await i.delete()
				print("channel name:", channel.name)
				print("deleted 1:" , first)
				print("deleted 2:" , second)
				print("deleted 3:" , third)
				print("\n")