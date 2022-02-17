from PySide6.QtCore import QThread, Signal, QSize
from PySide6.QtGui import QPixmap
import pydantic
import aiohttp
import aiofiles
import asyncio
import schemas
import os
import tempfile
import json
import utils

#TODO
# too long process

async def fetch(session, endpoint, id=None, download=False, download_data=None):
    try:
        if not download:
            async with session.get(endpoint) as response:
                if(id != None):
                    return  {'response': await response.text(),
                            'id': id}
                else:
                    return await response.text()
        else:
            if not (os.path.isfile(download_data['save_path'])):
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        f = await aiofiles.open(download_data['save_path'], mode='wb')
                        await f.write(await response.read())
                        await f.close()
                        return download_data
                
    except Exception as ex:
        return {'status_code': 500,
               'error': 'Error on fetch request'}


async def make_request(*args):
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        task = [fetch(session=session, **args[i])
                for i in range(len(args))]
        return await asyncio.gather(*task)


class Search(QThread):
    
    response_received = Signal(dict)
    
    def __init__(self) -> None:
        super(Search, self).__init__()
        self._search_endpoint = 'https://api.deezer.com/search?q='
        self._search_playlist_endpoint = 'https://api.deezer.com/search/playlist?q='
        self.path = tempfile.mkdtemp()
        self._query_str = None
        
    def run(self):
        print('Working Thread')
        data =  asyncio.run(make_request(*self._request))
        response_tracks, response_playlist = None, None
        
        for response in data:
            if not 'error' in response:
                response = self._convert_to_dict(response)
                if(response['total'] > 0):
                    if(response['data'][0]['type'] == 'track'):
                        response_tracks = response
                    else:
                        response_playlist = response
        
        try:                
            valid_track_schema = self._validate_tracks_response(response_tracks, download_cover=True)
            valid_playlist_schema = self._validate_playlist_response(response_playlist)

            self.response_received.emit({'tracks': valid_track_schema,
                                         'playlists': valid_playlist_schema})
        except Exception as ex:
            # emit signal to error
            self.response_received.emit({'tracks': [],
                                         'playlists': []})      
        
    def update_query(self, query_str):
        self._query_str = query_str.replace(' ', '+')
        self._request = [{'endpoint': f'{self._search_endpoint}{self._query_str}'}, 
                         {'endpoint': f'{self._search_playlist_endpoint}{self._query_str}'}]
        
    def _validate_tracks_response(self, response: dict, download_cover: bool = True):
        assert(response != None and type(response) == dict)
        
        schema_response = []  
        if not 'error' in response:
            if(response['total'] > 0):
                for data in response['data']:
                    if(data['type'] == 'track'):
                        aux = {'id': data['id'],
                            'title': data['title'],
                            'artist': data['artist']['name'],
                            'album_title': data['album']['title'],
                            'path': self.path,
                            'duration': data['duration']}
                        
                        try:  
                            aux['album_cover_url'] =  data['album']['cover_small'] if type(data['album']['cover_small']) != tuple\
                                                        else data['album']['cover_small'][0]
                            aux['album_cover_playlist_url'] =  data['album']['cover_medium']
                        except KeyError:
                            # not cover for this track
                            pass
                        try:
                            schema_response.append(schemas.MusicSchema.parse_obj(aux))
                        except pydantic.error_wrappers.ValidationError as error:
                            print(error, '\n', aux['album_cover_url'])
                            
                        
            if(download_cover):
                for schema in schema_response:
                    schema.album_cover = utils.download_cover(self, schema.album_cover_url, 
                                                        schema.album_title)
                
                # async download images, i dont know why but even 
                # async aiohttp take more time
                # to write the content on disk, maybe aiofiles isnt foog enought
                # ll keep request sync for now
                 
                #request = []
                #for schema in schema_response:
                #    if schema.album_cover_url != None:
                #        aux = schema.album_title.replace('/', '')
                #        aux = schema.album_title.replace(' ', '')
                #        request.append({'endpoint': schema.album_cover_url,
                #                       'download': True,
                #                       'download_data': {'id': schema.id,
                #                                        'save_path': f'{self.path}/{aux}.jpg'}})
                #
                #data =  asyncio.run(make_request(*request))
                #
                #
                #for response in data:
                #    if type(response) != None:
                #        print(response)
                #        if not 'error' in response:
                #            for schema in schema_response:
                #                if schema.id == response['id']:
                #                    schema.album_cover = QPixmap(response['save_path'])
                
            return schema_response
    
    def _validate_playlist_response(self, response):
        assert(response != None and type(response) == dict)
        
        schema_response = []
        if not 'error' in response:
            if(response['total'] >= 10):
                for i in range(10):
                    schema_response.append(schemas.PlaylistSchema.parse_obj(
                                                            response['data'][i]))
            else:
                for data in response['data']:
                    schema_response.append(schemas.PlaylistSchema.parse_obj(data))

            if(schema_response != None):
                request = []
                for schema in schema_response:
                    request.append({'endpoint': f'https://api.deezer.com/playlist/{schema.id}',
                                    'id': schema.id})
                    
                data = asyncio.run(make_request(*request))
                
                for response in data:
                    if not 'error' in response:
                        for schema in schema_response:
                            if schema.id == response['id']:
                                aux = self._convert_to_dict(response['response'])['tracks']
                                aux['total'] = len(aux['data'])
                                track_response = self._validate_tracks_response(aux, download_cover=False)
                                schema.music_list = track_response
                                
                for schema in schema_response:
                    self._download_playlist_cover(schema)
                            
        return schema_response
      
    def _download_playlist_cover(self, playlist_obj: schemas.PlaylistSchema):
        max_item = 4
        for music in playlist_obj.music_list:
            aux = None
            if(len(playlist_obj.cover_images) == 0):
                aux = utils.download_cover(self, album_cover_url=music.album_cover_playlist_url,
                                                album_title=music.album_title, playlist_cover=True)
                playlist_obj.cover_images.append(schemas.PlaylistListCover.parse_obj({'cover': aux,
                                                                                        'album_title': music.album_title}))                  
            else:
                for cover in playlist_obj.cover_images:
                    if(music.album_title != cover.album_title and len(playlist_obj.cover_images) < 4):
                        aux = utils.download_cover(self, album_cover_url=music.album_cover_playlist_url,
                                                album_title=music.album_title, playlist_cover=True)
                        playlist_obj.cover_images.append(schemas.PlaylistListCover.parse_obj({'cover': aux,
                                                                                        'album_title': music.album_title}))                  
                        break  
                    
        if len(playlist_obj.cover_images) < max_item:
            if(len(playlist_obj.cover_images) != 0):
                for i in range(max_item-len(playlist_obj.cover_images)):
                    playlist_obj.cover_images.append(playlist_obj.cover_images[0])
            else:
                for i in range(max_item):
                    playlist_obj.cover_images.append(QPixmap(':/images/default_cover.png'))
                    
                
    def _convert_to_dict(self, response):        
        return json.loads(response)
