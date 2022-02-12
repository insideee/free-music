from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QLineEdit
from PySide6.QtCore import QSize, Qt

from components import Player, SearchPage
import utils

class AppUi(object):
    def init_gui(self, app):
        
        # app config
        app.setObjectName('main_app')
        app.setWindowTitle('Free Music')
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
        self.container_layout.addWidget(self.nav_container)
         
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
        self.search_entry.setMinimumSize(QSize(180, 20))
        self.search_entry.setMaximumSize(QSize(180, 20))
        utils.set_font(self.search_entry, size=11)
        self.search_entry.setStyleSheet('color: #909090;\
                                        border: none;\
                                        background-color: rgba(0, 0, 0, 0)')
        self.search_layout.addWidget(self.search_entry)
        
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