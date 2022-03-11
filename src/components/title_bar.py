from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QLineEdit, QToolButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QWindow
from PySide6.QtSvgWidgets import QSvgWidget

import utils

class TitleBar(QFrame):
    """Custom title bar for replace the default system title bar
    """
    
    def __init__(self, parent):
        super(TitleBar, self).__init__(parent=parent)
        self.setObjectName('title_bar_container')
        self.setMinimumHeight(70)
        self.setMaximumHeight(70)
        self.setStyleSheet('background-color: none;')
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(10, 0, 10, 0)       
        
        self.search_container = QFrame(self)
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
        self.layout().addWidget(self.search_container)
        
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
        
        self.btns_container = QFrame(self)
        self.btns_container.setObjectName('btns_container')
        self.btns_container.setFixedSize(QSize(80, 70))
        self.btns_container.setFrameShape(QFrame.NoFrame)
        self.btns_container.setFrameShadow(QFrame.Raised)
        self.btns_container.setStyleSheet('background-color: none;')
        self.btns_layout = QHBoxLayout(self.btns_container)
        self.btns_layout.setAlignment(Qt.AlignCenter)
        self.btns_layout.setSpacing(12)
        self.btns_container.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.btns_container)
        
        self.exit_btn = CustomTitleBarBtns(self.btns_container, type='exit',
                                           icon=':/images/exit.svg')
        self.minimize_btn = CustomTitleBarBtns(self.btns_container, type='minimize',
                                               icon=':/images/minimize.svg')
        self.expand_btn = CustomTitleBarBtns(self.btns_container, type='expand',
                                               icon=':/images/expand.svg')
        
        self.btns_layout.addWidget(self.minimize_btn)
        self.btns_layout.addWidget(self.expand_btn)
        self.btns_layout.addWidget(self.exit_btn)

        # variables
        self.support_system_move = False
        self.window_handle = None

    def set_window_handle(self, window: QWindow) -> None:
        self.window_handle = window
        
    def mouseMoveEvent(self, event) -> None:
        """Handle the window move event if not 
        support the startsystemmove
        """
        if not self.support_system_move:
            app = utils.find_parent(obj=self, target='main_app')
            if app != None:
                if not app.isMaximized():
                    if event.buttons() == Qt.LeftButton:
                        app.move(app.pos() + event.globalPos() - app.drag_pos)
                        app.drag_pos = event.globalPos()
                        event.accept()
        return super().mousePressEvent(event)
    
    def mousePressEvent(self, event) -> None:
        """Move window function using mouse press event
        """
        if self.window_handle != None:
            self.support_system_move = True if self.window_handle.startSystemMove() else False
        return super().mousePressEvent(event)

    
class CustomTitleBarBtns(QToolButton):
    """Custom button for minimize, expand, exit functionality
    """
    
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
        