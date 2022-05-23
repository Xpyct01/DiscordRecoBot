import pandas as pd

from reco_system.models.database import engine


class DF:
    """
    DataFrame storage is used to fast manage sample in RAM
    """
    def __init__(self):
        self.df = None

    def launch_storage(self):
        """
        Open dataframe from SQL table
        """
        self.df = pd.read_sql('Dataset', con=engine)

    def add_item(self, data):
        """
        Add new item to dataframe
        :param data: dict
        """
        self.df = self.df.append(data, ignore_index=True)


dataframe = DF()
