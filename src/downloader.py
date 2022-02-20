import yt_dlp
from youtubesearchpython import VideosSearch
from PySide6.QtCore import QThread, QUrl, Signal
import tempfile
import os


class Downloader(QThread):
    
    download_completed = Signal(list)
    
    def __init__(self):
        super(Downloader, self).__init__()
        self._title = None
        self._path = None  
        self._emit_play = False
        self._is_playlist = False
        
    def run(self):
        print('Downloader Thread Started')
        
        url_video, _id = self._search_video(self._title)
        
        if(url_video != None):
            if(self._path == None):
                self._path = self._create_path()
            
            ydl_opts = {'format': 'bestaudio',
                        'outtmpl': f'{self._path}/%(id)s.mp3',
                        'noplaylist': True,
                        'quiet': False,}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_video])
            
            file_path = QUrl.fromLocalFile(f'{self._path}/{_id}.mp3')
            if(self._emit_play):
                self.download_completed.emit([[file_path, _id], True, self._is_playlist])
                self._emit_play = False
            else:
                self.download_completed.emit([[file_path, _id], False, self._is_playlist])
                
            
    def _search_video(self, title):
        video_search = VideosSearch(title, limit=1)
        url_video = None

        if 'link' in video_search.result()['result'][0]:
            url_video = video_search.result()['result'][0]['link'] 
            title = video_search.result()['result'][0]['title']
            _id = video_search.result()['result'][0]['id']
            
        return [url_video, _id]
    
    def _create_path(self):
        return tempfile.mkdtemp()
    
    def update_title(self, title, is_playlist = False):
        if(is_playlist):
            self._is_playlist = True
        else:
            self._is_playlist = False
        self._title = title
        
    def update_emit_play(self, emit: bool):
        self._emit_play = emit

        
class SourceDownloader(QThread):
    
    download_completed = Signal(QUrl)
    
    def __init__(self):
        super(SourceDownloader, self).__init__()
        self._source_id = None
        self._yt_endpoint = 'https://www.youtube.com/watch?v='
        self._path = None
        
    def run(self):
        print('Downloader Thread Working')
        
        if(self._path != None):
            if( not os.path.isdir(self._path)):
                self._path = self._create_path
                
        ydl_opts = {'format': 'bestaudio',
                        'outtmpl': f'{self._path}/%(id)s.mp3',
                        'noplaylist': True,
                        'quiet': False,}
        
        url_video = f'{self._yt_endpoint}{self._source_id}'
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_video])
            file_path = QUrl.fromLocalFile(f'{self._path}/{self._source_id}.mp3')
            
            if(os.path.isfile(file_path.path())):
                self.download_completed.emit(file_path)
                
    def update_path(self, path: str):
        self._path = path
     
    def update_id(self, id: int):
        self._id = id
        
    def _create_path(self):
        return os.mkdir(self._path)
