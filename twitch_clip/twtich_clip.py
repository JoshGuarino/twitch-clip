import requests

class TwitchClip:
    def __init__(self, client_id, client_secret, access_token):
        self.main_path = 'https://api.twitch.tv/helix/'
        self.oauth2_path = 'https://id.twitch.tv/oauth2/'
        self.root_path = os.getcwd()
        self.client_id = client_id
        self.clips = None
        self.game = None
        self.client_secret = client_secret
        self.access_token = access_token

    def get(self):
        
    def post(self):

    def acquire_access_token(self):

    def check_token_valid(self):

    def revoke_access_token(self):

    def download_clips(self):

    def get_clips(self, date, game_id, num_of_clips): 