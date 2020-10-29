import asyncio
import random
from os import listdir
from os.path import isfile, join

import discord
from discord.ext import commands


class SoundEffects(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def play_sound_effect(self, ctx, soundeffect):
        # channel the caller is in
        channel = ctx.message.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

        audio_source = discord.FFmpegPCMAudio(soundeffect)

        ctx.voice_client.play(audio_source)
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        await ctx.voice_client.disconnect()

    """
    Play a sound effect with the command !se to play a random sound effect.
    You can also call !se <name> to play a specific sound effect.
    """

    @commands.command()
    async def se(self, ctx, name=None):
        if ctx.message.author.voice is None:
            await ctx.send("You are not connected to a voice-channel!")
            return

        files = [f for f in listdir("soundeffects/") if isfile(join("soundeffects/", f))]

        if name is not None:
            files = list(filter(lambda string: name in string, files))
        if len(files) != 0:
            await self.play_sound_effect(ctx, "soundeffects/" + random.choice(files))
        else:
            await ctx.send("Can't find the sound effect you asked for!")

    """Stop the bot while playing the sound effect."""

    @commands.command()
    async def stop(self, ctx):
        try:
            await ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
        # stopping throws an exception, can't figure out why, probably the wrong context?
        # nevertheless this still works as intended.
        except Exception:
            pass
