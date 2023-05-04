#!/usr/bin/python3
import discord
import configparser

from gen_string import gen_string
from gpt_api import gpt_generate

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
config = configparser.ConfigParser()

game_started = 0
given = ""

config.read("gptgame.ini")
discord_key = config['api.keys']['DiscordKey']

def check_substrings(given_output, string, case_sensitive):
    words = given_output.split()

    if not case_sensitive:
        string = string.lower()

    for word in words:
        if not case_sensitive:
            word = word.lower()

        if word + " " in string or " " + word in string:
            return True

    return False

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
        await message.channel.send('pong')

    if message.content.startswith('>gptgame.help'):
        help = """>gptgame.help  -  Print this help
        >gptgame.ping  -  Ping the bot
        >gptgame.printconfig  -  Print current game settings
        >gptgame.genstring  -  Generate test string
        >gptgame.start  -  Start new game
        >gptgame.reset  -  Restart bot (only when game is running)
        """

        embed = discord.Embed(description=help,color=discord.Color.dark_magenta())
        await message.channel.send("Available commands:", embed=embed)
    
    if message.content.startswith('>gptgame.printconfig'):
        global game_started
        gameconfig = ""

        key_dict = {
            "api":"API used",
            "nooftransformations":"Number of string transformations",
            "noofwords":"Number of words in given output",
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

        if game_started == 0:
            game_running = "No"
        else:
            game_running = "Yes"

        embed = discord.Embed(description=gameconfig,color=discord.Color.dark_purple())
        await message.channel.send('**Game running:** ' + game_running + '\n\n**Current game settings:**\n', embed=embed)

    if message.content.startswith('>gptgame.genstring'):
        global given
        given = gen_string(int(config['difficulty.settings']['NoOfWords']), int(config['difficulty.settings']['NoOfTransformations']))
        embed = discord.Embed(description=given,color=discord.Color.gold())
        await message.channel.send("**Test string:**", embed=embed)

    if message.content.startswith('>gptgame.start'):
        if game_started == 0:
            given = gen_string(int(config['difficulty.settings']['NoOfWords']), int(config['difficulty.settings']['NoOfTransformations']))
            embed = discord.Embed(description=given,color=discord.Color.gold())
            await message.channel.send("**Started a new game. Make GPT output this:**", embed=embed)
        
            print("game started")
            game_started = 1

        else:
            await message.channel.send("Game already running. Use `>gptgame.reset` to restart.")

    if message.content.startswith('>gptgame.reset') and game_started == 1:
        print("game reset")
        game_started = 0
        await message.channel.send("Game reset.")

    if not message.content.startswith('>gptgame') and game_started == 1:
        allowed = True

        if config["difficulty.settings"]["MayContainCaseInsens"] == "no" or config["difficulty.settings"]["MayContainCaseSens"] == "no":
            if config["difficulty.settings"]["MayContainCaseSens"] == "no":
                conf_insens = True
            else:
                conf_insens = False

            allowed = not check_substrings(given, message.content, conf_insens) 

        if allowed:
            generated = gpt_generate(message.content)
            if generated == given:
                game_started = 0
                embed = discord.Embed(description=generated,color=discord.Color.green())
                await message.channel.send(f'Success! <@{message.author.id}> scored a match with a {len(message.content)} character long prompt. Use `>gptgame.start` to play again.', embed=embed)
            else:
                embed = discord.Embed(description=generated,color=discord.Color.red())
                await message.channel.send(f'The generated output did not match the given string. Your prompt was {len(message.content)} characters long.', embed=embed)
        else:
            await message.channel.send(":rotating_light: Your prompt contains one or more word(s) that are part of the given string. Try again.")    

client.run(discord_key)
