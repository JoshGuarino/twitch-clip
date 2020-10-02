import requests
import os
# from urllib import HTTPError
from pprint import pprint

class TwitchClip:
    '''
    A class used to find and download clips from twitch.tv

    ...

    Attributes
    ----------
    main_path : str
    oauth2_path : str
    root_path : str
    clips : list
    game : int
    client_id : str
    client_secret : str
    access_token : str

    Methods
    -------

    
    '''
    def __init__(self, client_id, client_secret, access_token=None):
        self.main_path = 'https://api.twitch.tv/helix/'
        self.oauth2_path = 'https://id.twitch.tv/oauth2/'
        self.root_path = os.getcwd()
        self.clips = None
        self.game = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

        #Acquire access token if no access token is given.
        if self.access_token == None:
            self.acquire_access_token()


    def __get(self, url, payload, headers):
        '''
        Generic GET handler.
        '''
        try:
            response = requests.get(url, params=payload, headers=headers)
            if response.status_code == 200:
                pprint(response.text)
                return response.json()
            if response.status_code == 401:
                pprint(response.text)
                return response.json()
        except requests.HTTPError as error:
            raise SystemExit(error)


    
    def __post(self, url, payload, headers):
        '''
        Generic POST handler.
        '''
        try:
            response = requests.post(url, params=payload, headers=headers)
            if response.status_code == 200:
                if response.text == '':
                    return
                pprint(response.text)
                return response.json()
            if response.status_code == 401:
                pprint(response.text)
                return response.json()
        except requests.HTTPError as error:
            raise SystemExit(error)


    def acquire_access_token(self):
        '''
        '''
        url = f'{self.oauth2_path}token'
        payload = { 'client_id':self.client_id, 'client_secret':self.client_secret, 'grant_type':'client_credentials' }
        data = self.__post(url, payload, {})
        pprint(data)
        self.access_token = data['access_token']
        return


    def check_token_valid(self):
        '''
        '''
        url = f'{self.oauth2_path}validate'
        headers = { 'Authorization' : f'Bearer {self.access_token}' }
        print(f'Checking validity of token: {self.access_token}')
        data = self.__get(url, {}, headers)
        print('Token is valid.')
        return


    def revoke_access_token(self):
        '''
        '''
        url = f'{self.oauth2_path}revoke'
        payload = { 'client_id':self.client_id, 'token':self.access_token }
        print(f'Revoking access token: {self.access_token}')
        data = self.__post(url, payload, {})
        print(f'Successfully revoked access token: {self.access_token}')
        return


    def __download_clips(self, clips):
        '''
        '''
        clips_url = f'{self.root_path}/clips/'
        if not os.path.exists(clips_url):
            os.makedirs(clips_url)
        for clip in progressbar.progressbar(clips, prefix='Downloading clips: '):
            down_url = f'{clip["thumbnail_url"][0:-20]}.mp4'
            out_path = f'{clips_url}{clip["video_id"]}.mp4'
            response = requests.__get(down_url, stream=True)
            with open(out_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file) 
        return


    def get_clips(self, date, game_id, num_of_clips):
        '''
        '''
        url = f'{self.main_path}clips'
        headers = { 'Authorization' : f'Bearer {self.access_token}', 'Client-ID' : self.client_id }
        payload = { 'started_at':date, 'game_id': game_id, 'first':num_of_clips }
        data = self.__get(url, payload, headers)
        self.__download_clips(data['data'])
        return
        
        
