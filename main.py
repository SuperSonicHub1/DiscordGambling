import discord
import os
import random
import json
import logging
logging.basicConfig(level=logging.INFO)
from keep_alive import keep_alive

# Allow for the use of multiple commands; the last two have spaces to fight against mobile autocorrect.
gambl = ["!gambl", "!gamble"]

with open('logbook.json') as f:
    logbook = json.load(f)


# Actual code starts here.
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        # Custom status.
        activity = discord.Activity(
            name='!gamble', type=discord.ActivityType.listening)
        await client.change_presence(activity=activity)

    async def on_message(self, message):
        # Don't respond to ourselves.
        if message.author == self.user:
            return

        # Stops bot from being spammed throughout the server.
        if str(message.channel) != "virtual-gambling":
            return

        # Creates a profile for a first-time user.

        try:
            print(logbook[message.author.name])
        except KeyError:
            logbook[message.author.name] = {
                'credits': 0,
                'wins': 0,
                'losses': 0
            }

        answer = message.content.split()

        # Shows stats.

        if answer[0].casefold() in gambl and "stats" in answer[1].casefold():
            await message.channel.send(
                "Name: {0} \n Credits: {1} \n Wins: {2} \n Losses: {3}"
                .format(
                    message.author.name,
                    logbook[message.author.name]['credits'],
                    logbook[message.author.name]['wins'],
                    logbook[message.author.name]['losses']))

        # Processes input, does the gambling stuff, sends a message, and processes the stats.
        if answer[0].casefold() in gambl:
            rnjesus = random.randrange(1, 100)
            answer = int(answer[1])
            miss = abs(answer - rnjesus)
            if miss == 0:
                await message.channel.send("You guessed correctly!")
                logbook[message.author.name]['wins'] = logbook[
                    message.author.name]['wins'] + 1
                logbook[message.author.name]['credits'] = logbook[
                    message.author.name]['credits'] + (rnjesus * 2)
            elif miss <= 10:
                await message.channel.send(
                    "You got real close! You guessed {0}. The correct answer is {1}. You were {2} off."
                    .format(answer, rnjesus, miss))
                logbook[message.author.name]['losses'] = logbook[
                    message.author.name]['losses'] + 1
                logbook[message.author.name]['credits'] = logbook[
                    message.author.name]['credits'] - miss
            else:
                await message.channel.send(
                    "You guessed {0}. The correct answer is {1}. You were {2} off."
                    .format(answer, rnjesus, miss))
                logbook[message.author.name]['losses'] = logbook[
                    message.author.name]['losses'] + 1
                logbook[message.author.name]['credits'] = logbook[
                    message.author.name]['credits'] - miss

        with open('logbook.json', 'w') as outfile:
            json.dump(logbook, outfile)


client = MyClient()
keep_alive()
client.run(os.environ.get("DISCORD_BOT_SECRET"))
