from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt, QSize, QObject
from PySide6.QtGui import QPixmap, QPainter, QFontDatabase, QFont
import requests
import os

def load_svg(path: str, size: QSize) -> QPixmap:
    """Load a svg file and return a qpixmap
    """
    svg_render = QSvgRenderer(path)   
    new_image = QPixmap(size)
    painter = QPainter()
    
    new_image.fill(Qt.transparent)
    painter.begin(new_image)
    svg_render.render(painter)
    painter.end()
    return new_image

def set_font(target: QObject, size: int, medium=False, bold: bool=False) -> None:
    """Set a custom font to the target
    """
    font_name = ':/fonts/IBMPlexSansThaiLooped-Regular.ttf' if not medium else ':/fonts/IBMPlexSansThaiLooped-Medium.ttf'
    index = 0
    
    # add font to app database
    font_id = QFontDatabase.addApplicationFont(f'{font_name}')
    font_name = QFontDatabase.applicationFontFamilies(font_id)
    
    # get font name
    font = QFont(font_name[index])
    font.setPointSize(size)
    font.setBold(bold)
    font.setStyleStrategy(QFont.PreferAntialias)
    
    target.setFont(font)
    
def download_cover(cls, album_cover_url, album_title, playlist_cover=False):
    """Download the album cover of a track
    """
    # find a better location for this

    if(album_cover_url != None):
        album_title = album_title.replace('/', '')
        album_title = album_title.replace(' ', '')
        if(not(os.path.isdir(cls.path))):
            os.mkdir(cls.path)
        save_path = f'{cls.path}/{album_title}.jpg' if not playlist_cover else f'{cls.path}/{album_title}_playlist.jpg'
        if not (os.path.isfile(save_path)):
            r = requests.get(album_cover_url, allow_redirects=True)
            open(save_path, 'wb').write(r.content)

        return QPixmap(save_path)
    else:
        # default image for no album cover
        return QPixmap(':/images/default_cover.png')
        
def find_parent(obj: QObject, target: str):
    """Find the target parent of a children qobject
    """
    parent = obj.parent()
    
    if hasattr(obj, 'objectName'):
        for i in range(40):
            if obj.objectName() == target:
                return obj
            else:
                obj = obj.parent()
                
    return None