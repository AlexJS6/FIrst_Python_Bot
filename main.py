import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive # To keep alive use UptimeRobot:
#https://uptimerobot.com/?gclid=Cj0KCQiAifz-BRDjARIsAEElyGIe-ehqdFkwAXevs__sCRgFQzrJs7f138ZJ7RnCj4IVPNmL85VI8f4aAprQEALw_wcB

# To add webhook on discord you need to put /github at the end of url -> application.json


client = discord.Client() # connection to discord

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing', 'cry']

starter_encouragements = [
    'Cheer up!',
    'Hang in there',
    'Your are a great person / bot!',
]

if 'responding' not in db.keys():
    db['responding'] = True

# returns random inspirational quote with author
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def update_encouragements(encouraging_message):
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(encouraging_message)
        db['encouragements'] = encouragements
    else:
        db['encouragements'] = [encouraging_message]

def delete_encouragement(index):
    encouragements = db['encouragements']
    if len(encouragements) > index:
        del encouragements[index]
        db['encouragements'] = encouragements

@client.event # async library
async def on_ready(): # when bot is ready do this
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message): # does something when someone sends a message, not if ourselves
    if message.author == client.user:
            return

    msg = message.content

    # for our bot we gona say that every command is a message that starts with a dollar sign
    if msg.startswith('$inspire'): 
        quote = get_quote()
        await message.channel.send(quote)

    if db['responding']:
        options = starter_encouragements
        if 'encouragements' in db.keys():
            options = options + db['encouragements']

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith('$new'):
        encouraging_message = msg.split('$new ', 1)[1] # splits message from $new + space
        update_encouragements(encouraging_message)
        await message.channel.send('New encouraging message added.')

    if msg.startswith('$del'):
        encouragements = []
        if 'encouragements' in db.keys():
            index = int(msg.split('$del', 1,)[1])
            delete_encouragement(index)
            encouragements = db['encouragements']
        await message.channel.send(encouragements)

    if msg.startswith('$list'):
        encouragements = []
        if 'encouragements' in db.keys():
            encouragements = db['encouragements']
        await message.channel.send(encouragements)

    if msg.startswith('$responding'):
        value = msg.split('$responding ', 1)[1] # The 1 is maxsplit

        if value.lower() == 'true':
            db['responding'] = True
            await message.channel.send('Responding is ON.')
        else:
            db['responding'] = False
            await message.channel.send('Responding is OFF.')
        
# by default repl.it is public so secret keys are visible -> use environment variables
# line to run the bot:
keep_alive()
client.run(os.getenv('TOKEN'))
