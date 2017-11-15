from moviepy.editor import *
from moviepy.editor import VideoFileClip

class Clip():    
    def __init__(self, source):
        self.source = source
        self.video = VideoFileClip(source)
        self.start = 0

class ClipModel():
    def __init__(self):
        self.data = []# 'Clip' objects will be stored here

    def organizeData(self):
        self.data.sort(key = lambda Clip: Clip.start)

    def createClip(self,source):
        newClip = Clip(source)
        self.data.append(newClip)
        
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
                                            
