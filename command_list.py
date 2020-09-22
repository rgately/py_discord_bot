from command import Command
import crypto_helper
import requests
import json
import pandas
import praw
import random

class CryptoCommand(Command) :

    def __init__(self) :
        self.set_key("crypto")

    async def invoke(self, message, ctx, args) :
        await super().invoke(message, ctx, args)

        response = crypto_helper.get_price(args[0])

        print("User requested crypto price \"" + str(args[0]) + "\" : " + str(response))

        if response == -1 :
            print("Currency not found.")
            await ctx.send("That currency is not available or does not exist")
            return

        await ctx.send(str(args[0]) + " : " + str(response))

class ExitCommand(Command) :

    def __init__(self) :
        self.set_key("exit")

    async def invoke(self, message, ctx, args) :
        await super().invoke(message, ctx, args)
        exit(0)

#class LeaveCommand(Command) :

    #def __init__(self) :
        #self.set_key("disconnect")

    #async def invoke(self, message, args) :


class MemeCommand(Command) :

    client_id = None
    client_secret = None
    user_agent = None
    path = "reddit_sources.txt"

    def __init__(self) :
        self.set_key("meme")

        with open("keys.json") as keys :
            keys_json = json.load(keys)
            self.client_id = keys_json["reddit_client_id"]
            self.client_secret = keys_json["reddit_client_secret"]
            self.user_agent = keys_json["reddit_user_agent"]

        self.reddit = praw.Reddit(client_id = self.client_id, client_secret = self.client_secret, user_agent = self.user_agent)
        self.cache = []

        with open(self.path) as subreddit_list :
            lines = subreddit_list.readlines()
            self.subreddits = {line.rstrip():self.reddit.subreddit(line.rstrip()) for line in lines if not line == "\n"}

        self.pre_cache(num_posts = 50)

    def pre_cache(self, num_posts) :
        self.cache.clear()
        print("Precaching...")

        for name, subreddit in self.subreddits.items() :
            posts = subreddit.hot(limit = num_posts)
            for post in posts :
                if "i.redd.it" in post.url :
                    self.cache.append(post.url)
        print("Cache length is " + str(len(self.cache)))

    async def invoke(self, message, ctx, args) :
        await super().invoke(message, ctx, args)

        if len(self.cache) == 0 :
            self.pre_cache(num_posts = 50)

        meme = random.choice(self.cache)
        print("Sending meme : " + str(meme))
        self.cache.remove(meme)
        print("Cache length is now " + str(len(self.cache)))

        await ctx.send(meme)

