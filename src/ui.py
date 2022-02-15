from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QLineEdit, QGridLayout, QToolButton, QGraphicsDropShadowEffect, QSystemTrayIcon, QPushButton
from PySide6.QtCore import QSize, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QPixmap, QColor, QIcon

from components import Player, SearchPage, CustomNavMenu, MiniPlayer
import utils

class AppUi(object):
    
    def init_gui(self, app):
        
        # app config
        app.setObjectName('main_app')
        app.setWindowTitle('Free Music')
        app.setWindowIcon(QPixmap(':/images/icon.png'))
        app.resize(QSize(QSize(1200, 750)))
        app.setMinimumSize(QSize(1050, 750)) 
        app.setStyleSheet("background-color: #003847")
        
        app.setWindowFlag(Qt.FramelessWindowHint)
        app.setAttribute(Qt.WA_TranslucentBackground)
        
        def move_window(event):  
            if event.buttons() == Qt.LeftButton:
                app.move(app.pos() + event.globalPos() - app.dragPos)
                app.dragPos = event.globalPos()
                event.accept()
        
        self.tray_icon = QSystemTrayIcon(QIcon(QPixmap(':/images/icon.png')), parent=app)
        self._mini_player = None
        self._mini_player_config()
        
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
        self.bg_container.setStyleSheet('background-color: rgba(0, 56, 71, 1); border-radius: 10px;')
        self.container_layout.addWidget(self.bg_container, 0, 1)
        self.bg_layout = QVBoxLayout(self.bg_container)
        self.bg_layout.setSpacing(0)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)
        self.bg_container.setGraphicsEffect(self.shadow)
        
        self.content_container = QFrame(self.bg_container)
        self.content_container.setObjectName('content_container')
        self.content_container.setStyleSheet('background-color: rgba(22, 28, 38, 0.6); border-radius: 10px;')
        self.bg_layout.addWidget(self.content_container)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignBottom)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # title container
        self.title_bar_container = QFrame(self.content_container)
        self.title_bar_container.setObjectName('title_bar_container')
        self.title_bar_container.setMinimumHeight(70)
        self.title_bar_container.setMaximumHeight(70)
        self.title_bar_container.setFrameShape(QFrame.NoFrame)
        self.title_bar_container.setFrameShadow(QFrame.Raised)
        self.title_bar_container.setStyleSheet('background-color: none;')
        self.title_bar_container.setLayout(QHBoxLayout())
        self.title_bar_container.layout().setSpacing(0)
        self.title_bar_container.layout().setContentsMargins(10, 0, 10, 0)
        self.title_bar_container.mouseMoveEvent = move_window        
        
        self.search_container = QFrame(self.content_container)
        self.search_container.setObjectName('search_container')
        self.search_container.setMinimumHeight(70)
        self.search_container.setMaximumHeight(70)
        self.search_container.setFrameShape(QFrame.NoFrame)
        self.search_container.setFrameShadow(QFrame.Raised)
        self.search_container.setStyleSheet('background-color: none;')
        self.search_layout = QHBoxLayout(self.search_container)
        self.search_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.search_layout.setSpacing(10)
        self.search_container.setContentsMargins(0, 0, 0, 0)
        self.title_bar_container.layout().addWidget(self.search_container)
        
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
        
        self.btns_container = QFrame(self.title_bar_container)
        self.btns_container.setObjectName('btns_container')
        self.btns_container.setFixedSize(QSize(80, 70))
        self.btns_container.setFrameShape(QFrame.NoFrame)
        self.btns_container.setFrameShadow(QFrame.Raised)
        self.btns_container.setStyleSheet('background-color: none;')
        self.btns_layout = QHBoxLayout(self.btns_container)
        self.btns_layout.setAlignment(Qt.AlignCenter)
        self.btns_layout.setSpacing(12)
        self.btns_container.setContentsMargins(0, 0, 0, 0)
        self.title_bar_container.layout().addWidget(self.btns_container)
        
        self.exit_btn = CustomTitleBarBtns(self.btns_container, type='exit',
                                           icon=':/images/exit.svg')
        self.minimize_btn = CustomTitleBarBtns(self.btns_container, type='minimize',
                                               icon=':/images/minimize.svg')
        self.expand_btn = CustomTitleBarBtns(self.btns_container, type='expand',
                                               icon=':/images/expand.svg')
        
        self.btns_layout.addWidget(self.minimize_btn)
        self.btns_layout.addWidget(self.expand_btn)
        self.btns_layout.addWidget(self.exit_btn)
        
        # display container        
        self.display_container = QStackedWidget(self.content_container)
        self.display_container.setObjectName('display_container')
        self.display_container.setMinimumHeight(590)
        self.display_container.setContentsMargins(0, 0, 0, 0)
        self.display_container.setStyleSheet('background-color: none')
        
        self.search_page = SearchPage(self.display_container)
        self.display_container.addWidget(self.search_page)
        self.display_container.setCurrentWidget(self.search_page)
        
        self.player = Player(self.content_container)
        
        self.content_layout.addWidget(self.title_bar_container)
        self.content_layout.addWidget(self.display_container)
        self.content_layout.addWidget(self.player)
        
        app.setCentralWidget(self.container)
        
    def _mini_player_config(self):
        # temp
        self._mini_player = QFrame()
        self._mini_player.setObjectName('mini_player')
        self._mini_player.setWindowTitle('mini player')
        self._mini_player.setFixedSize(250, 350)
        self._mini_player.setStyleSheet('background-color: red')
        self._mini_player.setWindowFlags(Qt.FramelessWindowHint)
        
        self._mini_player.close_btn = QPushButton(parent=self._mini_player)
        self._mini_player.close_btn.setFixedSize(80, 80)
        self._mini_player.close_btn.clicked.connect(self._mini_player.hide)
        
        

class CustomTitleBarBtns(QToolButton):
    
    def __init__(self, parent, type: str, icon: str):
        super(CustomTitleBarBtns, self).__init__(parent=parent)
        
        size = QSize(14,14) 
        icon_size = size if type != 'minimize' else  QSize(14, 2)
        self.setStyleSheet('background-color: none;\
                            border: none')
        self.setFixedSize(size)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setIcon(utils.load_svg(icon, size=icon_size))
        self.setIconSize(icon_size)
        self.setCursor(Qt.PointingHandCursor)
        