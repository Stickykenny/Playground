import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands.context import Context
import logging
from dotenv import load_dotenv
import os
from random import choice

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # change to daily
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

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



@bot.event
async def on_ready():
    print("Starting bot....")
    await bot.tree.sync() # Sync slash commands, also you need to allow the bot to access slash commands for it to works
    print(bot.user.name+" - Discord bot is ready and slash commands synced.")
    print()

@bot.event
async def on_message(message : discord.message.Message):
    if message.author == bot.user :
        return
    print("Message received : "+message.content)
 
    # Mandatory because we are overwriting and this instructions is missing 
    await bot.process_commands(message)

'''@bot.event
async def on_command(context : discord.ext.commands.context.Context):
    print("Command received : ")
    print(context.message.content)
    #await message.channel.send(f"Message received from {message.author.mention} - {message.content}")
 '''

@bot.event
async def on_command_error(ctx : Context, err):
    ' Command on Cooldown '
    print(err)


"""
    Classic command with prefix "!", uses Context
"""
@bot.command()
async def hello(ctx : Context):
    #await ctx.message.delete() # TODO not working
    reply_message = f"Hello {ctx.author.mention}!"
    print(reply_message)
    await ctx.reply(reply_message)

"""
Newer Command (allow autocomplete), uses Interaction
If Command takes more than 3 seconds => Discord will show "The application did not respond"
To fix this, we'll defer the response

Message to a command is by default not showing/deleted?
"""
@bot.tree.command()
async def hello(interaction: discord.Interaction):
    reply_message = f"Hello {interaction.user.mention}"
    await interaction.response.defer()
    await interaction.followup.send(reply_message)


@bot.tree.command()
@app_commands.describe(
    text='The text to repeat'
)
async def repeat(interaction: discord.Interaction, text: str):
    """Adds two numbers together."""
    await interaction.response.defer()
    await interaction.followup.send(f""+choice(emoticon_list)+" -<( "+text+" ) ~ ")

@bot.tree.command()
@app_commands.rename(first_value="a")
@app_commands.rename(second_value="b")
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.defer()
    await interaction.followup.send(f'{first_value} + {second_value} = {first_value + second_value}')


bot.run(discord_token, log_handler=handler, log_level=logging.INFO)