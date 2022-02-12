import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtCore import QSize, QUrl, Qt
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from components import Player
from resources import resource


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setMinimumSize(QSize(1200, 750)) 
        self.setStyleSheet("background-color: #003847") 
        
        self.source = QUrl.fromLocalFile("/home/inside/Música/gototown.mp3")
        self.player = Player(self)
        self.player.add_to_playlist(self.source)
        self.source = QUrl.fromLocalFile("/home/inside/Música/doja_cat_all_nighter.mp3")
        self.player.add_to_playlist(self.source)      
        
    def print_duration(self):
        print(self.player.duration())


if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
    