import sys
import shutil

from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QMouseEvent, QCloseEvent, QIcon, QPixmap

from downloader import Downloader
from search import Search
from resources import resource
from components import SystemTrayDialog
import ui


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self._ui =  ui.AppUi()
        self._ui.init_gui(self)
        
        self._sender = None
        self._music_obj = None
        self._playlist_obj = None
        self._playlist_index = None
        self._stop_download = False
        self._activate_sys_tray = True
        
        self._search = Search()
        self._search.response_received.connect(self._search_response_received)
        
        self._downloader = Downloader()
        self._downloader.download_completed.connect(self._download_receiver)
        
        self._ui.search_entry.returnPressed.connect(self.make_search)
        self._ui.search_page.play_request.connect(self._play_requested)
        self._ui.search_page.playlist_request.connect(self._play_playlist)
        self._ui.player._next_btn.clicked.connect(self._check_worker_busy)
        self._ui.player.check_playlist.connect(self._check_worker_busy)
        
        # title bar btn config
        self._ui.exit_btn.clicked.connect(self._exit_btn_config)
        self._ui.expand_btn.clicked.connect(self._expand_btn_config)
        self._ui.minimize_btn.clicked.connect(self._minimize_btn_config)
        
        # tray icon
        self._ui.tray_icon.activated.connect(self._tray_icon_clicked)
        #self.tray_icon = QSystemTrayIcon(QIcon(QPixmap(':/images/icon.png')), parent=app)
        self.show()
        self._ui._mini_player.show()
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.dragPos = event.globalPosition().toPoint()
        # remove cursor when search lose focus
        focus_widget = QApplication.focusWidget()

        if hasattr(focus_widget, 'objectName'):
            if focus_widget.objectName() == 'search_entry':
                focus_widget.clearFocus()

        return super().mousePressEvent(event)
    
    def _download_receiver(self, data_list: list):
        
        file_data, play, is_playlist = data_list
        
        if(len(file_data) == 2):
            self._music_obj.music_file, self._music_obj.music_file_id = file_data
        
            if is_playlist:
                self._ui.player.add_to_playlist(play, self._music_obj)
                self._add_next_track_playlist()
            else:
                self._ui.player.add_to_playlist(play, self._music_obj)
                    
            if(self._sender != None):
                if(hasattr(self._sender, 'loading')):
                    self._sender.stop_loading() 
            
    def hideEvent(self, event) -> None:
        
        return super().hideEvent(event)
    
    def event(self, event) -> bool:
        #if event.type() == Qt.WindowState.
        return super().event(event)
    
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
    
    def _search_response_received(self, response: dict):
        print('finished')
        self._ui.search_loading.close()
        self._ui.search_page.update_search_page(response) # update for dict
        self._ui.display_container.setCurrentWidget(self._ui.search_page)
        
    def _play_requested(self, data):
        self._music_obj, self._sender = data
        self._downloader.update_title(f'{self._music_obj.title} - {self._music_obj.artist}')
        self._downloader.update_emit_play(True)
        self._downloader.start()
        
    def _play_playlist(self, data: list):
        self._playlist_obj, self._sender = data
        
        if self._playlist_obj.music_list != None:
            self._music_obj = self._playlist_obj.music_list[0]
            self._downloader.update_title(f'{self._playlist_obj.music_list[0].title} - \
                                            {self._playlist_obj.music_list[0].artist}', is_playlist=True)
            self._downloader.update_emit_play(True)
            self._downloader.start()
            self._playlist_index = 0
    
    def _add_next_track_playlist(self, download_next = False):
        if(self._playlist_obj != None and self._playlist_index < len(self._playlist_obj.music_list)):
            if self._playlist_index < 2 or download_next:
                self._music_obj = self._playlist_obj.music_list[self._playlist_index+1]
                self._downloader.update_title(f'{self._music_obj.title} - \
                                            {self._music_obj.artist}', is_playlist=True)
                self._downloader.update_emit_play(False)
                self._downloader.start()
                self._playlist_index += 1    
        elif(self._playlist_index == len(self._playlist_obj.music_list)):
            self._playlist_index = None
            self._playlist_obj = None
            
    def _check_worker_busy(self):
        if(not self._downloader.isRunning()):
            self._add_next_track_playlist(download_next=True)

    def _exit_btn_config(self):
        confirmation_dialog = SystemTrayDialog(self, info='close', action=self.close)
        confirmation_dialog.minimize_btn.clicked.connect(self._minimize_to_tray)
        confirmation_dialog.show()
        
    def _minimize_btn_config(self):
        self.showMinimized()
    
    def _expand_btn_config(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def _minimize_to_tray(self):
        #ensure pop up  is closed before hide
        sender = self.sender().parent()
        for i in range(100):
            sender = sender.parent()
            if hasattr(sender, 'objectName'):
                if sender.objectName() == 'sys_dialog':
                    sender.close()
                    break
                    
        self.hide()
        self._ui.tray_icon.show()
    
    def _tray_icon_clicked(self, reason):
        print('activated', reason)
        if(reason == QSystemTrayIcon.Trigger):
          # show miniplayer
          self._ui._mini_player.show()
          
        elif(reason == QSystemTrayIcon.DoubleClick):
            if(not self.isVisible()):
                self.show()
                self._ui.tray_icon.hide()
     
if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec())
    