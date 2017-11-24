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
        
        #Labels
        self.ClipName = QLabel(self)
        self.videostartHint = QLabel(self)
        self.videostartHint.setText("Video start time:")
        self.substartHint = QLabel(self)
        self.substartHint.setText("Subtitle start time:")
        self.subendHint = QLabel(self)
        self.subendHint.setText("Subtitle end time:")
        #Time Line:
        self.TimeLine = QListWidget(self)
        self.TimeLine.setFlow(QListWidget.LeftToRight)
        self.TimeLine.setStyleSheet("background-color: rgb(239,71,111)")
        
        #TextEdits:
        self.projectName = QLineEdit(self)
        self.projectName.setText("VideoProject")
        self.subtitlesText = QLineEdit(self)
        self.posText = QLineEdit(self)
        self.substartText = QLineEdit(self)
        self.subendText = QLineEdit(self)
        
        #Buttons:
        self.Add_btn = QPushButton('Add Video', self)
        self.Add_btn.clicked.connect(self.Add_Function)

        self.AddImage_btn = QPushButton('Add Image', self)
        self.AddImage_btn.clicked.connect(self.AddImage_Function)

        self.Render_btn = QPushButton('Render',self)
        self.Render_btn.clicked.connect(self.Render_Function)

        self.Play_btn = QPushButton('play',self)
        self.Play_btn.clicked.connect(self.Play_Function)


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

        effectsrowOne = QHBoxLayout()
        effectsrowOne.addWidget(self.videostartHint)
        effectsrowOne.addWidget(self.posText)
        effectsrowOne.addWidget(self.SetPos_btn)

        effectsrowTwo = QHBoxLayout()      
        effectsrowTwo.addWidget(self.subtitlesText)
        effectsrowTwo.addWidget(self.AddSub_btn)

        effectsrowThree = QHBoxLayout()
        effectsrowThree.addWidget(self.substartHint)
        effectsrowThree.addWidget(self.substartText)
        effectsrowThree.addWidget(self.subendHint)
        effectsrowThree.addWidget(self.subendText)
        
        effects.addLayout(effectsrowOne)
        effects.addLayout(effectsrowTwo)
        effects.addLayout(effectsrowThree)

        
        timelineL = QHBoxLayout()
        timelineL.addWidget(self.TimeLine)
        
        options = QVBoxLayout()
        options.addWidget(self.Play_btn)
        options.addWidget(self.Add_btn)
        options.addWidget(self.AddImage_btn)
        options.addWidget(self.projectName)
        options.addWidget(self.Render_btn)

        first_row.addLayout(effects)


        second_row.addLayout(timelineL)
        second_row.addLayout(options)

        overall_layout.addLayout(first_row)
        #overall_layout.addStretch()
        overall_layout.addLayout(second_row)
        self.setLayout(overall_layout)

       
        
        self.show()
        
    def UpdateEffects(self):
        if (self.ID != None):
            Clip = self.data.givemeClip(self.ID)
            self.ClipName.setText(Clip.name)
            self.subtitlesText.setText("")
            self.substartText.setText("0")
            self.subendText.setText(str (Clip.duration))
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
            clip = self.data.createClip(name[0],0)
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

    def AddImage_Function(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.png *.jpg)")
        if (name[0]!= None):
            print(name[0])
            clip = self.data.createClip(name[0],5)
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
        self.Play_btn.setEnabled(False)
        self.data.Preview()
        self.Play_btn.setEnabled(True)
        

        
    def Render_Function(self):
        if self.projectName.text() != "":
            name = self.projectName.text()
            self.projectName.setText("")
            self.data.Render(name)

    def AddSub_Function(self):
        if (self.ID != None):
            Clip = self.data.givemeClip(self.ID)
            text = self.subtitlesText.text()
            start = float(self.substartText.text())
            end = float(self.subendText.text())
            self.data.addText(Clip,text,start,end)
            self.subtitlesText.setText("")
            self.UpdateTimeline()
        print("add sub")

    def SetPos_Function(self):
        if (self.ID != None):
            Clip = self.data.givemeClip(self.ID)
            Clip.setStart(float(self.posText.text()))
            self.UpdateTimeline()
            
    def mouseSel(self, label):
        self.ID = label.ClipID
        label.setStyleSheet('border: 5px Solid rgb(0,0,255)')
        self.UpdateEffects()
        print(label.ClipID)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

