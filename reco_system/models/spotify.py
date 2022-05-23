from config import *
import tekore as tk

app_token = tk.request_client_token(client_id, client_secret)

spotify = tk.Spotify(app_token)
