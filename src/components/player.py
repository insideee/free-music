import sys

from PySide6.QtCore import QUrl, QSize, Qt, Slot, QTimer
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QToolButton, QProgressBar, QLabel, QSlider
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from decimal import Decimal

import utils

class CustomSlider(QSlider):
    
    def __init__(self, orientation, parent):
        super(CustomSlider, self).__init__(orientation=orientation, parent=parent)
        self.setMinimumHeight(5)
        self.setMinimum(0)
        self.setMaximum(100)
        
        self.setStyleSheet(f"""QSlider::groove:horizontal{{
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
                                            }}""")
        
        self.setTickInterval(10)
        
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            x = e.pos().x()
            value = (self.maximum() - self.minimum()) * x / self.width() + self.minimum()
            self.setValue(value)
        else:
            return super().mousePressEvent(self, e) 

class Player(QFrame):

    def __init__(self, parent):
        super(Player, self).__init__(parent=parent)
        self.setMaximumHeight(60)
        self.setMinimumHeight(60)
        self.setMinimumWidth(1035)
        self.setStyleSheet('background-color: rgba(22, 28, 38, 0.6)')
        self._main_layout = QHBoxLayout(self)
        self._main_layout.setAlignment(Qt.AlignCenter)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._clear_style = 'background-color: rgba(255, 255, 255, 0); border: none'

        self._playlist = []
        self._playlist_index = -1
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
        
        # info
        self._info_container = QFrame(self)
        self._info_container.setObjectName('info_container')
        self._info_container.setMinimumSize(QSize(215, 60))
        self._info_container.setMaximumSize(QSize(215, 60))
        self._info_container.setStyleSheet(self._clear_style)
        self._main_layout.addWidget(self._info_container)
        self._info_layout = QHBoxLayout(self._info_container)
        self._info_layout.setAlignment(Qt.AlignCenter)
        self._info_layout.setContentsMargins(0, 0, 0, 0)
        self._info_layout.setSpacing(0)

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

        self._duration_progress = QProgressBar(self._duration_container)
        self._duration_progress.setObjectName("duration_progress")
        self._duration_progress.setMaximumSize(QSize(16777215, 5))
        self._duration_progress.setStyleSheet("""QProgressBar {
                                                    background-color: #565C67;
                                                    color: rgba(200, 200, 200, 0);
	                                                border: none;
                                                    border-radius: 2px;
                                                    }
                                                QProgressBar::chunk {
	                                                background-color: #3B89EE;
	                                                border: none;
                                                    border-radius: 2px;
                                                }""")
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

    def add_to_playlist(self, url: QUrl):
        self._playlist.append(url)
        if(self._playlist_index == -1):
            self._playlist_index = 0
            self._player.setSource(self._playlist[self._playlist_index])

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
            self._duration_progress.setRange(0, self._duration / 1000)

    def _update_duration_label(self):
        self._label_duration += Decimal(0.001)
        if(str(self._label_duration)[2] == '6'):
            self._label_duration += Decimal(.40)
        self._duration_progress.setValue(self._player.position() / 1000)
        self._duration_label.setText(
            f'{str(self._label_duration)[0]}:{str(self._label_duration)[2]}{str(self._label_duration)[3]}')

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
            self._player.setSource(self._playlist[self._playlist_index])
            self._player.play()
            self._reset_label_duration()

    @Slot()
    def _play_previous(self):
        if(self._player.position() <= 5000 and self._playlist_index > 0):
            self._playlist_index -= 1
            self._player.pause()
            self._player.setSource(self._playlist[self._playlist_index])
            self._player.play()
        else:
            self._player.setPosition(0)
            self._player.pause()
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

    @Slot()
    def _play_next_track(self):
        if(self._duration > 0 and self._duration == self._player.position()):
            self._play_next()
     
    def _change_volume(self, volume: float):
        self._audio_output.setVolume(volume)
           
    def _reset_label_duration(self):
        self._label_duration = Decimal(0.00)
        self._timer.stop()
        self._timer.setInterval(100)
        self._timer.start()
        self._duration_progress.setValue(0)        
        self._duration_label.setText('0:00')
