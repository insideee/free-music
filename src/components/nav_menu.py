from PySide6.QtWidgets import QFrame, QHBoxLayout, QGraphicsDropShadowEffect, QGridLayout, QToolButton, QVBoxLayout, QSizePolicy, QPushButton, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint, QRect, QAbstractAnimation, Slot
from PySide6.QtSvgWidgets import QSvgWidget

import utils

class CustomNavMenu(QFrame):
    
    
    def __init__(self, parent):
        super(CustomNavMenu, self).__init__(parent=parent)
        
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(20)
        self._shadow.setXOffset(0)
        self._shadow.setYOffset(0)
        self._shadow.setColor(QColor(0, 0, 0, 100))
        
        self._expanded = True
        
        self.setMinimumWidth(28)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet('border-bottom-left-radius: 10px;')
        self.setLayout(QGridLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 15, 0, 15)
        self.layout().setAlignment(Qt.AlignRight)
        self.setGraphicsEffect(self._shadow)
        
        icon_size = QSize(5, 9)
        self._expand_left_icon = utils.load_svg(':/images/expand_left.svg', size=icon_size)
        self._expand_right_icon = utils.load_svg(':/images/expand_right.svg', size=icon_size)
        self._toggle_btn = QToolButton(self)
        self._toggle_btn.setCursor(Qt.PointingHandCursor)
        self._toggle_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self._toggle_btn.setIcon(self._expand_right_icon)
        self._toggle_btn.setIconSize(icon_size)
        self._toggle_btn.setBaseSize(QSize(13, 29))
        self._toggle_btn.setFixedSize(self._toggle_btn.baseSize())
        self._toggle_btn.setStyleSheet('background-color: rgba(22, 28, 38, 1);\
                                        border-bottom-left-radius: 5px;\
                                        border-top-left-radius: 5px;')
        self.layout().addWidget(self._toggle_btn, 0, 0)
        self.layout().setAlignment(self._toggle_btn,  Qt.AlignTop)
        self._toggle_btn.clicked.connect(self._toggle_animation)
        self._toggle_btn.clicked.connect(self._change_toggle_icon)
        
        self._nav_container = QFrame(self)
        self._nav_container.setObjectName('nav_container')
        self._nav_container.setMinimumWidth(165)
        self._nav_container.setMaximumWidth(165)
        self.layout().addWidget(self._nav_container, 0, 1)
        self._nav_container.setStyleSheet('background-color: rgba(22, 28, 38, 1); border-bottom-left-radius: 10px;')
        self._nav_layout = QGridLayout(self._nav_container)
        self._nav_layout.setSpacing(0)
        self._nav_layout.setContentsMargins(0, 0, 0, 0)
        
        self._buttons_nav_config()
        
        #self._logo_container = QFrame(self._nav_container)
        #self._logo_container.setMinimumSize(QSize(165, 60))
        #self._logo_container.setMaximumSize(QSize(165, 60))
        #self._logo_container.setStyleSheet('background-color: none')
        #self._nav_layout.addWidget(self._logo_container, 0, 0)
        #self._logo_layout = QVBoxLayout(self._logo_container)
        #self._logo_layout.setAlignment(Qt.AlignLeft)
        #self._logo_layout.setSpacing(0)
        #self._logo_layout.setContentsMargins(15, 0, 0, 0)
        
        #self._logo = QSvgWidget(':/images/logo.svg')
        #self._logo.setFixedSize(QSize(100, 40))
        #self._logo_layout.addWidget(self._logo)
        
        self._animation = QPropertyAnimation(self._nav_container, b'minimumWidth')
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.InOutSine)
     
    def _buttons_nav_config(self):
        self.music_container = QFrame(self._nav_container)
        self.music_container.setMaximumSize(145, 220)
        self.music_container.setMinimumSize(145, 220)
        self.music_container.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self._nav_layout.setAlignment(self.music_container, Qt.AlignLeft | Qt.AlignTop)
        self.music_layout = QGridLayout(self.music_container)
        self.music_layout.setSpacing(2)
        self.music_layout.setContentsMargins(15, 25, 0, 0)
        self.music_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.music_title_btn = CustomButtom(parent=self.music_container, text='music', title=True)
        self.music_layout.addWidget(self.music_title_btn)
        
        self.discover_btn = CustomButtom(parent=self.music_container, text='discover',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 65)), 
                                                        QSize(QSize(80, 20))))  
        self.rising_btn = CustomButtom(parent=self.music_container, text='rising',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 90)), 
                                                        QSize(QSize(80, 20))))       
        self.my_stars_btn = CustomButtom(parent=self.music_container, text='my stars',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 115)), 
                                                        QSize(QSize(80, 20))))
        self.songs_btn = CustomButtom(parent=self.music_container, text='songs',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 150)), 
                                                        QSize(QSize(80, 20))))
        self.artists_btn = CustomButtom(parent=self.music_container, text='artists',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 175)), 
                                                        QSize(QSize(80, 20))))
        self.albuns_btn = CustomButtom(parent=self.music_container, text='albuns',
                                         geometry=QRect(QPoint(self.music_container.pos()+QPoint(15, 200)), 
                                                        QSize(QSize(80, 20))))

        
        # playlists
        self.playlists_container = QFrame(self._nav_container)
        self.playlists_container.setBaseSize(QSize(145, 220))
        self.playlists_container.setMaximumSize(self.playlists_container.baseSize())
        self.playlists_container.setMinimumSize(self.playlists_container.baseSize())
        self.playlists_container.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.playlists_layout = QVBoxLayout(self.playlists_container)
        self.playlists_layout.setSpacing(2)
        self.playlists_layout.setContentsMargins(15, 0, 15, 0)
        self.playlists_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.playlists_container.setGeometry(QRect((self.music_container.pos() + QPoint(0, self.music_container.height())),
                                             self.playlists_container.baseSize()))
        
        self.playlist_header = QFrame(self.playlists_container)
        self.playlist_header.setFixedSize(QSize(165, 60))
        self.playlists_layout.addWidget(self.playlist_header)
        
        self.playlist_header_layout = QHBoxLayout(self.playlist_header)
        self.playlist_header_layout.setSpacing(0)
        self.playlist_header_layout.setContentsMargins(0, 0, 0, 0)
        self.playlist_header_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.playlist_title_btn = CustomButtom(parent=self.playlist_header, text='playlists', title=True)
        self.playlist_header_layout.addWidget(self.playlist_title_btn)
        
        self.add_playlist_btn = QToolButton(self.playlist_header)
        self.add_playlist_btn.setIcon(utils.load_svg(':/images/plus.svg', size=QSize(16, 16)))
        self.add_playlist_btn.setStyleSheet('background-color: rgba(0, 0, 0, 0);\
                                            border: none;\
                                            border-radius: none')
        self.add_playlist_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.add_playlist_btn.setCursor(Qt.PointingHandCursor)
        self.add_playlist_btn.setFixedSize(QSize(16, 16))
        self.playlist_header_layout.addWidget(self.add_playlist_btn) 
    
    @Slot()   
    def _toggle_animation(self):
        start_w = self._nav_container.width()
        standard = 165
        expand = standard if start_w < standard else 15
        
        self._animation.setStartValue(start_w)
        self._animation.setEndValue(expand)
        self._animation.start()
    
    @Slot()   
    def _change_toggle_icon(self):
        if self._expanded:
            self._toggle_btn.setIcon(self._expand_left_icon)
            self._expanded = False
        else:
            self._toggle_btn.setIcon(self._expand_right_icon)
            self._expanded = True
            
        

class CustomButtom(QPushButton):
    
    def __init__(self, parent, text, geometry: QRect = None, title: bool = False):
        super(CustomButtom, self).__init__(parent=parent)
        if geometry != None:
            self.setGeometry(geometry)
        self._title = title
        
        self._clear_style = 'background-color: none; \
                            border: none; \
                            border-radius: none'
        
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        size = QSize(80, 20) if not self._title else QSize(100, 30)
        self.setFixedSize(size) 
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(self._clear_style)
        
        self._title_label = QLabel(text.capitalize()) if not self._title else QLabel(text.upper())
        self._title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._title_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        if self._title:
            self._title_label.setStyleSheet('background-color: none; color: #909090')
            utils.set_font(self._title_label, size=12, medium=True)
        else:
            self._title_label.setStyleSheet('background-color: none; color: #565C67')
            utils.set_font(self._title_label, size=12)
        self.layout().addWidget(self._title_label)
        
            
    def enterEvent(self, event) -> None:
        self.setStyleSheet(self._clear_style)
        if not self._title:
            self._title_label.setStyleSheet('background-color: none; color: #909090')        
        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        self.setStyleSheet(self._clear_style)
        if not self._title:
            self._title_label.setStyleSheet('background-color: none; color: #565C67')  
        return super().leaveEvent(event)
        
        
        