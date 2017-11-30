import sys
import os
from moviepy.editor import *
from moviepy.editor import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip



class Clip():    
    def __init__(self, source, IsImage):
        self.source = source
        self.name = os.path.splitext(source)[0]
        
        if(IsImage != 0):
            print("it's an image")
            self.video = ImageClip(source)
            self.duration = IsImage
            self.video.set_duration(IsImage)
            
        else:
            self.video = VideoFileClip(source)
            self.duration = self.video.duration
            
        self.start = 0
        self.end = self.start + self.duration
        self.clipID = 0
        print("Video Duration:"+str(self.duration))
        
    def setStart(self,start):
        self.start = start
        self.end = self.start + self.duration
        print("start time changed!")

class ClipModel():
    
    def __init__(self):
        self.data = []# 'Clip' objects will be stored here
        self.counter = 0# this is used to generate unique ID's for the clips

    def IsEmpty(self):
        if(len(self.data)==0):
            return 1
        else:
            return 0

    def makePic(self,clip):
        clip.video.save_frame("frame.png")

    def givemeClip(self,clipid):
        for clip in self.data:
            if(clip.clipID == clipid):
                return clip

    def organizeData(self):
        self.data.sort(key = lambda Clip: Clip.start)

    def createClip(self,source,IsImage):
        self.organizeData()
        newClip = Clip(source,IsImage)
        newClip.video.save_frame("frame.png")
        self.counter = self.counter + 1
        newClip.clipID = self.counter
        if(self.IsEmpty() == 0):
            lastclip = self.data[len(self.data) - 1]
            newClip.setStart(lastclip.end)  
        self.data.append(newClip)        
        return (self.counter)

    def getSpacing(self,clip):
        index = self.data.index(clip)
        if(index < (len(self.data) - 1)):
           nextClip = self.data[index + 1]
           return (nextClip.start - clip.end)
        else:
           return 0

    def Remove(self,clip):
        self.data.remove(clip)
        self.organizeData()
    
    def addText(self,clip,text,s,e):
        vclip = clip.video
        tclip = TextClip(text,fontsize=70,color='white')
        d = e-s
        tclip = tclip.set_pos('center').set_duration(d)
        clip.video = CompositeVideoClip([vclip,tclip.set_start(s)])
    
    def Preview(self):
        videoList = []
        for clip in self.data:
            videoList.append(clip.video.set_start(clip.start).set_duration(clip.duration).set_pos("center"))
        final_clip = CompositeVideoClip(videoList)
        final_clip.write_videofile("preview.mp4",fps=13,codec='libx264')
        final_clip = VideoFileClip("preview.mp4")
        final_clip.preview()
        
        
    def Render(self,name):
        videoList = []
        for clip in self.data:
            videoList.append(clip.video.set_start(clip.start).set_duration(clip.duration).set_pos("center"))
        final_clip = CompositeVideoClip(videoList)
        filename = name +".mp4"
        final_clip.write_videofile(filename,fps=24)

