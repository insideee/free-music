from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QSizePolicy, QToolButton
from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve, QAbstractAnimation, QPoint, QRect
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QPixmap

from components import Player, SearchPage
import utils

class AppUi(object):
    
    def init_gui(self, app):
        
        # app config
        app.setObjectName('main_app')
        app.setWindowTitle('Free Music')
        app.setWindowIcon(QPixmap(':/images/icon.png'))
        app.setMinimumSize(QSize(1200, 750)) 
        app.setStyleSheet("background-color: #003847")
        
        self.container = QFrame(app)
        self.container.setObjectName('main_container')
        self.container.setStyleSheet('background-color: none')
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setSpacing(0)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.nav_container = QFrame(self.container)
        self.nav_container.setObjectName('nav_container')
        self.nav_container.setMaximumWidth(165)
        self.nav_container.setMinimumWidth(165)
        self.nav_container.setStyleSheet('background-color: #161C26')
        self.nav_layout = QGridLayout(self.nav_container)
        self.nav_layout.setSpacing(0)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.container_layout.addWidget(self.nav_container)
        
        self.logo_container = QFrame(self.nav_container)
        self.logo_container.setMinimumSize(QSize(165, 60))
        self.logo_container.setMaximumSize(QSize(165, 60))
        self.logo_container.setStyleSheet('background-color: none')
        self.nav_layout.addWidget(self.logo_container, 0, 0)
        self.logo_layout = QVBoxLayout(self.logo_container)
        self.logo_layout.setAlignment(Qt.AlignLeft)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setContentsMargins(15, 0, 0, 0)
        
        self.logo = QSvgWidget(':/images/logo.svg')
        self.logo.setFixedSize(QSize(100, 40))
        self.logo_layout.addWidget(self.logo)
        
        self._buttons_nav_config()
        
        # content container
        self.content_container = QFrame(self.container)
        self.content_container.setObjectName('content_container')
        self.content_container.setStyleSheet('background-color: #003847')
        self.container_layout.addWidget(self.content_container)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignBottom)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # search container
        self.search_container = QFrame(self.content_container)
        self.search_container.setObjectName('search_container')
        self.search_container.setMinimumHeight(70)
        self.search_container.setMaximumHeight(70)
        self.search_container.setStyleSheet('background-color: none;')
        self.search_layout = QHBoxLayout(self.search_container)
        self.search_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.search_layout.setSpacing(10)
        self.search_container.setContentsMargins(10, 0, 0, 0)
        
        self.search_icon = QLabel(self.search_container)
        self.search_icon.setMinimumSize(QSize(20, 20))
        self.search_icon.setMaximumSize(QSize(20, 20))
        self.search_icon.setPixmap(utils.load_svg(':/images/search.svg', size = QSize(20, 20)))
        self.search_icon.setScaledContents(True)
        self.search_icon.setFocus()
        self.search_layout.addWidget(self.search_icon)
        
        self.search_entry = QLineEdit(self.search_container)
        self.search_entry.setObjectName('search_entry')
        self.search_entry.setPlaceholderText('Type here to search')
        self.search_entry.setMinimumSize(QSize(150, 20))
        self.search_entry.setMaximumSize(QSize(150, 20))
        utils.set_font(self.search_entry, size=11)
        self.search_entry.setStyleSheet('color: #909090;\
                                        border: none;\
                                        background-color: rgba(0, 0, 0, 0)')
        self.search_layout.addWidget(self.search_entry)
        
        self.search_loading = QSvgWidget(':/images/loading.svg')
        self.search_loading.setMinimumSize(QSize(30, 30))
        self.search_loading.setMaximumSize(QSize(30, 30))
        self.search_layout.addWidget(self.search_loading)
        self.search_loading.close()
        
        # display container        
        self.display_container = QStackedWidget(self.content_container)
        self.display_container.setObjectName('display_container')
        self.display_container.setMinimumHeight(620)
        self.display_container.setContentsMargins(0, 0, 0, 0)
        self.display_container.setStyleSheet('background-color: none')
        
        self.search_page = SearchPage(self.display_container)
        self.display_container.addWidget(self.search_page)
        self.display_container.setCurrentWidget(self.search_page)
        
        self.player = Player(self.content_container)
        
        self.content_layout.addWidget(self.search_container)
        self.content_layout.addWidget(self.display_container)
        self.content_layout.addWidget(self.player)
        
        app.setCentralWidget(self.container)
        
    def _buttons_nav_config(self):
        self.music_container = QFrame(self.nav_container)
        self.music_container.setMaximumSize(165, 200)
        self.music_container.setMinimumSize(165, 200)
        self.music_container.setStyleSheet('background-color: none')
        self.nav_layout.addWidget(self.music_container)
        self.music_layout = QVBoxLayout(self.music_container)
        self.music_layout.setSpacing(2)
        self.music_layout.setContentsMargins(15, 25, 0, 0)
        self.music_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.music_title_btn = CustomButtom(parent=self.music_container, text='music', title=True)
        self.music_title_btn.clicked.connect(lambda: self._nav_container_animation(self.music_container))
        self.music_layout.addWidget(self.music_title_btn)
        
        self.discover_btn = CustomButtom(parent=self.music_container, text='discover',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 60)), 
                                                        QSize(QSize(80, 20))))  
        self.rising_btn = CustomButtom(parent=self.music_container, text='rising',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 80)), 
                                                        QSize(QSize(80, 20))))       
        self.my_stars_btn = CustomButtom(parent=self.music_container, text='my stars',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 100)), 
                                                        QSize(QSize(80, 20))))
        self.songs_btn = CustomButtom(parent=self.music_container, text='songs',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 130)), 
                                                        QSize(QSize(80, 20))))
        self.artists_btn = CustomButtom(parent=self.music_container, text='artists',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 150)), 
                                                        QSize(QSize(80, 20))))
        self.albuns_btn = CustomButtom(parent=self.music_container, text='albuns',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 170)), 
                                                        QSize(QSize(80, 20))))

        # playlists
        self.playlists_container = QFrame(self.nav_container)
        self.playlists_container.setMaximumSize(165, 200)
        self.playlists_container.setMinimumSize(165, 200)
        self.playlists_container.setStyleSheet('background-color: none')
        self.nav_layout.addWidget(self.playlists_container)
        self.playlists_layout = QVBoxLayout(self.playlists_container)
        self.playlists_layout.setSpacing(2)
        self.playlists_layout.setContentsMargins(15, 0, 15, 0)
        self.playlists_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.playlist_header = QFrame(self.playlists_container)
        self.playlist_header.setFixedSize(QSize(165, 60))
        self.playlists_layout.addWidget(self.playlist_header)
        
        self.playlist_header_layout = QHBoxLayout(self.playlist_header)
        self.playlist_header_layout.setSpacing(0)
        self.playlist_header_layout.setContentsMargins(0, 0, 0, 0)
        self.playlist_header_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.playlist_title_btn = CustomButtom(parent=self.playlist_header, text='playlists', title=True)
        self.playlist_header_layout.addWidget(self.playlist_title_btn)
        self.playlist_title_btn.clicked.connect(lambda: self._nav_container_animation(self.playlists_container))
        
        self.add_playlist_btn = QToolButton(self.playlist_header)
        self.add_playlist_btn.setIcon(utils.load_svg(':/images/plus.svg', size=QSize(16, 16)))
        self.add_playlist_btn.setStyleSheet('background-color: rgba(0, 0, 0, 0);\
                                            border: none;\
                                            border-radius: none')
        self.add_playlist_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.add_playlist_btn.setCursor(Qt.PointingHandCursor)
        self.add_playlist_btn.setFixedSize(QSize(16, 16))
        self.playlist_header_layout.addWidget(self.add_playlist_btn)
        
    def _nav_container_animation(self, frame: QFrame):
        height = frame.height()
        standard = 200
        extend = standard if height < standard else 60
        
        frame.animation = QPropertyAnimation(frame, b'minimumHeight')
        frame.animation.setDuration(400)
        frame.animation.setStartValue(height)
        frame.animation.setEndValue(extend)
        frame.animation.setEasingCurve(QEasingCurve.InOutQuad)
        frame.animation.start(QAbstractAnimation.DeleteWhenStopped)
        
        
class CustomButtom(QPushButton):
    
    def __init__(self, parent, text, geometry: QRect = None, title: bool = False):
        super(CustomButtom, self).__init__(parent=parent)
        if geometry != None:
            self.setGeometry(geometry)
        self._title = title
        
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        size = QSize(80, 20) if not self._title else QSize(120, 30)
        self.setFixedSize(size)  
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0); \
                                            border: none; \
                                            border-radius: none')
        
        self._title_label = QLabel(text.capitalize()) if not self._title else QLabel(text.upper())
        self._title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._title_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        if self._title:
            self._title_label.setStyleSheet('color: #909090')
            utils.set_font(self._title_label, size=11, medium=True)
        else:
            self._title_label.setStyleSheet('color: #565C67')
            utils.set_font(self._title_label, size=11)
        self.layout().addWidget(self._title_label)
        
            
    def enterEvent(self, event) -> None:
        if not self._title:
            self._title_label.setStyleSheet('color: #909090')        
        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        if not self._title:
            self._title_label.setStyleSheet('color: #565C67')  
        return super().leaveEvent(event)