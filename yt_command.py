from command import Command
import urllib.request
import re
import discord
from bs4 import BeautifulSoup
import requests

class YoutubeCommand(Command) :

    def __init__(self) :
        self.set_key("play")

    async def invoke(self, message, args) :
        await super().invoke(message, args)

        query = "+".join(args)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        for video_id in video_ids :
            print("https://www.youtube.com/watch?v=" + str(video_id))


        top_url = "https://www.youtube.com/watch?v=" + str(video_ids[0])

        print("Playing : " + top_url)
        await message.channel.send("Now playing " + top_url)
