from collections import deque


class Playlist:
    """
    Class to manage the playlist
    """
    def __init__(self):
        self.play_queue = deque()

        self.loop = False

    def __len__(self):
        """
        Get length of queue
        :return:
        """
        return len(self.play_queue)

    def add(self, tracks):
        """
        Add new tracks to queue
        :param tracks: list
        """
        self.play_queue.extend(tracks)

    def next(self):
        """
        Move to next track in queue
        """
        if self.loop:
            self.play_queue.appendleft(self.play_queue[-1])

        return self.play_queue[0].url if len(self.play_queue) != 0 else None
