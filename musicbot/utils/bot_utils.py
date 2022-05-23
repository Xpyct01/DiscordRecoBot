import json

from config import *
from musicbot.models.async_requests import session
from musicbot.models.async_spotify import async_spotify
from musicbot.models.memory_storage import Storage
from musicbot.utils.link_utils import TrackProcess


class Misc:
    """
    Class that contains necessary functions to commands
    """
    def __init__(self, ctx):
        self.voice = None
        self.ctx = ctx
        self.guild = ctx.message.guild

    async def connect(self):
        """
        Connects to user's voice channel
        """
        self.voice = self.ctx.message.guild.voice_client
        if self.voice is None or not self.voice.is_connected():
            channel = self.ctx.message.author.voice.channel
            await channel.connect()

    async def get_audio_controller(self):
        """
        Get audio controller inside 'environment'
        :return: audio_controller: Audio controller
        """
        return await Storage.get(self.guild)

    async def get_play_queue(self):
        """
        Get the playlist to relative audio controller
        :return: playlist: Playlist
        """
        audio_controller = await self.get_audio_controller()
        return audio_controller.playlist.play_queue

    async def get_reco_ids(self):
        """
        Get the sequence of the most appropriate tracks to ones in playlist.
        :return: reco_ids: dict
        """
        play_queue = await self.get_play_queue()
        track_ids = [_.track_id for _ in play_queue]

        data = {"queue": track_ids}
        response = await session.post(url=reco_url, json=data)
        dd = json.loads(response.text)

        track_names = [(await async_spotify.track(_)).name for _ in dd['recommendations:']]
        reco_ids = dict(zip(track_names, dd['recommendations:']))
        return reco_ids

    async def add_to_queue(self, reco_ids: dict, answer: str):
        """
        Add the new tracks to playlist.
        :param reco_ids: dict
        :param answer: str
        """
        track_name = list(reco_ids.keys())[int(answer) - 1]
        track_id = reco_ids[track_name]

        audio_controller = await self.get_audio_controller()
        audio_controller.playlist.add(TrackProcess(track_id))
