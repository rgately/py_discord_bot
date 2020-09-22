import discord
from discord.ext import commands
import crypto_helper
from command_list import *
from yt_command import YoutubeCommand
import json
import os


token = None
client = commands.Bot(command_prefix=".")

crypto_cmd = CryptoCommand()
m_cmd = MemeCommand()
yt_cmd = YoutubeCommand()

def main() :

    if os.path.isdir("./cache/") :
        print("Cache directory already exists.")
    else :
        print("Creating cache")
        os.mkdir("./cache")

    with open("keys.json") as keys :
        keys_json = json.load(keys)
        token = keys_json["discord_token"]
    client.run(token)

@client.event
async def on_ready() :
    print("Bot is ready.")

@commands.command()
async def crypto(ctx, *args) :
    await crypto_cmd.invoke(message = None, ctx = ctx, args = args)

@commands.command()
async def leave(ctx) :
    print("calling leave")
    await ctx.voice_client.disconnect()

@commands.command()
async def meme(ctx) :
    await m_cmd.invoke(message = None, ctx = ctx, args = None)

@commands.command()
async def play(ctx, *args) :
    await yt_cmd.invoke(message = None, ctx = ctx, args = args)

if __name__ == "__main__" :
    client.add_command(leave)
    client.add_command(crypto)
    client.add_command(meme)
    client.add_command(play)
    main()
