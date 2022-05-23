class MemoryStorage:
    """
    Storage which contains guilds and relative audio controllers
    """
    def __init__(self):
        self._storage = {}

    async def add(self, guild, audio_controller):
        """
        Adds new pair guild-audio controller
        :param guild: Guild
        :param audio_controller: Audio controller
        """
        self._storage[guild] = audio_controller

    async def get(self, guild):
        """
        Get relative audio controller to guild
        :param guild: Guild
        :return: audio_controller: Audio controller
        """
        return self._storage[guild]


Storage = MemoryStorage()
