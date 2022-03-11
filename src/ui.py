from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidgetAction, QVBoxLayout, QStackedWidget, QLabel, QLineEdit, QGridLayout, QToolButton, QGraphicsDropShadowEffect, QSystemTrayIcon, QPushButton, QSizeGrip, QMenu
from PySide6.QtCore import QSize, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QPixmap, QColor, QIcon, QAction

from components import Player, SearchPage, CustomNavMenu, MiniPlayer, TitleBar
import utils


class AppUi(object):

    def init_gui(self, app):

        # app config
        app.setObjectName('main_app')
        app.setWindowTitle('Free Music')
        app.setWindowIcon(QPixmap(':/images/icon.png'))
        app.setMinimumSize(QSize(1200, 750))
        app.setStyleSheet("background-color: #003847")
        app.drag_pos = None
        
        app.setWindowFlag(Qt.FramelessWindowHint)
        app.setAttribute(Qt.WA_TranslucentBackground)

        # tray system
        self._menu = QMenu()
        self.restore_act = QAction('restore'.capitalize())
        self._exit_act = QAction('exit'.capitalize())
        self._exit_act.triggered.connect(lambda: app.close())
        self._menu.addAction(self.restore_act)
        self._menu.addAction(self._exit_act)
        self.tray_icon = QSystemTrayIcon(
            QIcon(QPixmap(':/images/icon.png')), parent=app)
        self.tray_icon.setContextMenu(self._menu)
        self._mp_action = QWidgetAction(self._menu)

        # shadow
        self.shadow = QGraphicsDropShadowEffect(app)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))

        self.container = QFrame(app)
        self.container.setObjectName('main_container')
        self.container.setStyleSheet('background-color: none')
        self.container_layout = QGridLayout(self.container)
        self.container_layout.setSpacing(0)
        self.container_layout.setContentsMargins(10, 10, 10, 10)

        self.nav_menu = CustomNavMenu(self.container)
        self.container_layout.addWidget(self.nav_menu, 0, 0)

        # content container
        self.bg_container = QFrame(self.container)
        self.bg_container.setObjectName('content_container')
        self.bg_container.setStyleSheet(
            'background-color: rgba(0, 56, 71, 1); border-radius: 10px;')
        self.container_layout.addWidget(self.bg_container, 0, 1)
        self.bg_layout = QVBoxLayout(self.bg_container)
        self.bg_layout.setSpacing(0)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)
        self.bg_container.setGraphicsEffect(self.shadow)

        self.content_container = QFrame(self.bg_container)
        self.content_container.setObjectName('content_container')
        self.content_container.setStyleSheet(
            'background-color: rgba(22, 28, 38, 0.6); border-radius: 10px;')
        self.bg_layout.addWidget(self.content_container)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignBottom)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # title container
        self.title_bar = TitleBar(app)

        # display container
        self.display_container = QStackedWidget(self.content_container)
        self.display_container.setObjectName('display_container')
        self.display_container.setMinimumHeight(560)
        self.display_container.setContentsMargins(0, 0, 0, 0)
        self.display_container.setStyleSheet('background-color: none')

        self.search_page = SearchPage(self.display_container)
        self.display_container.addWidget(self.search_page)
        self.display_container.setCurrentWidget(self.search_page)

        self.player = Player(self.content_container)

        self.bottom_container = QFrame(self.bg_container)
        self.bottom_container.setStyleSheet('background-color: none')
        self.bottom_container.setFixedHeight(30)
        self.bottom_container.setLayout(QHBoxLayout())
        self.bottom_container.layout().setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._size_grip = QSizeGrip(self.bottom_container)
        self._size_grip.setFixedSize(QSize(15, 15))
        self._size_grip.setStyleSheet('QSizeGrip { background-color: none;  border-radius: 7px}\
                                        QSizeGrip::hover { background-color: rgba(22, 28, 38, 0.9) }')
        self.bottom_container.layout().addWidget(self._size_grip)

        self.content_layout.addWidget(self.title_bar)
        self.content_layout.addWidget(self.display_container)
        self.content_layout.addWidget(self.player)
        self.content_layout.addWidget(self.bottom_container)

        app.setCentralWidget(self.container)
