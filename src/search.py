from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QPixmap
import requests
import schemas
import ast
import tempfile
import json

class Search(QThread):
    
    response_received = Signal(list)
    
    def __init__(self) -> None:
        super(Search, self).__init__()
        self._search_endpoint = 'https://api.deezer.com/search?q='
        self.path = tempfile.mkdtemp()
        self._query_str = None
        
    def run(self):
        print('Working Thread')
        
        if(self._query_str != None):
            response = self.search_by_str()
            self.response_received.emit(response)
        
    def update_query(self, query_str):
        self._query_str = query_str
        
    def search_by_str(self):
        assert(self._query_str != None)
        
        self._query_str = self._query_str.replace(' ', '+')
        response = requests.get(f'{self._search_endpoint}{self._query_str}')
        
        try:
            response_dict = self.convert_to_dict(response)
        except Exception as ex:
            print(f"error {ex}")
            return None
        
        raw_response = []
        schema_response = []  
        if not 'error' in response_dict:
            if(response_dict['total'] > 0):
                for data in response_dict['data']:
                    if(data['type'] == 'track'):
                        aux = {'title': data['title'],
                            'artist': data['artist']['name'],
                            'album_title': data['album']['title'],
                            'album_cover': self.download_cover(data['album']['cover_small'], album_title=data['album']['title']),
                            'path': self.path,
                            'duration': data['duration']}
                        raw_response.append(aux)
                        
            for dict_ in raw_response:
                model = schemas.MusicSchema.parse_obj(dict_)
                schema_response.append(model)
            
            return schema_response
        
    def convert_to_dict(self, response):
        a = json.loads(response.text)
        
        return a
    
    def download_cover(self, album_cover_url, album_title):
        if(album_cover_url != None):
            r = requests.get(album_cover_url, allow_redirects=True)
            album_title = album_title.replace('/', '')
            album_title = album_title.replace(' ', '')
            save_path = f'{self.path}/{album_title}.jpg'
            open(save_path, 'wb').write(r.content)

            return QPixmap(save_path)
        else:
            # default image for no calbum cover
            return QPixmap('default_cover')
    
    
