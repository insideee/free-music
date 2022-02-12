import sys
import shutil

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QUrl
from PySide6.QtGui import QMouseEvent, QCloseEvent

from downloader import Downloader
from resources import resource
import ui


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self._ui =  ui.AppUi()
        self._ui.init_gui(self)
        
        self._downloader = Downloader()
        self._downloader.download_completed.connect(self._download_receiver)
        self._downloader.update_title('Doja cat Say So')
        self._downloader.start()
        
        self._source = None
        
    def mousePressEvent(self, event: QMouseEvent) -> None:

        # remove cursor when search lose focus
        focus_widget = QApplication.focusWidget()

        if hasattr(focus_widget, 'objectName'):
            if focus_widget.objectName() == 'search_entry':
                focus_widget.clearFocus()

        return super().mousePressEvent(event)
    
    def _download_receiver(self, url: QUrl):
        self._source = url
        
        if(self._source != None):
            self._ui.player.add_to_playlist(self._source)
            
    def closeEvent(self, event: QCloseEvent) -> None:
        if(self._downloader._path != None):
            shutil.rmtree(self._downloader._path)
        return super().closeEvent(event)

if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
    