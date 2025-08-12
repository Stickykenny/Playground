import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from random import choice

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # change to daily
intents = discord.Intents.default()
intents.message_content = True

emoticon_list = [
    "(￣▽￣)",
    "(๑>◡<๑)",
    "(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)",
    "(っ˘̩╭╮˘̩)っ"	,
    "(・_・;)"	,
     "(｡•̀ᴗ-)✧",
     "(ಠ_ಠ)",
    "(ノಠ益ಠ)ノ彡┻━┻",
    "ヽ(ヅ)ノ",
    "ಥ_ಥ",
    "(〃ω〃)",
]


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(bot.user.name+" - Discord bot is ready")

@bot.event
async def on_message(message : discord.message.Message):
    if message.author == bot.user :
        return
    print("Message received : "+message.content)
    #await message.channel.send(f"Message received from {message.author.mention} - {message.content}")
 

 # Mandatory because we are overwriting and this instructions is missing 
    await bot.process_commands(message)

@bot.command()
async def hello(ctx : discord.ext.commands.context.Context):
    print("!hello")
    await ctx.reply(f"Hello {ctx.author.mention}!")

#!repeat
@bot.command()
async def repeat(context : discord.ext.commands.context.Context,  *args):
    print("!repeat")
    await context.message.delete()
    await context.channel.send(f""+choice(emoticon_list)+" -<( "+' '.join(args)+" ) ~ "+context.author.mention)


bot.run(discord_token, log_handler=handler, log_level=logging.INFO)