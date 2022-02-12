from pydantic import BaseModel
from PySide6.QtGui import QPixmap

class MusicSchema(BaseModel):
    title: str
    artist: str
    album_title: str
    album_cover: QPixmap
    path: str
    duration: int
    
    class Config:
        arbitrary_types_allowed = True