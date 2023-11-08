import nextcord
import os
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents) #bot instance

@client.event
async def on_ready():
    print("Ready for use.")
    print("--------------")

initial_extensions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

client.run('') #removed token for security purposes

