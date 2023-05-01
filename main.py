import discord
import configparser

from gen_string import *

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
config = configparser.ConfigParser()

config.read("gptgame.ini")
discord_key = config['api.keys']['DiscordKey']

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    channel = client.get_channel(message.channel.id)
    channel_topic = channel.topic

    if message.author == client.user:
        return
    
    if channel.topic is None or not (channel_topic.lower().startswith("gptgame=true")):
        return
    config.read_string(channel_topic.removeprefix("gptgame=true\n"))

    if message.content.startswith('>gptgame.ping'):
        await message.channel.send('du stinkst')
    
    if message.content.startswith('>gptgame.getconfig'):
        gameconfig = ""

        key_dict = {
            "deepai_gpt2":"Use GPT-2 API from DeepAI",
            "gpt4free_gpt3.5":"Use GPT-3.5 API from GPT4free",
            "openai_gpt3":"Use GPT-3 API from OpenAI",
            "nooftransformations":"Number of String Transformations",
            "noofwords":"Number of Words in given output",
            "maycontaincaseinsens":"Prompt may contain case insensitive given words",
            "maycontaincasesens":"Prompt may contain case sensitive given words"
        }

        for section in config:
            if section != 'api.keys' and section != 'DEFAULT':
                gameconfig += "[" + section + "]\n"
                for key in config[section]:
                    if key in key_dict:
                        gameconfig += key_dict[key] + ": " + config[section][key] + "\n"
                    else:
                        gameconfig += key + ": " + config[section][key] + "\n"
                gameconfig += "\n"

        await message.channel.send('**Current Game Settings:**\n' + gameconfig)

client.run(discord_key)
