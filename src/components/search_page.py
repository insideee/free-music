from datetime import timedelta
from PySide6.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QToolButton, QGraphicsDropShadowEffect, QSizePolicy, QGridLayout
from PySide6.QtCore import Qt, QSize, Signal, QPoint, QRect, QPropertyAnimation, QEasingCurve, QAbstractAnimation, Slot
from PySide6.QtGui import QColor
from PySide6.QtSvgWidgets import QSvgWidget
import schemas
import utils


class SearchPage(QFrame):
    
    play_request = Signal(list)
    playlist_request = Signal(list)

    def __init__(self, parent) -> None:
        super(SearchPage, self).__init__(parent=parent)
        self._transparency_style = 'background-color: rgba(0, 0, 0, 0); border: none;'
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0); border: none;')
        
        self.music_entry_list = []
        self.playlist_entry_list = []
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
                                            background: rgba(0, 0, 0, 0);
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
        
        self._playlist_display = None
        self._playlist_result_area = None
        self._playlist_results_scroll = None
            
    def update_search_page(self, data: dict):
        
        self._delete_entries()
        self._create_playlist_display()
        
        for k, v in data.items():
            if k == 'playlists':
               for playlist in v:
                    entry = PlaylistEntry(playlist)
                    self.playlist_entry_list.append(entry)
            else:
                for track in v:
                    track = MusicEntry(track)
                    self.music_entry_list.append(track)
                 
        # show new widgets
        for entry in self.playlist_entry_list:
            self._playlist_result_area.layout().addWidget(entry)
            entry.playlist_play_clicked.connect(self._play_playlist_clicked)
        
        count = 0
        for entry in self.music_entry_list:
            if count == 3:
                if self._playlist_display.isHidden() and \
                    len(self.playlist_entry_list) > 0:
                    self._results_layout.addWidget(self._playlist_display)
            entry.info.connect(self._play_clicked)
            self._results_layout.addWidget(entry)
            count += 1
     
    def _delete_entries(self):
        if len(self.music_entry_list) > 0:
            for entry in self.music_entry_list:
                try:
                    entry.deleteLater()
                except RuntimeError:
                    # already deleted
                    pass
            self.music_entry_list = []
                
        if len(self.playlist_entry_list) > 0:
            for entry in self.playlist_entry_list:
                try:
                    entry.deleteLater()
                except RuntimeError:
                    # already deleted
                    pass
            self.playlist_entry_list = []
                   
    @Slot()           
    def _play_clicked(self, music_obj):
        self._sender = self.sender()
        self.play_request.emit([music_obj, self._sender])
    
    @Slot()
    def _play_playlist_clicked(self, playlist_obj):
        self._sender = self.sender()
        self.playlist_request.emit([playlist_obj, self._sender])      
        
    def _create_playlist_display(self):
        if self._playlist_display != None \
            and self._playlist_result_area != None \
            and self._playlist_results_scroll != None:
            try:
                self._playlist_display.deleteLater()
                self._playlist_result_area.deleteLater()
                self._playlist_results_scroll.deleteLater()
            except RuntimeError:
                # already deleted
                pass
            finally:
                self._playlist_display = None
                self._playlist_result_area = None
                self._playlist_results_scroll = None
                
        self._playlist_display = QFrame(self._results_area)
        self._playlist_display.setMinimumHeight(360)
        self._playlist_display.setMinimumHeight(360)
        self._playlist_display.setStyleSheet(self._transparency_style)
        self._playlist_display.setLayout(QHBoxLayout())
        self._playlist_display.layout().setSpacing(50)
        self._playlist_display.layout().setContentsMargins(0, 0, 0, 25)
        self._playlist_display.layout().setAlignment(Qt.AlignCenter)  
        
        self._playlist_result_area = QWidget() 
        self._playlist_result_area.setLayout(QHBoxLayout())
        self._playlist_result_area.layout().setSpacing(100)
        self._playlist_result_area.layout().setContentsMargins(50, 0, 50, 0)
        self._playlist_result_area.layout().setAlignment(Qt.AlignCenter)  
        
        self._playlist_results_scroll = QScrollArea()
        self._playlist_results_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self._playlist_results_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self._playlist_results_scroll.setWidgetResizable(True)
        self._playlist_results_scroll.setStyleSheet("""QScrollBar:horizontal {
                                            background: rgba(0, 0, 0, 0);
                                            height:8px;    
                                            margin-left: 5px;
                                            }
                                            QScrollBar::handle:horizontal {
                                            background: #161C26;
                                            border-radius: 4px;
                                            min-width: 0px;
                                            margin-left: 5px;
                                            }
                                            QScrollBar::add-line:horizontal {
                                            background: rgba(0, 0, 0, 0);
                                            height: 0px;
                                            subcontrol-position: bottom;
                                            subcontrol-origin: margin;
                                            }
                                            QScrollBar::sub-line:horizontal {
                                            background: rgba(0, 0, 0, 0);
                                            height: 0 px;
                                            subcontrol-position: top;
                                            subcontrol-origin: margin;
                                            }""")

        self._playlist_results_scroll.setWidget(self._playlist_result_area)  
        self._playlist_display.layout().addWidget(self._playlist_results_scroll)


class CustomPlayButton(QLabel):
    
    clicked = Signal(bool)
    
    def __init__(self, parent):
        super(CustomPlayButton, self).__init__(parent=parent)
        self.setBaseSize(QSize(80, 80))
        self.setMinimumSize(self.baseSize())
        self.resize(self.baseSize())
        self.setStyleSheet('background-color: none')
        a = utils.load_svg(':/images/playlist.svg', size=QSize(80, 80))
        self.setCursor(Qt.PointingHandCursor)
        self.setPixmap(utils.load_svg(':/images/playlist.svg', size=QSize(80, 80)))
        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
        # animation
        self.animation = QPropertyAnimation(self, b'minimumSize')
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutSine)
        
        # shadow
        drop_shadow = QGraphicsDropShadowEffect(self)
        drop_shadow.setBlurRadius(20)
        drop_shadow.setOffset(0)
        drop_shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(drop_shadow)
    
    def mousePressEvent(self, ev) -> None:
        if ev.button() == Qt.LeftButton:
           ev.accept()
           self.clicked.emit(True)
        else:
            return super().mousePressEvent(ev)
       
    def enterEvent(self, event) -> None:
        init_rect = self.geometry()
        end_rect = QRect(QPoint(0, 0), QSize(100, 100))
        end_rect.moveCenter(init_rect.center())
        
        init_size = QSize(80, 80)
        end_size = QSize(100, 100)
        
        self.animation.setStartValue(init_size)
        self.animation.setEndValue(end_size)
        self.animation.setDirection(QAbstractAnimation.Forward)
        self.animation.start()
        
        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.start()
        return super().leaveEvent(event)    


class PlaylistEntry(QFrame):
    
    playlist_play_clicked = Signal(schemas.PlaylistSchema)
    
    def __init__(self, playlist_obj: schemas.PlaylistSchema):
        super(PlaylistEntry, self).__init__()
        
        self._default_icon = utils.load_svg(':/images/playlist.svg', size=QSize(80, 80))
        self._hover_icon = utils.load_svg(':/images/playlist.svg', size=QSize(100, 100))
        self._transparency_style = 'background-color: rgba(0, 0, 0, 0)'
        self._playlist_obj = playlist_obj
        self.title = self._playlist_obj.title.title() if len(self._playlist_obj.title) <= 22 else \
                                    self._playlist_obj.title[:22]+'...'.title()
        
        self.setFixedSize(QSize(240, 275))
        self.setStyleSheet(self._transparency_style)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        
        # top container
        self._top_container = QFrame(self)
        self._top_container.setStyleSheet(self._transparency_style)
        self._top_container.setFixedSize(QSize(240, 240))
        self.layout().addWidget(self._top_container)
        
        self._cover_container = QFrame(self._top_container)
        self._cover_container.setGeometry(QRect(QPoint(0, 0), QSize(240, 240)))
        self._cover_container.setStyleSheet(self._transparency_style)
        self._cover_container.setLayout(QGridLayout())
        self._cover_container.layout().setSpacing(0)
        self._cover_container.layout().setContentsMargins(0, 0, 0, 0)
        
        
        self._covers = []
        
        for cover_obj in self._playlist_obj.cover_images:
            label = QLabel(self._cover_container)
            label.setFixedSize(QSize(120, 120))
            label.setPixmap(cover_obj.cover)
            label.setScaledContents(True)
            self._covers.append(label)
            
        for i in range(len(self._covers)):
            row = 1 if i >= 2 else 0
            if(i % 2 == 0):
                self._cover_container.layout().addWidget(self._covers[i], row, 0)
            else:
                self._cover_container.layout().addWidget(self._covers[i], row, 1)
                
        self._play_container = QFrame(self._top_container)
        self._play_container.setGeometry(QRect(QPoint(0, 0), QSize(240, 240)))
        self._play_container.setStyleSheet(self._transparency_style)
        self._play_container.setLayout(QVBoxLayout())
        self._play_container.layout().setSpacing(0)
        self._play_container.layout().setAlignment(Qt.AlignCenter)
        self._play_container.layout().setContentsMargins(0, 0, 0, 0)
        
        self._play_btn = CustomPlayButton(self._play_container)
        self._play_btn.clicked.connect(lambda: self.playlist_play_clicked.emit(self._playlist_obj))
        self._play_container.layout().addWidget(self._play_btn)
        
        # info/ btn container
        self._bottom_container = QFrame(self)
        self._bottom_container.setStyleSheet(self._transparency_style)
        self._bottom_container.setFixedSize(QSize(240, 35))
        self._bottom_container.setLayout(QHBoxLayout())
        self._bottom_container.layout().setAlignment(Qt.AlignVCenter)
        self._bottom_container.layout().setSpacing(10)
        self._bottom_container.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._bottom_container)
        
        self._album_label = QLabel(self._bottom_container)
        self._album_label.setMinimumHeight(35)
        self._album_label.setStyleSheet('color: #909090')
        self._album_label.setText(self.title)
        utils.set_font(self._album_label, medium=True, size=11)
        self._bottom_container.layout().addWidget(self._album_label)    
        
        self._plus_btn = QToolButton(self._bottom_container)
        self._plus_btn.setFixedSize(15, 15)
        self._plus_btn.setIcon(utils.load_svg(':/images/plus.svg', size=QSize(15, 15)))
        self._plus_btn.setIconSize(QSize(15, 15))
        self._plus_btn.setCursor(Qt.PointingHandCursor)
        self._bottom_container.layout().addWidget(self._plus_btn)
        
        self._favorite_btn = QToolButton(self._bottom_container)
        self._favorite_btn.setFixedSize(15, 15)
        self._favorite_btn.setIcon(utils.load_svg(':/images/favorite.svg', size=QSize(15, 15)))
        self._favorite_btn.setIconSize(QSize(15, 15))
        self._favorite_btn.setCursor(Qt.PointingHandCursor)
        self._bottom_container.layout().addWidget(self._favorite_btn)        

class MusicEntry(QFrame):
    
    info = Signal(schemas.MusicSchema)

    def __init__(self, music_obj):
        super(MusicEntry, self).__init__()
        self.setMinimumHeight(60)
        self.setMaximumHeight(60)
        self.setStyleSheet('background-color: rgba(22, 28, 38, 0)')
        
        self.music_obj = music_obj
        self.title = music_obj.title if len(music_obj.title) <= 30 else music_obj.title[:30]+'...'
        self.artist = music_obj.artist if len(music_obj.artist) <= 15 else music_obj.artist[:15]+'...'
        self.album_title = music_obj.album_title if len(music_obj.album_title) <= 17 else music_obj.album_title[:17]+'...'
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
        if(self.cover != None):
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
        self.setStyleSheet('background-color: rgba(22, 28, 38, 0.2)')
        if(not self.loading):
            self._play_btn.show()        
        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        self.setStyleSheet('background-color: rgba(22, 28, 38, 0)')
        self._play_btn.close()        
        return super().leaveEvent(event)
    
    def convert_duration(self, seconds: int):        
        return str(timedelta(seconds=seconds))[2:]
    
    @Slot()
    def send_info(self):
        self.info.emit(self.music_obj)
        
    def update_loading(self, value: bool):
        self.loading = value
    
    @Slot()    
    def _init_loading(self):
        self.loading = True
        self._play_btn.close()
        self._loading_widget.show()
        
    def stop_loading(self):
        self.loading = False
        if not(self._loading_widget.isHidden()):
            self._loading_widget.close()