import sys
import shutil

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QUrl
from PySide6.QtGui import QMouseEvent, QCloseEvent

from downloader import Downloader
from search import Search
from resources import resource
import ui


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self._ui =  ui.AppUi()
        self._ui.init_gui(self)
        
        self._sender = None
        self._music_obj = None
        
        self._search = Search()
        self._search.response_received.connect(self._search_response_received)
        
        self._downloader = Downloader()
        self._downloader.download_completed.connect(self._download_receiver)
        
        self._ui.search_entry.returnPressed.connect(self.make_search)
        self._ui.search_page.play_request.connect(self._play_requested)
        
    def mousePressEvent(self, event: QMouseEvent) -> None:

        # remove cursor when search lose focus
        focus_widget = QApplication.focusWidget()

        if hasattr(focus_widget, 'objectName'):
            if focus_widget.objectName() == 'search_entry':
                focus_widget.clearFocus()

        return super().mousePressEvent(event)
    
    def _download_receiver(self, data_list: list):
        data_list.append(self._music_obj)
        self._ui.player.add_to_playlist(*data_list)
        if(self._sender != None and self._sender.loading):
            self._sender.stop_loading()
            
    def closeEvent(self, event: QCloseEvent) -> None:
        print('closing')
        if(self._downloader._path != None):
            shutil.rmtree(self._downloader._path)   
        if(self._search.path != None):
            shutil.rmtree(self._search.path)
        return super().closeEvent(event)
    
    def make_search(self):
        self._ui.search_loading.show()
        self._ui.search_entry.clearFocus()
        self._search.update_query(self._ui.search_entry.text())
        self._search.start()
    
    def _search_response_received(self, response: list):
        print('finished')
        self._ui.search_loading.close()
        self._ui.search_page.update_search_page(response)
        self._ui.display_container.setCurrentWidget(self._ui.search_page)
        
    def _play_requested(self, data):
        self._music_obj, self._sender = data
        self._downloader.update_title(self._music_obj.title)
        self._downloader.update_emit_play(True)
        self._downloader.start()

if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
    