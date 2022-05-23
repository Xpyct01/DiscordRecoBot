import numpy as np
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler

from reco_system.models.spotify import spotify
from reco_system.utils.db_api.SQL import add_track
from reco_system.utils.db_api.DfStorage import dataframe


class RecoSystem:
    """
    Main recommendation class
    """

    feature_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                       'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

    def __init__(self, queue):
        self.queue = queue

    @staticmethod
    def get_song_data(track_id):
        """
        Get song data of the track
        :param track_id:
        :return: song_data: list
        """
        song_data = spotify.track_audio_features(track_id)
        arr = np.array([song_data.acousticness,
                        song_data.danceability,
                        song_data.energy,
                        song_data.instrumentalness,
                        song_data.liveness,
                        song_data.loudness,
                        song_data.speechiness,
                        song_data.tempo,
                        song_data.valence])

        return arr

    def get_song_list(self):
        """
        Get song data from a couple of tracks and mean vector of given songs
        :return: song_data: list
        :return: mean_song: list
        """
        song_vector = []
        for song in self.queue:
            song_features = self.get_song_data(song)
            song_vector.append(song_features)

        song_data = dict(zip(self.queue, song_vector))
        mean_song = np.mean(np.array([song_vector]), axis=0)
        return song_data, mean_song

    def get_reco(self):
        """
        Get top-10 the most appropriate tracks
        :return: recommendations: list
        """
        song_data, mean_song = self.get_song_list()
        song_ids = song_data.keys()

        for song_id in song_ids:
            if song_id not in dataframe.df['track_id'].values:
                # checks whether we have songs from queue in our database and adds if not
                data = dict(zip(self.feature_columns, song_data[song_id]))
                data['track_id'] = song_id
                add_track(data)
                dataframe.add_item(data)

        reco_df = dataframe.df.copy()
        temp_df = reco_df.iloc[:, 1:].copy()  # iloc[:, 1:] is used to select all features except track_id
        new_df = StandardScaler().fit_transform(temp_df.values)
        reco_df.iloc[:, 1:] = new_df

        bad_df = reco_df['track_id'].isin(song_ids)
        reco_df = reco_df[~bad_df]

        distances = cdist(mean_song, reco_df.iloc[:, 1:], 'correlation')
        indexes = list(np.argsort(distances)[:, :10][0])
        rec_songs = reco_df['track_id'].iloc[indexes]

        return rec_songs.tolist()
