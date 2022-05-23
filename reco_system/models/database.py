from sqlalchemy import Column, String, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

metadata = Base.metadata


class Dataset(Base):
    """
    Database class that defines the structure of 'Dataset' table
    """
    __tablename__ = 'Dataset'

    track_id = Column(String, primary_key=True)
    acousticness = Column(Float)
    danceability = Column(Float)
    energy = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    loudness = Column(Float)
    speechiness = Column(Float)
    tempo = Column(Float)
    valence = Column(Float)

    def __init__(self, track_id, acousticness, danceability, energy, instrumentalness,
                 liveness, loudness, speechiness, tempo, valence):
        self.track_id = track_id
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.tempo = tempo
        self.valence = valence


engine = create_engine("postgresql://postgres:1@localhost/spotydb")
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
