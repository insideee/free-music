import yt_dlp
from youtubesearchpython import VideosSearch
from PySide6.QtCore import QThread, QUrl, Signal
import tempfile


class Downloader(QThread):
    
    download_completed = Signal(list)
    
    def __init__(self):
        super(Downloader, self).__init__()
        self._title = None
        self._path = None  
        self._emit_play = False
        
    def run(self):
        print('Thread Working')
        
        url_video, title_video = self._search_video(self._title)
        
        if(url_video != None):
            if(self._path == None):
                self._path = self._create_path()
            
            ydl_opts = {'format': 'bestaudio',
                        'outtmpl': f'{self._path}/%(title)s.mp3',
                        'noplaylist': True,
                        'quiet': False,}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_video])
            
            file_path = QUrl.fromLocalFile(f'{self._path}/{title_video}.mp3')
            if(self._emit_play):
                self.download_completed.emit([file_path, True])
                self._emit_play = False
            else:
                self.download_completed.emit([file_path, False])
                
            
    def _search_video(self, title):
        video_search = VideosSearch(title, limit=1)
        url_video = None

        if 'link' in video_search.result()['result'][0]:
            url_video = video_search.result()['result'][0]['link'] 
            title = video_search.result()['result'][0]['title']
            
        return [url_video, title]
    
    def _create_path(self):
        return tempfile.mkdtemp()
    
    def update_title(self, title):
        self._title = title
        
    def update_emit_play(self, emit: bool):
        self._emit_play = emit
