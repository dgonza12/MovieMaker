"""
Fall 2017 CSc 690 

File: Main.py

Author: Amandeep Kaur & Danny Gonzalez
Last edited: 
"""

import sys
import os
import model

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QSlider, QListWidgetItem ,QLabel, QListView, QListWidget, QWidget, QScrollArea,QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QApplication, QFileDialog
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ClickableLabel(QLabel):
    # when QLabel is clicked, emit a signal with a str parameter
    clicked = pyqtSignal(QLabel)
    
    def __init(self, parent):
        super().__init__(parent)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self)

class Window(QWidget):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        #Define data:
        self.data = model.ClipModel()
        
        #Define Window:
        self.setWindowTitle('Movie Maker')
        self.setGeometry(100, 100, 800, 600)
        #Video Preview:
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.resize(400, 300)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.videoWidget.show()
        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        
        #Time Line:
        self.TimeLine = QListWidget(self)
        self.TimeLine.setFlow(QListWidget.LeftToRight)
        self.TimeLine.setStyleSheet("background-color: rgb(239,71,111)")
        
        #TextEdits:
        self.projectName = QLineEdit(self)
        
        #Buttons:
        self.Add_btn = QPushButton('Add media', self)
        self.Add_btn.clicked.connect(self.Add_Function)

        self.Render_btn = QPushButton('Render',self)
        self.Render_btn.clicked.connect(self.Render_Function)

        self.Play_btn = QPushButton('play',self)
        self.Play_btn.clicked.connect(self.Play_Function)

        self.Pause_btn = QPushButton('pause',self)
        self.Pause_btn.clicked.connect(self.Pause_Function)


        #Layouts
        overall_layout = QVBoxLayout()
        first_row = QHBoxLayout()
        second_row = QHBoxLayout()

        effects = QHBoxLayout()
        
        preview = QVBoxLayout()
        preview.addWidget(self.videoWidget)
        preview.addWidget(self.Play_btn)
        preview.addWidget(self.Pause_btn)
        preview.addWidget(self.positionSlider)
        
        timelineL = QHBoxLayout()
        timelineL.addWidget(self.TimeLine)
        
        options = QVBoxLayout()
        options.addWidget(self.Add_btn)
        options.addWidget(self.projectName)
        options.addWidget(self.Render_btn)

        first_row.addLayout(effects)
        first_row.addLayout(preview)

        second_row.addLayout(timelineL)
        second_row.addLayout(options)

        overall_layout.addLayout(first_row)
        overall_layout.addStretch()
        overall_layout.addLayout(second_row)
        self.setLayout(overall_layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        self.show()
        
    def Add_Function(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Video files (*.mp4 )")
        if (name[0]!= None):
            print(name[0])
            self.data.createClip(name[0])
            thumb = ClickableLabel(self)
            thumb.clicked.connect(self.mouseSel)
            #pic = QPixmap(photo_name)
            #thumb.setPixmap(pic)
            thumb.setText(name[0])
            thumb.setStyleSheet('border: 5px Solid rgb(6,214,160)')
            item = QListWidgetItem()
            item.setSizeHint(thumb.sizeHint())
            self.TimeLine.addItem(item)
            self.TimeLine.setItemWidget(item,thumb)

    def Play_Function(self):                   
        if os.path.isfile("TempVideo.mp4"):
            os.remove("TempVideo.mp4")
        self.data.Preview()
        qmc = QMediaContent(QUrl.fromLocalFile("TempVideo.mp4"))
        self.mediaPlayer.setMedia(qmc)
        #Play TempVideo
        
    def Pause_Function(self):
        self.mediaPlayer.play()
        
    def Render_Function(self):
        if self.projectName.text() != "":
            name = self.projectName.text()
            self.projectName.setText("")
            self.data.Render(name)
            
    def mediaStateChanged(self, state):
        print("state chnage");

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.Play_btn.setEnabled(False)
        
    def mouseSel(self, label):
        print(label.text())
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
