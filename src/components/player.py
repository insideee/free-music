from PySide6.QtCore import QUrl, QSize, Qt, Slot, QTimer, QObject, QEvent, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QToolButton, QGridLayout, QLabel, QSlider
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from decimal import Decimal

import utils, schemas, search

class CustomSlider(QSlider):
    
    def __init__(self, orientation, parent):
        super(CustomSlider, self).__init__(orientation=orientation, parent=parent)
        self.setMinimumHeight(5)
        self.setMinimum(0)
        self.setMaximum(100)
        
        self._default_style = f"""QSlider::groove:horizontal{{
                                                background: #565C67;
                                                border-radius: 2px;
                                                height: 5px;
                                                position: absolute;
                                                margin: 2px 0;
                                                left: 4px; right: 4px
                                            }}
                                            QSlider::handle:horizontal{{
                                                background: rgba(255, 255, 255, 0);
                                                border: none;
                                                border-radius: 3px;
                                                width: 0px;
                                            }}
                                            QSlider::add-page:horizontal {{
                                                background: #565C67;
                                                border-radius: 2px;
                                                height: 5px;
                                                margin: 2px 0;
                                            }}
                                            QSlider::sub-page:horizontal {{
                                                background: #3B89EE;
                                                border-radius: 2px;
                                                height: 5px;
                                                margin: 2px 0;
                                            }}"""
        self._hover_style = f"""QSlider::groove:horizontal{{
                                                background: #565C67;
                                                border-radius: 4px;
                                                height: 8px;
                                                position: absolute;
                                                margin: 2px 0;
                                                left: 4px; right: 4px
                                            }}
                                            QSlider::handle:horizontal{{
                                                background: rgba(255, 255, 255, 0);
                                                border: none;
                                                border-radius: none;
                                                width: 0px;
                                            }}
                                            QSlider::add-page:horizontal {{
                                                background: #565C67;
                                                border-radius: 4px;
                                                height: 8px;
                                                margin: 4px 0;
                                            }}
                                            QSlider::sub-page:horizontal {{
                                                background: #3B89EE;
                                                border-radius: 4px;
                                                height: 8px;
                                                margin: 2px 0;
                                            }}"""
        self.setStyleSheet(self._default_style)
        
        self.setTickInterval(10)
       
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            x = e.pos().x()
            value = (self.maximum() - self.minimum()) * x / self.width() + self.minimum()
            self.setValue(value)
        else:
            return super().mousePressEvent(e) 
        
    def enterEvent(self, event) -> None:
        self.setStyleSheet(self._hover_style)
        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        self.setStyleSheet(self._default_style)
        return super().leaveEvent(event)
  
        
class DurationSlider(CustomSlider):
    
    update_playback = Signal(int)
    
    def __init__(self, orientation, parent):
        super(DurationSlider, self).__init__(orientation, parent)
        self.setMaximum(1)
        self._timer = QTimer()
        
    def update_maximum(self, value: int):
        self.setMaximum(value)
        
    def update_value(self, value: int):
        self.setValue(value)
    
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            x = e.pos().x()
            value = (self.maximum() - self.minimum()) * x / self.width() + self.minimum()
            self.setValue(value)
            self.update_playback.emit(self.value())
        else:
            return super().mousePressEvent(e)


class Player(QFrame):

    def __init__(self, parent):
        super(Player, self).__init__(parent=parent)
        self.setMaximumHeight(60)
        self.setMinimumHeight(60)
        self.setMinimumWidth(1035)
        self.setStyleSheet('background-color: rgba(22, 28, 38, 0)')
        
        self._main_layout = QHBoxLayout(self)
        self._main_layout.setAlignment(Qt.AlignCenter)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._clear_style = 'background-color: rgba(255, 255, 255, 0); border: none'

        self._playlist = []
        self._playlist_index = -1
        self._music_obj = []
        self._duration = -1
        self._label_duration = Decimal(0.00)
        self._timer = QTimer()
        self._timer.setInterval(100)
        self._timer.timeout.connect(self._update_duration_label)

        #core components
        self._audio_output = QAudioOutput()
        self._audio_output.setVolume(0.2)
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self._player.durationChanged.connect(self._set_duration)
        self._player.playbackStateChanged.connect(
            lambda: self._update_buttons(self._player.playbackState()))
        self._player.playbackStateChanged.connect(self._play_next_track)
        self._player.playbackStateChanged.connect(
            lambda: self._stop_timer(self._player.playbackState()))
        
        # info
        self._info_container = QFrame(self)
        self._info_container.setObjectName('info_container')
        self._info_container.setMinimumSize(QSize(215, 60))
        self._info_container.setMaximumHeight(60)
        self._info_container.setStyleSheet(self._clear_style)
        self._main_layout.addWidget(self._info_container)
        self._info_layout = QHBoxLayout(self._info_container)
        self._info_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._info_layout.setContentsMargins(10, 0, 10, 0)
        self._info_layout.setSpacing(10)
        
        self._cover_label = QLabel(self._info_container)
        self._cover_label.setMinimumSize(QSize(54, 54))
        self._cover_label.setMaximumSize(QSize(54, 54))
        self._cover_label.setScaledContents(True)
        self._info_layout.addWidget(self._cover_label)
        
        self._title_container = QFrame(self._info_container)
        self._title_container.setMinimumHeight(60)
        self._title_container.setMaximumHeight(60)
        self._title_container.setStyleSheet(self._clear_style)
        self._title_layout = QGridLayout(self._title_container)
        self._title_layout.setContentsMargins(0, 5, 0, 5)
        self._title_layout.setSpacing(0)
        self._title_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._info_layout.addWidget(self._title_container)
        
        self._title_label = QLabel(self._title_container)
        self._title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._title_label.setMinimumHeight(30)
        self._title_label.setStyleSheet('color: #909090')
        utils.set_font(self._title_label, size=11, medium=True)
        self._title_layout.addWidget(self._title_label, 0, 0)
        
        self._artist_label = QLabel(self._title_container)
        self._artist_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._artist_label.setMinimumHeight(30)
        self._artist_label.setStyleSheet('color: #565C67')
        utils.set_font(self._artist_label, size=11)
        self._title_layout.addWidget(self._artist_label, 1, 0)

        #controlers
        self._controlers_container = QFrame(self)
        self._controlers_container.setObjectName('controlers_container')
        self._controlers_container.setMinimumSize(QSize(240, 60))
        self._controlers_container.setMaximumSize(QSize(240, 60))
        self._controlers_container.setStyleSheet(self._clear_style)
        self._main_layout.addWidget(self._controlers_container)
        self._controlers_layout = QHBoxLayout(self._controlers_container)
        self._controlers_layout.setAlignment(Qt.AlignCenter)
        self._controlers_layout.setContentsMargins(0, 0, 0, 0)
        self._controlers_layout.setSpacing(0)

        self._play_btn = QToolButton(self._controlers_container)
        self._play_btn.setIcon(utils.load_svg(
            path=':/images/play.svg', size=QSize(45, 45)))
        self._play_btn.setIconSize(QSize(45, 45))
        self._play_btn.setMinimumSize(45, 45)
        self._play_btn.setMaximumSize(45, 45)
        self._play_btn.setCursor(Qt.PointingHandCursor)
        self._play_btn.clicked.connect(
            lambda: self._play_btn_clicked(self._player.playbackState()))
        self._play_btn.setStyleSheet(self._clear_style)

        self._previous_btn = QToolButton(self._controlers_container)
        self._previous_btn.setIcon(utils.load_svg(
            path=':/images/previous.svg', size=QSize(24, 24)))
        self._previous_btn.setIconSize(QSize(24, 24))
        self._previous_btn.setMinimumSize(24, 24)
        self._previous_btn.setMaximumSize(24, 24)
        self._previous_btn.setCursor(Qt.PointingHandCursor)
        self._previous_btn.setStyleSheet(self._clear_style)
        self._previous_btn.clicked.connect(self._play_previous)

        self._next_btn = QToolButton(self._controlers_container)
        self._next_btn.setIcon(utils.load_svg(
            path=':/images/next.svg', size=QSize(24, 24)))
        self._next_btn.setIconSize(QSize(24, 24))
        self._next_btn.setMinimumSize(24, 24)
        self._next_btn.setMaximumSize(24, 24)
        self._next_btn.setCursor(Qt.PointingHandCursor)
        self._next_btn.setStyleSheet(self._clear_style)
        self._next_btn.clicked.connect(self._play_next)

        self._controlers_layout.addWidget(self._previous_btn)
        self._controlers_layout.addWidget(self._play_btn)
        self._controlers_layout.addWidget(self._next_btn)

        # duration container
        self._duration_container = QFrame(self)
        self._duration_container.setObjectName('duration_container')
        self._duration_container.setMinimumSize(QSize(460, 60))
        self._duration_container.setMaximumSize(QSize(460, 60))
        self._duration_container.setStyleSheet(self._clear_style)
        self._main_layout.addWidget(self._duration_container)
        self._duration_layout = QHBoxLayout(self._duration_container)
        self._duration_layout.setAlignment(Qt.AlignCenter)
        self._duration_layout.setContentsMargins(10, 0, 10, 0)
        self._duration_layout.setSpacing(6)

        self._duration_label = QLabel(self._duration_container)
        self._duration_label.setObjectName('duration_label')
        self._duration_label.setText('0:00')
        utils.set_font(self._duration_label, size=10)
        self._duration_label.setStyleSheet('color: #565C67')
        self._duration_layout.addWidget(self._duration_label)

        self._duration_progress = DurationSlider(Qt.Horizontal, self._duration_container)
        self._duration_progress.setObjectName("duration_progress")
        self._duration_progress.update_playback.connect(self._update_playback)
        self._duration_layout.addWidget(self._duration_progress)
        
        # volume
        self._volume_container = QFrame(self)
        self._volume_container.setObjectName('volume_container')
        self._volume_container.setMinimumSize(QSize(120, 60))
        self._volume_container.setMaximumSize(QSize(120, 60))
        self._volume_container.setStyleSheet(self._clear_style)
        self._main_layout.addWidget(self._volume_container)
        self._volume_layout = QHBoxLayout(self._volume_container)
        self._volume_layout.setAlignment(Qt.AlignCenter)
        self._volume_layout.setContentsMargins(10, 0, 10, 0)
        self._volume_layout.setSpacing(6)
        
        self._volume_icon = QLabel(self._volume_container)
        self._volume_icon.setObjectName('volume_icon')
        self._volume_icon.setMaximumSize(QSize(13, 13))
        self._volume_icon.setMinimumSize(QSize(13, 13))
        self._volume_icon.setPixmap(utils.load_svg(
            path=':/images/sound.svg', size=QSize(13, 13)))
        self._volume_icon.setScaledContents(True)
        self._volume_layout.addWidget(self._volume_icon)
        
        self._volume_slider = CustomSlider(orientation=Qt.Horizontal, parent=self._volume_container)
        self._volume_slider.setValue(int(self._audio_output.volume() * 100))
        self._volume_slider.valueChanged.connect(lambda: self._change_volume(self._volume_slider.value()/100))
        self._volume_layout.addWidget(self._volume_slider)
        
    def add_to_playlist(self, url: QUrl, play: bool, music_obj: schemas.MusicSchema):
        self._playlist.append(url)
        self._music_obj.append(music_obj)
        if(self._playlist_index == -1):
            self._playlist_index = 0
            self._update_player_info()
        if(self._player.playbackState() == QMediaPlayer.StoppedState or self._player.playbackState() == QMediaPlayer.PausedState): 
            self._play_btn_clicked(QMediaPlayer.StoppedState)
            
        if(play):
            self._playlist_index = self._playlist_length() -1
            self._update_player_info()
            self._player.play()
            self._reset_label_duration()

    def remove_from_playlist(self, url: QUrl):
        try:
            index = self._playlist.index(url)
            item_removed = self._playlist.pop(index)
        except ValueError:
            item_removed = None
        return item_removed

    def _playlist_length(self):
        return len(self._playlist)

    def playlist_empty(self):
        if (len(self._playlist) != 0):
            return False
        else:
            return True

    def _get_playlist_index(self, url: QUrl):
        try:
            return self._playlist.index(url)
        except ValueError:
            return -1

    def _set_duration(self):
        if (self._player.duration() > 0 or self._playlist_length() <= 0):
            self._duration = self._player.duration()
            self._duration_progress.update_maximum(int(self._duration / 1000))

    def _update_duration_label(self):
        self._label_duration += Decimal(0.001)
        if(str(self._label_duration)[2] == '6'):
            self._label_duration += Decimal(.40)
        self._duration_progress.update_value(int(self._player.position() / 1000))
        self._duration_label.setText(
            f'{str(self._label_duration)[0]}:{str(self._label_duration)[2]}{str(self._label_duration)[3]}')
        
    def _update_playback(self, value: int):
        self._player.setPosition(value * 1000)
        value_to_label = Decimal(value / 100)
        if(len(str(value_to_label)) >= 3):
            if(str(value_to_label)[2] >= '6'):
                value_to_label += Decimal(.40)
                self._duration_label.setText(f'{str(value_to_label)[0]}:{str(value_to_label)[2]}{str(value_to_label)[3]}')
        else:
            self._duration_label.setText(f'{str(value_to_label)[0]}:00')
        self._label_duration = value_to_label
        

    @Slot()
    def _play_btn_clicked(self, state):
        if (state != QMediaPlayer.PlayingState and not self.playlist_empty()):
            self._player.play()
            self._timer.start()
        else:
            self._player.pause()
            self._timer.stop()
        self._update_buttons(self._player.playbackState())

    @Slot()
    def _play_next(self):
        if(self._playlist_index != self._playlist_length() - 1):
            self._playlist_index += 1
            self._update_player_info()
            self._player.play()
            self._reset_label_duration()

    @Slot()
    def _play_previous(self):
        if(self._player.position() <= 5000 and self._playlist_index > 0):
            self._playlist_index -= 1
            self._update_player_info()
            self._player.play()
        else:
            self._player.setPosition(0)
            self._player.play()
        self._reset_label_duration()

    @Slot()
    def _update_buttons(self, state):
        if (state == QMediaPlayer.PlayingState):
            self._play_btn.setIcon(utils.load_svg(
                path=':/images/pause.svg', size=QSize(45, 45)))
        else:
            self._play_btn.setIcon(utils.load_svg(
                path=':/images/play.svg', size=QSize(45, 45)))
            self._stop_timer(self._player.playbackState())

    @Slot()
    def _play_next_track(self):
        if(self._duration > 0 and self._duration <= self._player.position()+50 and self._playlist_index < self._playlist_length()-1):
            self._play_next()
            
    def _stop_timer(self, state):
        if(state == self._player.StoppedState and self._playlist_index == self._playlist_length()-1):
            self._reset_label_duration(stop=True)
     
    def _change_volume(self, volume: float):
        self._audio_output.setVolume(volume)
           
    def _reset_label_duration(self, stop=False):
        self._label_duration = Decimal(0.00)
        self._timer.stop()
        self._timer.setInterval(100)
        if(not stop):
            self._timer.start()
        self._duration_progress.update_value(0)        
        self._duration_label.setText('0:00')
        
    def _update_player_info(self):
        self.path = self._music_obj[self._playlist_index].path
        self._player.setSource(self._playlist[self._playlist_index])
        if(self._music_obj[self._playlist_index].album_cover != None):
            self._cover_label.setPixmap(self._music_obj[self._playlist_index].album_cover)
        else:
            self._cover_label.setPixmap(utils.download_cover(self, album_cover_url=self._music_obj[self._playlist_index].album_cover_url, 
                                 album_title=self._music_obj[self._playlist_index].album_title))
        self._artist_label.setText(self._music_obj[self._playlist_index].artist)
        self._title_label.setText(self._music_obj[self._playlist_index].title.upper())
