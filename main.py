import discord
import os
import requests
import json

client = discord.Client() # connection to discord

# returns random inspirational quote with author
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

@client.event # async library
async def on_ready(): # when bot is ready do this
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message): # does something when someone sends a message, not if ourselves
    if message.author == client.user:
            return

    # for our bot we gona say that every command is a message that starts with a dollar sign
    if message.content.startswith('$inspire'): 
        quote = get_quote()
        await message.channel.send(quote)

# by default repl.it is public so secret keys are visible -> use environment variables
# line to run the bot:
client.run(os.getenv('TOKEN'))
