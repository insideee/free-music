from PySide6.QtWidgets import QFrame, QStyle, QLabel, QVBoxLayout, QGraphicsDropShadowEffect, QToolButton,QHBoxLayout, QPushButton, QCheckBox
from PySide6.QtCore import QSize, Qt, QRect, QPoint, QEvent
from PySide6.QtGui import QGuiApplication, QColor

import utils

class SystemTrayDialog(QFrame):
    
    def __init__(self, parent, info: str, action: QEvent):
        super(SystemTrayDialog, self).__init__(parent=parent)
        
        self.setObjectName('sys_dialog')
        self.setFixedSize(QSize(460, 180))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            self.size(),
            QGuiApplication.primaryScreen().availableGeometry(),
        ))
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(10, 10, 10, 10)        
        
        self.bg_container = QFrame(self)
        self.bg_container.setStyleSheet('background-color: #07303D;\
                           border-radius: 10px')
        self.bg_container.setLayout(QVBoxLayout())
        self.bg_container.layout().setSpacing(0)
        self.bg_container.layout().setContentsMargins(0, 20, 0, 0)
        self.layout().addWidget(self.bg_container)
        self.shadow = QGraphicsDropShadowEffect(self.bg_container)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.bg_container.setGraphicsEffect(self.shadow)
        
        self.information_label = QLabel(self)
        self.information_label.setFixedHeight(40)
        self.information_label.setStyleSheet('background-color: none;\
                                             color: #909090;\
                                             margin-left: 20px')
        self.information_label.setText(f'you are about to {info}'.upper())
        utils.set_font(self.information_label, size=12, medium=True)
        self.information_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.bg_container.layout().addWidget(self.information_label)
        
        self.msg_label = QLabel(self)
        self.msg_label.setStyleSheet('background-color: none;\
                                    color: #565C67;\
                                    margin-left: 20px;\
                                    margin-right: 20px')
        self.msg_label.setText('is this what you really want or minimize to system tray?'.capitalize())
        utils.set_font(self.msg_label, size=12)
        self.msg_label.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.bg_container.layout().addWidget(self.msg_label)
        
        self.bottom_container = QFrame(self)
        self.bottom_container.setFixedHeight(40)
        self.bottom_container.setStyleSheet('background-color: rgba(22, 28, 38, 0.6);\
                                            border-top-right-radius: 0px;\
                                            border-top-left-radius: 0px;\
                                            border-bottom-left-radius: 10px;\
                                            border-bottom-right-radius: 10px')        
        self.bg_container.layout().addWidget(self.bottom_container)
        self.bottom_container.setLayout(QHBoxLayout())
        self.bottom_container.layout().setSpacing(0)
        self.bottom_container.layout().setContentsMargins(0, 0, 0, 0)   
        
        self.check_container = QFrame(self.bottom_container)
        self.check_container.setLayout(QHBoxLayout())
        self.check_container.setStyleSheet('background-color: none')
        self.check_container.layout().setSpacing(0)
        self.check_container.layout().setContentsMargins(20, 0, 0, 0)
        self.check_container.layout().setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.bottom_container.layout().addWidget(self.check_container)  
        
        self.check_box_select = QCheckBox()
        self.check_box_select.setCursor(Qt.PointingHandCursor)
        self.check_box_select.setStyleSheet(f"""QCheckBox{{ background-color: none;
                                                    border: none;
                                                    border-radius: 5px;
                                        }}
                                        QCheckBox::indicator{{
                                                        background-color: none;
                                                        border: 2px solid #565C67;
                                                        width: 13;
                                                        height: 13;
                                                        border-radius: 4px;}}
                                        QCheckBox::indicator::checked{{
                                                            background-color: #565C67;
                                                            image: url(:/images/checked.svg)}}""")
        self.check_box_select.stateChanged.connect(self._remember_check)
        self.check_container.layout().addWidget(self.check_box_select)
        
        self.check_label = QLabel(self)
        self.check_label.setStyleSheet('background-color: none;\
                                    color: #565C67;')
        self.check_label.setText('remember'.capitalize())
        utils.set_font(self.check_label, size=10)
        self.check_label.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.check_container.layout().addWidget(self.check_label)
        
        self.btns_container = QFrame(self.bottom_container)
        self.btns_container.setLayout(QHBoxLayout())
        self.btns_container.setStyleSheet('background-color: none')
        self.btns_container.layout().setSpacing(0)
        self.btns_container.layout().setContentsMargins(0, 0, 0, 0)
        self.btns_container.layout().setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bottom_container.layout().addWidget(self.btns_container)
        
        self.minimize_btn = QPushButton(self)
        self.minimize_btn.setText('minimize'.capitalize())
        self.minimize_btn.setCursor(Qt.PointingHandCursor)
        self.minimize_btn.setFixedSize(QSize(80, 40))
        utils.set_font(self.minimize_btn, size=9, medium=True)
        self.minimize_btn.setStyleSheet('background-color: none;\
                                        color: #909090')
        self.btns_container.layout().addWidget(self.minimize_btn)
        
        self.confirm_btn = QPushButton(self.btns_container)
        self.confirm_btn.setText('confirm'.capitalize())
        self.confirm_btn.setCursor(Qt.PointingHandCursor)
        self.confirm_btn.setFixedSize(QSize(100, 40))
        utils.set_font(self.confirm_btn, size=11, medium=True)
        self.confirm_btn.setStyleSheet('background-color: rgba(22, 28, 38, 0.6);\
                                        border-top-right-radius: 0px;\
                                        border-top-left-radius: 0px;\
                                        border-bottom-left-radius: 0px;\
                                        border-bottom-right-radius: 10px;\
                                        color: #909090')
        self.confirm_btn.clicked.connect(action)
        self.btns_container.layout().addWidget(self.confirm_btn)

        self.exit_btn = QToolButton(self)
        self.exit_btn.setBaseSize(QSize(14, 14))
        self.exit_btn.setStyleSheet('background-color: none;\
                                    border: none')
        self.exit_btn.setFixedSize(self.exit_btn.baseSize())
        self.exit_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.exit_btn.setIcon(utils.load_svg(':/images/exit.svg', size=self.exit_btn.baseSize()))
        self.exit_btn.setIconSize(self.exit_btn.baseSize())
        self.exit_btn.setCursor(Qt.PointingHandCursor)
        self.exit_btn.clicked.connect(self.close)
        self.exit_btn.setGeometry(QRect(QPoint(420, 20),
                                        QSize(self.exit_btn.baseSize())))
        self.show()
    
    def _remember_check(self):
        pass