import asyncio
import random
from os import listdir
from os.path import isfile, join

import discord
from discord.ext import commands


class SoundEffects(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def se(self, ctx, name=None):
        """
        Play a sound effect with the command !se to play a random sound effect.
        You can also call !se <name> to play a specific sound effect.
        """

        files = [f for f in listdir("soundeffects/") if isfile(join("soundeffects/", f))]

        if name is not None:
            files = list(filter(lambda string: name in string, files))
        if len(files) == 0:
            await ctx.send("Can't find the sound effect you asked for!")
            return

        sound_file = "soundeffects/" + random.choice(files)
        print("Playing", sound_file, "for user", ctx.author)
        audio_source = discord.FFmpegPCMAudio(sound_file)

        ctx.voice_client.play(audio_source)


    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        print("Leaving voice channel.")
        await ctx.voice_client.disconnect()

    @se.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
