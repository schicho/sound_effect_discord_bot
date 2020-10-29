from discord import LoginFailure
from discord.ext import commands

import soundeffectCog

bot = commands.Bot(command_prefix='!')
token = open("token.txt", "r").readline()


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.event
async def on_ready():
    print('ONLINE! {0} ({0.id})'.format(bot.user))
    print('------')


if __name__ == "__main__":
    bot.add_cog(soundeffectCog.SoundEffects(bot))
    try:
        bot.run(token)
    except LoginFailure:
        print("Error: token is not valid.\nCould not start bot.")



