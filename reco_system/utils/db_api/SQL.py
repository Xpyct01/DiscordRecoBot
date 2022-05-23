from reco_system.models.database import Dataset, session


def add_track(data):
    """
    Add new data to SQL table
    :param data: dict
    """
    session.add(Dataset(track_id=data['track_id'],
                        acousticness=data['acousticness'],
                        danceability=data['danceability'],
                        energy=data['energy'],
                        instrumentalness=data['instrumentalness'],
                        liveness=data['liveness'],
                        loudness=data['loudness'],
                        speechiness=data['speechiness'],
                        tempo=data['tempo'],
                        valence=data['valence']))
    session.commit()
