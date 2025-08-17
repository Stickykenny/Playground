import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands.context import Context
from dotenv import load_dotenv
import os
from random import choice
import monitoring

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
command_set_separator = "-----------"
DISCORD_CHAR_LIMIT = 2000
DISCORD_RATE_LIMIT_DELAY = 3


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
logger = monitoring.setup_logger()

anchor = """
==========TASKLIST==========
"""

emoticon_list = [
    "(￣▽￣)",
    "(๑>◡<๑)",
    "(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)",
    "(っ˘̩╭╮˘̩)っ",
    "(・_・;)",
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
    # Sync slash commands, also you need to allow the bot to access slash commands for it to works
    await bot.tree.sync()
    logger.info(bot.user.name +
                " - Discord bot is ready and slash commands synced.\n")


@bot.event
async def on_message(message: discord.message.Message):
    if 'tasklist-center' not in message.channel.name:
        return
    if message.author == bot.user:
        return
    logger.info(command_set_separator)
    logger.info("Message received : " + message.content + " by " +
                str(message.author.id) + "/" + message.author.name)

    # Mandatory because we are overwriting and this instructions is missing
    await bot.process_commands(message)


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        logger.info(command_set_separator)
        logger.info(
            f"Slash command used: /{interaction.data} by {interaction.user}")


@bot.event
async def on_error(ctx: Context, err):
    logger.info("ERROR - Others")
    logger.debug(type(err))
    logger.error(err)


@bot.event
async def on_app_command_error(ctx: Context, err):
    logger.info("ERROR - App Command / Slash Command")
    logger.debug(type(err))
    logger.error(err)


@bot.event
async def on_command_error(ctx: Context, err):
    logger.info("ERROR - Prefix Command")
    logger.debug(type(err))
    logger.error(err)


"""
Classic command with prefix "!", uses Context
"""


@bot.command()
async def hello(ctx: Context):
    # await ctx.message.delete() # TODO not working
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
    """Repeat"""
    await interaction.response.defer()
    repeat_reponse = f"" + choice(emoticon_list) + " -<( " + text + " ) ~ "
    if (len(repeat_reponse) > 1900):
        logger.info("Didn't repeat (too long) : " + text)
        await interaction.followup.send(f"Can't repeat this (too long)")
        return
    logger.info("Repeated : " + repeat_reponse)
    await interaction.followup.send(repeat_reponse)


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


@bot.tree.command()
async def update(interaction: discord.Interaction):
    """Update the current tasklist
    This process will autostart on launch"""
    await interaction.response.defer()
    channel = interaction.channel
    invalid_instructions = []

    messages = []
    # Default history fetch from earliest to oldest
    async for message in channel.history():
        messages.append(message)
    messages = messages[::-1]
    for message in messages:
        print("---------------")
        # Clean up Slash Commands Response in channel
        if message.type.name == discord.MessageType.chat_input_command.name:
            logger.info("Deleting Slash command response :" + str(message.content))
            # await asyncio.sleep(3)
            await message.delete(delay=DISCORD_RATE_LIMIT_DELAY)  # Delay to avoid rate limit

        else:
            print(message.type)
            print(message.content)

            # Instruction fetching
            instruction = message.content.split(" ")[0]
            match instruction:
                case "!add":
                    break
                case "!complete":
                    break
                case "!remove":
                    break
                case "!update":
                    break
                case _:
                    logger.info("Invalid Instruction ! - " + message.content)
                    invalid_instructions.append(message)
                    await message.delete(delay=DISCORD_RATE_LIMIT_DELAY)  # Delay to avoid rate limit

    await interaction.followup.send(anchor + "\nHey here's the current tasklist")


bot.run(discord_token, log_handler=None)
