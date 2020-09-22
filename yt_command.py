from command import Command
import urllib.request
import re
import discord
from bs4 import BeautifulSoup
import requests
import youtube_dl
import os
from os import system

class YoutubeCommand(Command) :

    def __init__(self) :
        self.set_key("play")

    async def invoke(self, message, ctx, args) :
        await super().invoke(message, ctx, args)

        try :
            channel = ctx.author.voice.channel
            print("User is in channel : " + str(channel))
        except AttributeError :
            print("Error : user in not is a voice channel.")
            await ctx.send("You must be in a voice channel to use this commmand!")
            return

        await channel.connect()

        query = "+".join(args)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        for video_id in video_ids :
            print("https://www.youtube.com/watch?v=" + str(video_id))

        top_url = "https://www.youtube.com/watch?v=" + str(video_ids[0])

        print("Playing : " + top_url)
        await ctx.send("Now playing " + top_url)

        #new stuff
        vc = ctx.voice_client
        ydl_opts = {
            'max-filesize' : "20M",
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        #add remove song stuff

        song_exists = os.path.isfile("song.mp3")

        if song_exists :
            try :
                os.remove("song.mp3")

            except PermissionError :
                await ctx.send("Wait for current song to finish (this will be fixed later)")
                return

        with youtube_dl.YoutubeDL(ydl_opts) as ydl :
            ydl.download([top_url])

        for file in os.listdir("./") :
            if file.endswith(".mp3") :
                os.rename(file, "song.mp3")

        vc.play(discord.FFmpegPCMAudio("song.mp3"))
        vc.source = discord.PCMVolumeTransformer(vc.source, volume=2.0)
        vc.is_playing()


