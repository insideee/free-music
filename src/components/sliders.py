from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt, QTimer, Signal


class CustomSlider(QSlider):
    
    def __init__(self, orientation, parent):
        super(CustomSlider, self).__init__(orientation=orientation, parent=parent)
        self.setMinimumHeight(5)
        self.setMinimum(0)
        self.setMaximum(100)
        
        self._default_style = f"""QSlider::groove:horizontal{{
                                                background: #565C67;
                                                border-radius: 2px;
                                                height: 5px;
                                                position: absolute;
                                                margin: 2px 0;
                                                left: 4px; right: 4px
                                            }}
                                            QSlider::handle:horizontal{{
                                                background: rgba(255, 255, 255, 0);
                                                border: none;
                                                border-radius: 3px;
                                                width: 0px;
                                            }}
                                            QSlider::add-page:horizontal {{
                                                background: #565C67;
                                                border-radius: 2px;
                                                height: 5px;
                                                margin: 2px 0;
                                            }}
                                            QSlider::sub-page:horizontal {{
                                                background: #3B89EE;
                                                border-radius: 2px;
                                                height: 5px;
                                                margin: 2px 0;
                                            }}"""
        self._hover_style = f"""QSlider::groove:horizontal{{
                                                background: #565C67;
                                                border-radius: 4px;
                                                height: 8px;
                                                position: absolute;
                                                margin: 2px 0;
                                                left: 4px; right: 4px
                                            }}
                                            QSlider::handle:horizontal{{
                                                background: rgba(255, 255, 255, 0);
                                                border: none;
                                                border-radius: none;
                                                width: 0px;
                                            }}
                                            QSlider::add-page:horizontal {{
                                                background: #565C67;
                                                border-radius: 4px;
                                                height: 8px;
                                                margin: 4px 0;
                                            }}
                                            QSlider::sub-page:horizontal {{
                                                background: #3B89EE;
                                                border-radius: 4px;
                                                height: 8px;
                                                margin: 2px 0;
                                            }}"""
        self.setStyleSheet(self._default_style)
        
        self.setTickInterval(10)
       
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            x = e.pos().x()
            value = (self.maximum() - self.minimum()) * x / self.width() + self.minimum()
            self.setValue(value)
        else:
            return super().mousePressEvent(e) 
        
    def enterEvent(self, event) -> None:
        self.setStyleSheet(self._hover_style)
        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        self.setStyleSheet(self._default_style)
        return super().leaveEvent(event)
  
        
class DurationSlider(CustomSlider):
    
    update_playback = Signal(int)
    
    def __init__(self, orientation, parent):
        super(DurationSlider, self).__init__(orientation, parent)
        self.setMaximum(1)
        self._timer = QTimer()
        
    def update_maximum(self, value: int):
        self.setMaximum(value)
        
    def update_value(self, value: int):
        self.setValue(value)
    
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            x = e.pos().x()
            value = (self.maximum() - self.minimum()) * x / self.width() + self.minimum()
            self.setValue(value)
            self.update_playback.emit(self.value())
        else:
            return super().mousePressEvent(e)