import os

from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker

from reco_system.models.database import engine
from reco_system.models.reco import RecoSystem
from reco_system.utils.db_api.DfStorage import dataframe

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

DBSession = sessionmaker(bind=engine)
session = DBSession()
dataframe.launch_storage()


@app.route('/get_reco/', methods=['POST'])
def hello_world():
    """
    Produces sequence of the most appropriate tracks
    :return: json
    """
    data = request.json
    response = RecoSystem(data['queue']).get_reco()
    return jsonify({'recommendations:': response})


if __name__ == '__main__':
    app.run()
