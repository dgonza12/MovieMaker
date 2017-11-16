"""
Fall 2017 CSc 690 

File: Main.py

Author: Amandeep Kaur & Danny Gonzalez
Last edited: 
"""

import sys
import os
import model
from PyQt5 import QtCore


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
    
    def __init(self,parent):
        super().__init__(parent)
        self.ClipID = 0
       
        
    def mousePressEvent(self, event):
        self.clicked.emit(self)

class Window(QWidget):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        #Define data & Variables:
        self.data = model.ClipModel()
        self.ID = None
        
        #Define Window:
        self.setWindowTitle('Movie Maker')
        self.setGeometry(100, 100, 800, 600)
        #Video Preview:
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.show()
        self.videoWidget.resize(400, 400)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        #Labels
        self.ClipName = QLabel(self)
        
        #Time Line:
        self.TimeLine = QListWidget(self)
        self.TimeLine.setFlow(QListWidget.LeftToRight)
        self.TimeLine.setStyleSheet("background-color: rgb(239,71,111)")
        
        #TextEdits:
        self.projectName = QLineEdit(self)
        self.subtitlesText = QLineEdit(self)
        self.posText = QLineEdit(self)
        
        #Buttons:
        self.Add_btn = QPushButton('Add media', self)
        self.Add_btn.clicked.connect(self.Add_Function)

        self.Render_btn = QPushButton('Render',self)
        self.Render_btn.clicked.connect(self.Render_Function)

        self.Play_btn = QPushButton('play',self)
        self.Play_btn.clicked.connect(self.Play_Function)

        self.Pause_btn = QPushButton('pause',self)
        self.Pause_btn.clicked.connect(self.Pause_Function)

        self.AddSub_btn = QPushButton('add subtitles',self)
        self.AddSub_btn.clicked.connect(self.AddSub_Function)
        
        self.SetPos_btn = QPushButton('set start position',self)
        self.SetPos_btn.clicked.connect(self.SetPos_Function)
        
        #Layouts
        overall_layout = QVBoxLayout()
        first_row = QHBoxLayout()
        second_row = QHBoxLayout()

        effects = QVBoxLayout()
        effects.addWidget(self.ClipName)
        effects.addStretch()
        effects.addWidget(self.subtitlesText)
        effects.addWidget(self.AddSub_btn)
        effects.addWidget(self.posText)
        effects.addWidget(self.SetPos_btn)
        
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
        #overall_layout.addStretch()
        overall_layout.addLayout(second_row)
        self.setLayout(overall_layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        self.show()
        
    def UpdateEffects(self):
        if (self.ID != None):
            Clip = self.data.givemeClip(self.ID)
            self.ClipName.setText(Clip.name)
            self.subtitlesText.setText("")
            self.posText.setText(str (Clip.start))
            
        
    def UpdateTimeline(self):
        self.TimeLine.clear()
        self.data.organizeData()
        for clipy in self.data.data:
            thumb = ClickableLabel(self)
            thumb.clicked.connect(self.mouseSel)
            thumb.ClipID = clipy.clipID
            thumb.setStyleSheet('border: 5px Solid rgb(6,214,160)')
            self.data.makePic(clipy)
            pic = QPixmap("frame.png")
            thumb.setPixmap(pic.scaled(100,100,QtCore.Qt.KeepAspectRatio))
            item = QListWidgetItem()
            item.setSizeHint(thumb.sizeHint())
            self.TimeLine.addItem(item)
            self.TimeLine.setItemWidget(item,thumb)
    
    def Add_Function(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Video files (*.mp4 )")
        if (name[0]!= None):
            print(name[0])
            clip = self.data.createClip(name[0])
            thumb = ClickableLabel(self)
            thumb.clicked.connect(self.mouseSel)
            thumb.ClipID = clip
            pic = QPixmap("frame.png")
            thumb.setPixmap(pic.scaled(100,100,QtCore.Qt.KeepAspectRatio))
            thumb.setStyleSheet('border: 5px Solid rgb(6,214,160)')
            item = QListWidgetItem()
            item.setSizeHint(thumb.sizeHint())
            self.TimeLine.addItem(item)
            self.TimeLine.setItemWidget(item,thumb)

    def Play_Function(self):                   
        if os.path.isfile("TempVideo.mp4"):
            os.remove("TempVideo.mp4")
        if(self.data.IsEmpty() == 0):# 0 is false, 1 is true
            self.Play_btn.setEnabled(False)
            self.data.Preview()
            qmc = QMediaContent(QUrl.fromLocalFile("TempVideo.mp4"))
            self.mediaPlayer.setMedia(qmc)
            self.mediaPlayer.play()
            self.Play_btn.setEnabled(True)
        #Play TempVideo
        
    def Pause_Function(self):
        self.mediaPlayer.pause()
        
    def Render_Function(self):
        if self.projectName.text() != "":
            name = self.projectName.text()
            self.projectName.setText("")
            self.data.Render(name)

    def AddSub_Function(self):
        if (self.ID != None):
            Clip = self.data.givemeClip(self.ID)
            text = self.subtitlesText.text()
            self.data.addText(Clip,text)
            self.UpdateTimeline()
        print("add sub")
        
    def SetPos_Function(self):
        if (self.ID != None):
            Clip = self.data.givemeClip(self.ID)
            Clip.start = int(self.posText.text())
            self.data.organizeData()
            self.UpdateTimeline()
        print("Set Pos")
            
    def mediaStateChanged(self, state):
        print("state chnage");

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        print("error")
        
    def mouseSel(self, label):
        self.ID = label.ClipID
        self.UpdateEffects()
        print(label.ClipID)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
