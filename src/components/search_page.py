from datetime import timedelta
from PySide6.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QWidget, QLabel, QSizePolicy, QHBoxLayout, QToolButton
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
import schemas
import requests
import tempfile
import utils


class SearchPage(QFrame):
    
    play_request = Signal(list)

    def __init__(self, parent) -> None:
        super(SearchPage, self).__init__(parent=parent)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0); border: none;')
        
        self.entry_list = []
        self._sender = None

        self._main_layout = QVBoxLayout(self)
        self._main_layout.setSpacing(0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self._results_area = QWidget()

        self._results_layout = QVBoxLayout(self._results_area)
        self._results_layout.setAlignment(Qt.AlignTop)
        self._results_layout.setSpacing(0)
        self._results_layout.setContentsMargins(0, 0, 0, 0)

        self._results_scroll = QScrollArea()
        self._results_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self._results_scroll.setWidgetResizable(True)
        self._results_scroll.setStyleSheet("""QScrollBar:vertical {
                                            background: #565C67;
                                            border-radius: 4px;
                                            width:8px;    
                                            margin: 0px 0px 0px 0px;
                                            }
                                            QScrollBar::handle:vertical {
                                            background: #161C26;
                                            border-radius: 4px;
                                            min-height: 0px;
                                            }
                                            QScrollBar::add-line:vertical {
                                            background: rgba(0, 0, 0, 0);
                                            height: 0px;
                                            subcontrol-position: bottom;
                                            subcontrol-origin: margin;
                                            }
                                            QScrollBar::sub-line:vertical {
                                            background: rgba(0, 0, 0, 0);
                                            height: 0 px;
                                            subcontrol-position: top;
                                            subcontrol-origin: margin;
                                            }""")

        self._results_scroll.setWidget(self._results_area)
        self._main_layout.addWidget(self._results_scroll)
            
    def update_search_page(self, data_list: list):
        if(len(self.entry_list) > 0):
            for entry in self.entry_list:
                try:
                    entry.deleteLater()
                except RuntimeError:
                    pass
            
            self.entry_list = []
        
        if(len(data_list) > 0):
            for data in data_list:
                object = MusicEntry(data)
                self.entry_list.append(object)
                
            for entry in self.entry_list:
                entry.info.connect(self._play_clicked)
                self._results_layout.addWidget(entry)
                
    def _play_clicked(self, music_obj):
        self._sender = self.sender()
        self.play_request.emit([music_obj, self._sender])


class MusicEntry(QFrame):
    
    info = Signal(schemas.MusicSchema)

    def __init__(self, music_obj):
        super(MusicEntry, self).__init__()
        self.setMinimumHeight(60)
        self.setMaximumHeight(60)
        self.setStyleSheet('background-color: rgba(22, 28, 38, 0.6)')
        
        self.music_obj = music_obj
        self.title = music_obj.title if len(music_obj.title) <= 30 else music_obj.title[:30]+'...'
        self.artist = music_obj.artist if len(music_obj.artist) <= 15 else music_obj.artist[:15]+'...'
        self.album_title = music_obj.album_title if len(music_obj.album_title) <= 17 else music_obj.album_title[:17]+'...'
        self.path = music_obj.album_cover
        self.cover = music_obj.album_cover
        self.duration = self.convert_duration(music_obj.duration)
        self._tranparency_style = 'background-color: rgba(0, 0, 0, 0)'
        self.loading = False

        self._main_layout = QHBoxLayout(self)
        self._main_layout.setSpacing(0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        # title container
        self._title_container = QFrame(self)
        self._title_container.setStyleSheet(self._tranparency_style)
        self._title_container.setMinimumWidth(420)
        self._title_container.setMinimumHeight(60)
        self._title_container.setMaximumWidth(420)
        self._title_layout = QHBoxLayout(self._title_container)
        self._title_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._title_layout.setSpacing(10)
        self._title_layout.setContentsMargins(10, 0, 10, 0)
        self._main_layout.addWidget(self._title_container)
        
        self._cover_label = QLabel(self._title_container)
        self._cover_label.setMinimumSize(QSize(54, 54))
        self._cover_label.setMaximumSize(QSize(54, 54))
        self._cover_label.setPixmap(self.cover)
        self._cover_label.setScaledContents(True)
        self._title_layout.addWidget(self._cover_label)
        
        self._title_label = QLabel(self._title_container)
        self._title_label.setMinimumWidth(300)
        self._title_label.setMaximumWidth(300)
        self._title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._title_label.setStyleSheet('color: #909090')
        self._title_label.setText(self.title.upper())
        utils.set_font(self._title_label, size=11, medium=True)
        self._title_layout.addWidget(self._title_label)
        
        # buttons container
        self._buttons_container = QFrame(self)
        self._buttons_container.setStyleSheet(self._tranparency_style)
        self._buttons_container.setMinimumWidth(80)
        self._buttons_container.setMinimumHeight(60)
        self._buttons_container.setMaximumWidth(80)
        self._buttons_layout = QHBoxLayout(self._buttons_container)
        self._buttons_layout.setAlignment(Qt.AlignCenter)
        self._buttons_layout.setSpacing(10)
        self._buttons_layout.setContentsMargins(10, 0, 10, 0)
        self._main_layout.addWidget(self._buttons_container)
        
        self._plus_btn = QToolButton(self._buttons_container)
        self._plus_btn.setMaximumSize(15, 15)
        self._plus_btn.setIcon(utils.load_svg(':/images/plus.svg', size=QSize(15, 15)))
        self._plus_btn.setIconSize(QSize(15, 15))
        self._plus_btn.setCursor(Qt.PointingHandCursor)
        self._buttons_layout.addWidget(self._plus_btn)
        
        self._favorite_btn = QToolButton(self._buttons_container)
        self._favorite_btn.setMaximumSize(15, 15)
        self._favorite_btn.setIcon(utils.load_svg(':/images/favorite.svg', size=QSize(15, 15)))
        self._favorite_btn.setIconSize(QSize(15, 15))
        self._favorite_btn.setCursor(Qt.PointingHandCursor)
        self._buttons_layout.addWidget(self._favorite_btn)
        
        # info container
        self._info_container = QFrame(self)
        self._info_container.setStyleSheet(self._tranparency_style)
        self._info_container.setMinimumHeight(60)
        self._info_layout = QHBoxLayout(self._info_container)
        self._info_layout.setAlignment(Qt.AlignVCenter)
        self._info_layout.setSpacing(10)
        self._info_layout.setContentsMargins(10, 0, 10, 0)
        self._main_layout.addWidget(self._info_container)
        
        self._artist_label = QLabel(self._info_container)
        self._artist_label.setAlignment(Qt.AlignCenter)
        self._artist_label.setStyleSheet('color: #565C67')
        self._artist_label.setText(self.artist)
        utils.set_font(self._artist_label, size=11)
        self._info_layout.addWidget(self._artist_label)
        
        self._album_title_label = QLabel(self._info_container)
        self._album_title_label.setAlignment(Qt.AlignCenter)
        self._album_title_label.setStyleSheet('color: #565C67')
        self._album_title_label.setText(self.album_title)
        utils.set_font(self._album_title_label, size=11)
        self._info_layout.addWidget(self._album_title_label)
        
        self._duration_label = QLabel(self._info_container)
        self._duration_label.setAlignment(Qt.AlignCenter)
        self._duration_label.setStyleSheet('color: #565C67')
        self._duration_label.setText(self.duration)
        utils.set_font(self._duration_label, size=11)
        self._info_layout.addWidget(self._duration_label)
        
        # play container
        self._play_container = QFrame(self)
        self._play_container.setStyleSheet(self._tranparency_style)
        self._play_container.setMaximumSize(QSize(60, 60))
        self._play_container.setMinimumSize(QSize(60, 60))
        self._play_layout = QHBoxLayout(self._play_container)
        self._play_layout.setAlignment(Qt.AlignCenter)
        self._play_layout.setSpacing(10)
        self._play_layout.setContentsMargins(10, 0, 10, 0)
        self._main_layout.addWidget(self._play_container)
        
        self._play_btn = QToolButton(self._play_container)
        self._play_btn.close()
        self._play_btn.setMaximumSize(30, 30)
        self._play_btn.setIcon(utils.load_svg(':/images/play_btn.svg', size=QSize(30, 30)))
        self._play_btn.setIconSize(QSize(30, 30))
        self._play_btn.setCursor(Qt.PointingHandCursor)
        self._play_btn.clicked.connect(self.send_info)
        self._play_btn.clicked.connect(self._init_loading)
        self._play_layout.addWidget(self._play_btn)
        
        self._loading_widget = QSvgWidget(':/images/loading.svg')
        self._loading_widget.setMinimumSize(QSize(30, 30))
        self._loading_widget.setMaximumSize(QSize(30, 30))
        self._play_layout.addWidget(self._loading_widget)
        self._loading_widget.close()
    
    def enterEvent(self, event) -> None:
        self.setStyleSheet('background-color: rgba(22, 28, 38, 0.7)')
        if(not self.loading):
            self._play_btn.show()        
        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        self.setStyleSheet('background-color: rgba(22, 28, 38, 0.6)')
        self._play_btn.close()        
        return super().leaveEvent(event)
    
    def convert_duration(self, seconds: int):        
        return str(timedelta(seconds=seconds))[2:]
    
    def send_info(self):
        self.info.emit(self.music_obj)
        #self.info.emit(f'{self.title} - {self.artist}')
        
    def update_loading(self, value: bool):
        self.loading = value
        
    def _init_loading(self):
        self.loading = True
        self._play_btn.close()
        self._loading_widget.show()
        
    def stop_loading(self):
        self.loading = False
        if not(self._loading_widget.isHidden()):
            self._loading_widget.close()