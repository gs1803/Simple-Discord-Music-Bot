import discord
from discord.ext import commands

class main_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
?help - displays all the available commands
?dc - will disconnect the bot and end the program

Music commands:
?play <keywords> - finds the song on youtube and plays it in your current channel
?pause - pauses the song thats currently playing
?resume - resumes the song that was paused
?stop - stops the current song
?queue - displays the current music queue
?remove - removes the most recent song from queue
?clear - removes all songs from the queue
?skip - skips the current song being played
?loop - loops the current song (use clear to end the loop)
```
"""

    @commands.command(name = "help", help = "Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    @commands.command(name = "dc", help = "Disconnects the bot")
    async def dc(self, ctx):
        await ctx.voice_client.disconnect()
        exit()
