from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QLineEdit, QGridLayout
from PySide6.QtCore import QSize, Qt
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