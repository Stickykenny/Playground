import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands.context import Context
import logging
from dotenv import load_dotenv
import os
from random import choice
import monitoring

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
command_set_separator = "-----------"


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
logger = monitoring.setup_logger()

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
    logger.info("Starting bot....")
    await bot.tree.sync() # Sync slash commands, also you need to allow the bot to access slash commands for it to works
    logger.info(bot.user.name+" - Discord bot is ready and slash commands synced.\n")


@bot.event
async def on_message(message : discord.message.Message):
    if 'tasklist-center' not in message.channel.name: return
    if message.author == bot.user :
        return
    logger.info(command_set_separator)
    logger.info("Message received : "+message.content+" by "+str(message.author.id)+"/"+message.author.name)
 
    # Mandatory because we are overwriting and this instructions is missing 
    await bot.process_commands(message)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        logger.info(command_set_separator)
        logger.info(f"Slash command used: /{interaction.data} by {interaction.user}")

'''@bot.event
async def on_command(context : Context):
    #if (context.message.content[0] != "!") : # Ignoring legacy commands
    logger.info(command_set_separator)
    logger.info("Command received : "+context.message.content)
    await bot.process_commands(message)
    #await message.channel.send(f"Message received from {message.author.mention} - {message.content}")'''

@bot.event
async def on_error(ctx : Context, err):
    logger.info("ERROR - Others")
    logger.error(err)

@bot.event
async def on_app_command_error(ctx : Context, err):
    logger.info("ERROR - App Command / Slash Command")
    logger.error(err)

@bot.event
async def on_command_error(ctx : Context, err):
    logger.info("ERROR - Prefix Command")
    logger.error(err)


"""
Classic command with prefix "!", uses Context
"""
@bot.command()
async def hello(ctx : Context):
    #await ctx.message.delete() # TODO not working
    reply_message = f"Hello {ctx.author.mention}/{ctx.author.name}!"
    logger.info(reply_message)
    await ctx.send(reply_message)
    await ctx.message.delete()

"""
Newer Command (allow autocomplete) Slash Commands, uses Interaction
If Command takes more than 3 seconds => Discord will show "The application did not respond"
To fix this, we'll defer the response

Message to a command is by default not showing/deleted?
"""
@bot.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.defer()
    reply_message = f"Hello {interaction.user.mention}/{interaction.user.name}"
    logger.info(reply_message)
    await interaction.followup.send(reply_message)


@bot.tree.command()
@app_commands.describe(
    text='The text to repeat'
)
async def repeat(interaction: discord.Interaction, text: str):
    """Adds two numbers together."""
    await interaction.response.defer()
    logger.info("Repeated : "+text)
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
    sum_display = f'{first_value} + {second_value} = {first_value + second_value}'
    logger.info(sum_display)
    await interaction.followup.send(sum_display)


bot.run(discord_token,  log_handler=None)