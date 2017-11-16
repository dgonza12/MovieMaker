import sys
import os
from moviepy.editor import *
from moviepy.editor import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip

class Clip():    
    def __init__(self, source):
        self.source = source
        self.name = os.path.splitext(source)[0]
        self.video = VideoFileClip(source)
        print(self.video.duration)
        self.start = 0
        self.clipID = 0

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

    def createClip(self,source):
        self.organizeData()
        newClip = Clip(source)
        newClip.video.save_frame("frame.png")
        self.counter = self.counter + 1
        newClip.clipID = self.counter
        if(self.IsEmpty() == 0):
            lastclip = self.data[len(self.data) - 1]
            newClip.start = lastclip.video.duration + lastclip.start 
        self.data.append(newClip)        
        return (self.counter)

    def addText(self,clip,text):
        vclip = clip.video
        tclip = TextClip(text,fontsize=70,color='white')
        tclip = tclip.set_pos('center').set_duration(vclip.duration)
        clip.video = CompositeVideoClip([vclip,tclip])
    
    def Preview(self):
        videoList = []
        for clip in self.data:
            clip.video.set_start(clip.start)
            videoList.append(clip.video)
        final_clip = CompositeVideoClip(videoList)    
        final_clip.write_videofile("TempVideo.mp4",fps=15)
        
    def Render(self,name):
        videoList = []
        for clip in self.data:
            clip.video.set_start(clip.start)
            videoList.append(clip.video)
        final_clip = CompositeVideoClip(videoList)
        filename = name +".mp4"
        final_clip.write_videofile(filename)
                                            
