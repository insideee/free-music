from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt, QSize, QObject
from PySide6.QtGui import QPixmap, QPainter, QFontDatabase, QFont

def load_svg(path: str, size: QSize):
    svg_render = QSvgRenderer(path)   
    new_image = QPixmap(size)
    painter = QPainter()
    
    new_image.fill(Qt.transparent)
    painter.begin(new_image)
    svg_render.render(painter)
    painter.end()
    return new_image

def set_font(target: QObject, size: int, font_name: str=':/fonts/IBMPlexSansThaiLooped-Regular.ttf', bold: bool=False, index: int=0) -> None:

    # add font to app database
    font_id = QFontDatabase.addApplicationFont(f'{font_name}')
    font_name = QFontDatabase.applicationFontFamilies(font_id)
    
    # get font name
    font = QFont(font_name[index])
    font.setPointSize(size)
    font.setBold(bold)
    font.setStyleStrategy(QFont.PreferAntialias)
    
    target.setFont(font)