import subprocess, os


class MakeVideo():
    def __init__(self):
        self.exepath = os.path.dirname(__file__)
        self.path = 'image/'
        self.file = ['ffmpeg']
        self.y = ['-y']
        self.rate = ['-r','1']
        self.input = ['-i',self.path + '%d.jpg']
        self.music = ['-i', 'music.mp3']
        self.src = ['-vf', 'subtitles='+'tmp.srt']
        self.output = ['final.mkv']
        self.t = ['-t', '40']

    def makevideo(self, rate=1, output_dir='final.mkv'):
        #print(self.file)
        self.output[0] = output_dir
        self.rate[1] = str(rate)
        args = self.file + self.y + self.rate\
               + self.input + self.src + self.output
        #print(' '.join(args))
        ly_process = subprocess.Popen(args)


if __name__ == '__main__':
    mv = MakeVideo()
    mv.makevideo(rate=2, output_dir='final.mkv')
