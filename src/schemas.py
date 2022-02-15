from typing import Optional
from pydantic import BaseModel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QUrl


class MusicSchema(BaseModel):
    id: int
    title: str
    artist: str
    album_title: str
    album_cover_url: Optional[str] = None
    album_cover_playlist_url: Optional[str] = None
    album_cover: Optional[QPixmap] = None
    path: str
    duration: int
    music_file: Optional[QUrl] = None
    music_file_id: Optional[int] = None
    
    class Config:
        arbitrary_types_allowed = True
  
class CreatorSchema(BaseModel):
    id: int
    name: str
    
class PlaylistListCover(BaseModel):
    cover: QPixmap
    album_title: str

    class Config:
        arbitrary_types_allowed = True
        
class PlaylistSchema(BaseModel):
    id: int
    title: str
    link: str
    nb_tracks: int
    tracklist: str
    creator: Optional[CreatorSchema] = None
    fans: Optional[int] = None
    duration: Optional[int] = None
    description: Optional[int] = None
    music_list: Optional[list] = None
    cover_images: Optional[list] = []