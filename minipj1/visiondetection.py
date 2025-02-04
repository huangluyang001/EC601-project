from google.cloud import vision
from google.oauth2 import service_account
import os
import io
import glob
import subprocess

class VisionDetction():
    def __init__(self):
        self.path = 'image'

    @staticmethod
    def SetEnvironment():
        pwd = os.getcwd()
        ly_subprocess = subprocess.Popen(['set','GOOGLE_APPLICATION_CREDENTIALS='+pwd+'\licenseofvision.json'])

    @staticmethod
    def CreateCredentials(filename):
        credentials = service_account.Credentials.from_service_account_file(filename)
        return credentials

    # Get description for pictures using Google Vision
    def GenerateTypes(self):
        #self.SetEnvironment()
        pwd = os.getcwd()
        lcs_filename = pwd+'\licenseofvision.json'
        credentials = self.CreateCredentials(lcs_filename)
        client = vision.ImageAnnotatorClient(credentials=credentials)
        route = os.path.join(os.path.dirname(__file__), self.path)
        filenames = glob.glob(route + '/*.jpg')
        if len(filenames) == 0:
            raise Exception('None pictures found. Try to increase count of homelines or user numbers.')
        elif len(filenames) > 100:
            raise Warning('Too much pictures. May take long time to run.')
        label_dict = {}
        for filename in filenames:
            image = io.open(filename, 'rb')
            content = image.read()
            ly_image = vision.types.Image(content=content)
            response = client.label_detection(image=ly_image)
            labels = response.label_annotations
            count = 0
            label_list= []
            for label in labels:
                #print(label.description)
                label_list.append(label.description)
                count += 1
                if count > 4:
                    break
            number = filename.split('/')[-1].split('\\')[-1].split('.')[0]
            label_dict.setdefault(number, label_list)
        return label_dict

    # make caption for pitures
    @staticmethod
    def MakeSrc(label_dict, rate=1.):
        path = os.path.dirname(__file__)
        f1 = open(path + '/tmp.srt','w')
        time_list = ['00','00','00']
        second = '000'
        time = 0
        for i in range(len(label_dict)):
            labels = ' '.join(label_dict[str(i+1)])
            start_time = ':'.join(time_list) + '.' + second
            time += 1. / rate
            time = round(time, 3)
            print(time)
            time_list[2] , second = str(time).split('.')
            if int(time_list[2]) < 59:
                time_list[2] = str(int(time_list[2]))
            else:
                time_list[1] = str(int(time_list[1])+1)
                time_list[2] = '00'
                time -= 60
            end_time = ':'.join(time_list) + '.' + second
            label_line = ''.join(labels)
            #print(label_line)
            thisline = [str(i+1), start_time + ' --> ' + end_time, label_line]
            thisline = '\n'.join(thisline)
            f1.write(thisline+'\n'+'\n')





# if __name__ == '__main__':
    # vd = VisionDetction()
    # label_dict = vd.GenerateTypes()
    # vd.MakeSrc(label_dict, rate=1)