# Intro


### WHY ?
> **I keep using the Note app on mobile but I never check it later, so why not use it on Discord (an app that I use daily)**

This is a small tests for a Discord bot in Python


Has
Python venv Virtual Environment




### Some commands

Create a venv called "venv"
python -m venv venv

Activate it (backslash important)
venv\Scripts\activate
deactivate

save requirements
pip freeze > requirements2.txt
pip install -r requirements2.txt


All prefix command errors go through on_command_error
All slash command errors go through on_app_command_error
Any other exceptions in events go through on_error

### Various ressources used

Setup discord bot
https://discord.com/developers/applications/

python library docs
https://discordpy.readthedocs.io/en/stable/
https://discordpy.readthedocs.io/en/stable/api.html?highlight=textchannel#discord.TextChannel.history 


Run the bot along-side an api
https://makubob.medium.com/combining-fastapi-and-discord-py-9aad07a5cfb6    


> Error "The application did not respond"
> Discord timeout if the commands takes too long > needs to defer
> https://www.reddit.com/r/Discord_Bots/comments/1j2g20i/problem_with_the_application_did_not_respond/


