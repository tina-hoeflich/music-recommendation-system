import tekore as tk
def authorize():
    CLIENT_ID = "9f53ded0579d4013b7274071fc5de966"
    CLIENT_SECRET = "2771eff6282345c69e3f765472c19c22"
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)