from discord.ext import commands
from main_cog import main_cog
from music_cog import music_cog

bot = commands.Bot(command_prefix = '?')

bot.remove_command('help')

bot.add_cog(main_cog(bot))
bot.add_cog(music_cog(bot))

TOKEN = "ODk2ODA4NzcxNjkzNzIzNjU5.YWMgQQ.2XYJ9SqsRq1Jd1zmU_Oup2IPHM0"
bot.run(TOKEN)
