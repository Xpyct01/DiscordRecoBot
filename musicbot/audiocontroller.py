import discord
import yt_dlp

from musicbot.playlist import Playlist
from musicbot.utils.link_utils import QueryProcess

from config import *


class AudioController:
    """
    Class which task is the control of sequence of the tracks
    """
    def __init__(self, bot, guild):
        self.bot = bot
        self.playlist = Playlist()
        self.current_song = None
        self.guild = guild

    async def stop_player(self):
        """
        Stop playing and clear the queue
        """
        if all([self.guild.voice_client.is_paused(), self.guild.voice_client.is_playing()])\
                or self.guild.voice_client is not None:

            self.playlist.loop = False
            self.playlist.next()
            self.playlist.play_queue.clear()
            self.guild.voice_client.stop()

    def next_song(self):
        """
        Move to next song in queue
        """
        next_song = self.playlist.next()
        self.current_song = None

        if next_song is not None:
            coro = self.play_song(next_song)
            self.bot.loop.create_task(coro)

    async def play_song(self, song_url):
        """
        Play song with YouTube url on track
        :param song_url: str
        """
        downloader = yt_dlp.YoutubeDL(
            {'format': 'bestaudio', 'title': True})
        response = downloader.extract_info(song_url, download=False)
        base_url = response.get('url')
        self.current_song = song_url

        self.guild.voice_client.play(discord.FFmpegPCMAudio(
            executable=ffmpeg_path,
            source=base_url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'),
            after=lambda e: self.next_song())
        self.guild.voice_client.source = discord.PCMVolumeTransformer(
            self.guild.voice_client.source)

        self.playlist.play_queue.popleft()

    async def process_query(self, query):
        """
        Processing input query
        :param query: str
        """
        process = QueryProcess(query)
        await process.get_songs()

        self.playlist.add(process.songs)
        if len(self.playlist) == 1:
            await self.play_song(self.playlist.play_queue[0].url)
