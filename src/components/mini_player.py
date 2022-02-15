from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt

class MiniPlayer(QFrame):
    
    def __unit__(self):
        super(MiniPlayer, self).__init__()
        
        self.setObjectName('mini_player')
        self.setWindowTitle('mini player')
        self.setFixedSize(250, 350)
        self.setStyleSheet('background-color: red')
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.close_btn = QPushButton(self)
        self.close_btn.setFixedSize(80, 80)
        self.close_btn.clicked.connect(self.hide)