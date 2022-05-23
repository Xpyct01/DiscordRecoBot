from discord.ext import commands

from musicbot.utils.bot_utils import Misc


class Music(commands.Cog):
    """
    Main class of bot commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play')
    async def play_song(self, ctx, *, query: str):
        """
        Plays the song by given query
        :param ctx:
        :param query: str
        """
        misc = Misc(ctx)
        audio_controller = await misc.get_audio_controller()

        await misc.connect()
        await audio_controller.process_query(query)
        await ctx.send('Done!')

    @commands.command(name='loop')
    async def loop(self, ctx):
        """
        Loop the queue
        :param ctx:
        """
        audio_controller = await Misc(ctx).get_audio_controller()

        audio_controller.playlist.loop = True
        await ctx.send('Done!')

    @commands.command(name='queue')
    async def queue(self, ctx):
        """
        Show the queue
        :param ctx:
        """
        play_queue = await Misc(ctx).get_play_queue()
        names = [str(i+1)+'. '+_.name for i, _ in enumerate(play_queue)]

        msg = 'queue:\n' + '\n'.join(names)
        await ctx.send(msg)

    @commands.command(name='skip')
    async def skip(self, ctx):
        """
        Skip current track
        :param ctx:
        """
        voice = Misc(ctx).voice

        await voice.stop()
        await ctx.send('skipped')

    @commands.command(name='stop')
    async def stop(self, ctx):
        """
        Stop playing
        :param ctx:
        """
        audio_controller = await Misc(ctx).get_audio_controller()

        await audio_controller.stop_player()

    @commands.command(name='reco')
    async def reco(self, ctx):
        """
        Get sequence of proposed tracks relatively to queue
        :param ctx:
        """
        misc = Misc(ctx)
        reco_ids = await misc.get_reco_ids()
        names = [str(i + 1) + '. ' + _ for i, _ in enumerate(reco_ids.keys())]
        msg = 'Input number of track:\n' + '\n'.join(names) + '\n\n999 - cancel'

        await ctx.send(msg)
        answer = (await self.bot.wait_for('message', timeout=15)).content

        await misc.add_to_queue(reco_ids, answer)
        await ctx.send('Done!')


def setup(bot):
    bot.add_cog(Music(bot))
