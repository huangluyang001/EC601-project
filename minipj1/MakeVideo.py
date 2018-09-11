import subprocess, os


class MakeVideo():
    def __init__(self):
        self.exepath = os.path.dirname(__file__)
        self.path = 'image/'
        self.file = ['ffmpeg']
        self.y = ['-y']
        self.rate = ['-r','1']
        self.input = ['-i',self.path + '%d.jpg']
        self.music = ['-i', '1.mp4']
        self.src = ['-vf', 'subtitles='+'tmp.srt']
        self.output = ['final.mkv']

    def makevideo(self):
        #print(self.file)
        args = self.file + self.y + self.rate + self.input + self.src + self.output
        ly_process = subprocess.Popen(args)


if __name__ == '__main__':
    mv = MakeVideo()
    mv.makevideo()
