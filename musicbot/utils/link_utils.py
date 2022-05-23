import urllib.parse
from dataclasses import dataclass

from bs4 import BeautifulSoup

from musicbot.models.async_requests import session
from musicbot.models.async_spotify import async_spotify


@dataclass
class Song:
    """
    Class to define song data structure
    """
    name: str
    track_id: str
    url: str


class Parser:
    """
    Class to get YouTube-url to one track id in Spotify
    """
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}

    def __init__(self, track_id):
        self.session = session
        self.track_id = track_id
        self.html = None
        self._url = None

    async def get_url(self):
        """
        Get search query url on YouTube
        """
        track = await async_spotify.track(self.track_id)
        name = track.name
        author = track.artists[0].name
        year = track.album.release_date.split('-')[0]
        encoded_search = urllib.parse.quote_plus(' '.join([author, name, year]))
        self._url = 'https://www.youtube.com/results?search_query=' + encoded_search

    async def get_html(self):
        """
        Get html of YouTube page with search results
        """
        response = await self.session.get(self._url, headers=self.headers)
        await response.html.arender(sleep=1, timeout=20)
        self.html = response.html.html

    async def get_track(self) -> str:
        """
        Get final track url on YouTube
        :return: url: str
        """
        await self.get_url()
        await self.get_html()
        soup = BeautifulSoup(self.html, 'html.parser')
        result = soup.find('a', id='video-title')['href']
        return 'https://www.youtube.com' + result


class QueryProcess:
    """
    Class to process query of Spotify tracks
    """

    def __init__(self, query):
        self.query = query
        self.id = urllib.parse.urlparse(self.query).path.split('/')[2] if 'https' in self.query else None
        self._tracks, self._names, self._track_ids, self._track_urls, self.songs = [], [], [], [], []

    async def get_tracks(self):
        """
        Get info about every track in the query
        :return: tracks: list
        """
        if 'playlist' in self.query:
            self._tracks = [_.track for _ in (await async_spotify.playlist_items(self.id)).items]
        elif 'album' in self.query:
            self._tracks = [_ for _ in (await async_spotify.album_tracks(self.id)).items]
        else:
            search_result, = await async_spotify.search(self.query)
            self._tracks = [search_result.items[0]]

    async def get_songs(self):
        """
        Get info about tracks in song format that has been declared above
        """
        await self.get_tracks()

        self._names = [_.name for _ in self._tracks]
        self._track_ids = [_.id for _ in self._tracks]
        self._track_urls = [await Parser(_).get_track() for _ in self._track_ids]
        self.songs = [Song(_[0], _[1], _[2]) for _ in list(zip(self._names, self._track_ids, self._track_urls))]


class TrackProcess(QueryProcess):
    """
    Similar class to defined above but only for one track
    """
    async def get_tracks(self):
        """
        Get info about one track. Takes track id as input
        """
        self._tracks = [await async_spotify.track(self.query)]
