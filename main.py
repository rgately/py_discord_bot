import discord
from discord.ext import commands
import crypto_helper
from command_list import *
from yt_command import YoutubeCommand
import json


token = None
client = commands.Bot(command_prefix=".")

m_cmd = MemeCommand()
yt_cmd = YoutubeCommand()

def main() :

    with open("keys.json") as keys :
        keys_json = json.load(keys)
        token = keys_json["discord_token"]
    client.run(token)

@client.event
async def on_ready() :
    print("Bot is ready.")

@commands.command()
async def leave(ctx) :
    print("calling leave")
    await ctx.voice_client.disconnect()

@client.event
async def on_message(message) :
    if not message.author.bot :
        if message.content[0] == "." :
            print("received message from " + str(message.author.id) + ": \"" + message.content + "\"")
            txt = message.content[1:]

            split = txt.split(" ")
            cmd = split[0]
            args = split[1:]

            if cmd == "hello" :
                await message.channel.send("hi, " + message.author.display_name)
            elif cmd == "crypto" :
                await CryptoCommand().invoke(message = message, args = args)
            elif cmd == "exit" :
                exit(0)
            elif cmd == "meme" :
                await m_cmd.invoke(message = message, args = args)
            elif cmd == "play" :
                await yt_cmd.invoke(message = message, args = args)
            elif cmd == "embed" :
                embed = discord.Embed(title= "", description = "", color = discord.Color.blue(), url="")
                embed.set_image(url="https://i.redd.it/mc273lxrwio51.jpg")
                await message.channel.send(embed = embed)


if __name__ == "__main__" :
    client.add_command(leave)
    main()
