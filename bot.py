from discord.ext import commands

from config import *
from musicbot.audiocontroller import AudioController
from musicbot.models.memory_storage import Storage

initial_extensions = ['musicbot.commands']
bot = commands.Bot(command_prefix='!')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    """
    Creates audio controllers at start
    """
    print('started')

    for guild in bot.guilds:
        await register(guild)


@bot.event
async def on_guild_join(guild):
    """
    Creates new instance of audio controller for new guild
    :param guild: Guild
    """
    await register(guild)


async def register(guild):
    """
    Connects audio controllers and relative guilds
    :param guild: Guild
    """
    audio_controller = AudioController(bot, guild)
    await Storage.add(guild, audio_controller)


bot.run(discord_token)
