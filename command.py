import discord
from discord.ext import commands

class Command() :

    def set_key(self, key) :
        self.key = key

    async def invoke(self, message, args) :

        try :
            print("invoking " + str(self.key) + " with args " + str(args))
        except AttributeError :
            print("no key has been specified.")
