from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QGraphicsDropShadowEffect, QToolButton, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt, QMargins, QSize, QEvent
from PySide6.QtGui import QColor

import utils
from .sliders import DurationSlider

class MiniPlayer(QFrame):
    
    def __init__(self):
        super(MiniPlayer, self).__init__()
        
        self.setObjectName('mini_player')
        self.setWindowTitle('mini player')
        self.setFixedSize(250, 160)
        self.setStyleSheet('border-radius: 10px')
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(QMargins(10, 10, 10, 10))
        self._clear_style = 'background-color: none'
        
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(20)
        self._shadow.setXOffset(0)
        self._shadow.setYOffset(0)
        self._shadow.setColor(QColor(0, 0, 0, 100))
        
        self._bg_container = QFrame(self)
        self._bg_container.setStyleSheet('background-color: rgba(0, 56, 71, 1)')
        self._bg_container.setLayout(QVBoxLayout())
        self._bg_container.setGraphicsEffect(self._shadow)
        self._bg_container.layout().setSpacing(0)
        self._bg_container.layout().setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout().addWidget(self._bg_container)
        
        self._bg_overlay = QFrame(self._bg_container)
        self._bg_overlay.setStyleSheet('background-color: rgba(22, 28, 38, 0.6)')
        self._bg_overlay.setLayout(QVBoxLayout())
        self._bg_overlay.layout().setSpacing(0)
        self._bg_overlay.layout().setContentsMargins(QMargins(0, 0, 0, 0))
        self._bg_container.layout().addWidget(self._bg_overlay)
        
        self._info_container = QFrame(self._bg_overlay)
        self._info_container.setStyleSheet('background-color: none')
        self._info_container.setFixedHeight(73)
        self._info_container.setLayout(QHBoxLayout())
        self._info_container.layout().setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._info_container.layout().setContentsMargins(10, 0, 10, 0)
        self._info_container.layout().setSpacing(10)
        
        self._cover_label = QLabel(self._info_container)
        self._cover_label.setMinimumSize(QSize(54, 54))
        self._cover_label.setMaximumSize(QSize(54, 54))
        self._cover_label.setStyleSheet('background: red; border-radius: 0px')
        self._cover_label.setScaledContents(True)
        self._info_container.layout().addWidget(self._cover_label)
        
        self._title_container = QFrame(self._info_container)
        self._title_container.setMinimumHeight(60)
        self._title_container.setMaximumHeight(60)
        self._title_container.setStyleSheet(self._clear_style)
        self._title_layout = QGridLayout(self._title_container)
        self._title_layout.setContentsMargins(0, 5, 0, 5)
        self._title_layout.setSpacing(0)
        self._title_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._info_container.layout().addWidget(self._title_container)
        
        self._title_label = QLabel(self._title_container)
        self._title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._title_label.setMinimumHeight(27)
        self._title_label.setStyleSheet('color: #909090')
        self._title_label.setText('teste'.upper())
        utils.set_font(self._title_label, size=11, medium=True)
        self._title_layout.addWidget(self._title_label, 0, 0)
        
        self._artist_label = QLabel(self._title_container)
        self._artist_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._artist_label.setMinimumHeight(27)
        self._artist_label.setText('test'.capitalize())
        self._artist_label.setStyleSheet('color: #565C67')
        utils.set_font(self._artist_label, size=11)
        self._title_layout.addWidget(self._artist_label, 1, 0)
        
        self._duration_container = QFrame(self._bg_overlay)
        self._duration_container.setMinimumHeight(22)
        self._duration_container.setLayout(QHBoxLayout())
        self._duration_container.layout().setAlignment(Qt.AlignCenter)
        self._duration_container.layout().setContentsMargins(10, 0, 10, 0)
        self._duration_container.layout().setSpacing(0)
        self._duration_container.setStyleSheet(self._clear_style)
        
        self._controllers_container = QFrame(self._bg_overlay)
        self._controllers_container.setFixedHeight(45)
        self._controllers_container.setLayout(QHBoxLayout())
        self._controllers_container.layout().setAlignment(Qt.AlignCenter)
        self._controllers_container.layout().setContentsMargins(0, 0, 0, 0)
        self._controllers_container.layout().setSpacing(0)
        self._controllers_container.setStyleSheet(self._clear_style)
        
        self._bg_overlay.layout().addWidget(self._info_container)
        self._bg_overlay.layout().addWidget(self._duration_container)
        self._bg_overlay.layout().addWidget(self._controllers_container)
        
        self.duration_label = QLabel(self._duration_container)
        self.duration_label.setObjectName('duration_label')
        self.duration_label.setText('0:00')
        utils.set_font(self.duration_label, size=9)
        self.duration_label.setStyleSheet('color: #565C67')
        self._duration_container.layout().addWidget(self.duration_label)
        
        self.duration_slider = DurationSlider(Qt.Horizontal, self._bg_overlay)
        self._duration_container.layout().addWidget(self.duration_slider)
        
        self.play_btn = QToolButton(self._controllers_container)
        size = QSize(40, 40)
        self.play_btn.setIcon(utils.load_svg(
            path=':/images/play.svg', size=size))
        self.play_btn.setIconSize(size)
        self.play_btn.setFixedSize(size)
        self.play_btn.setCursor(Qt.PointingHandCursor)
        #self.play_btn.clicked.connect(
        #    lambda: self.play_btn_clicked(self._player.playbackState()))
        self.play_btn.setStyleSheet(self._clear_style)

        self.previous_btn = QToolButton(self._controllers_container)
        self.previous_btn.setIcon(utils.load_svg(
            path=':/images/previous.svg', size=QSize(24, 24)))
        self.previous_btn.setIconSize(QSize(24, 24))
        self.previous_btn.setMinimumSize(24, 24)
        self.previous_btn.setMaximumSize(24, 24)
        self.previous_btn.setCursor(Qt.PointingHandCursor)
        self.previous_btn.setStyleSheet(self._clear_style)
        #self.previous_btn.clicked.connect(self._play_previous)

        self.next_btn = QToolButton(self._controllers_container)
        self.next_btn.setIcon(utils.load_svg(
            path=':/images/next.svg', size=QSize(24, 24)))
        self.next_btn.setIconSize(QSize(24, 24))
        self.next_btn.setMinimumSize(24, 24)
        self.next_btn.setMaximumSize(24, 24)
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(self._clear_style)
        #self.next_btn.clicked.connect(self._play_next)
        
        self._controllers_container.layout().addWidget(self.previous_btn)
        self._controllers_container.layout().addWidget(self.play_btn)
        self._controllers_container.layout().addWidget(self.next_btn)
    
    def mousePressEvent(self, event) -> None:
        print('pressed')
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event) -> None:
        if not self.isMaximized():
            self._drag_pos = event.globalPosition().toPoint()
            print(self.parent())
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + (event.globalPos() - self._drag_pos))
                event.accept()
           
        return super().mousePressEvent(event)
    
    def mousePressEvent(self, event) -> None:
        self.setCursor(Qt.ClosedHandCursor)
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event) -> None:
        self.setCursor(Qt.ArrowCursor)
        return super().mouseReleaseEvent(event)
         
    def event(self, event) -> bool:
        if not self.isHidden() and event.type() == QEvent.Type.WindowDeactivate:
            self.hide()
        return super().event(event)
    