import glob
import cv2
import numpy as np
import logging


# Input 3*224*224 Output 2 dimension one-hot label
class Preprocess():
    def __init__(self):
        self.data_folder = 'data/'
        self.data_dict = {
            'image' : [],
            'label' : []
        }

    def read_image(self):
        filenames = glob.glob(self.data_folder+'*.jpg')
        for filename in filenames:
            image = cv2.imread(filename, cv2.IMREAD_COLOR)
            image = cv2.resize(image, (224,224))
            self.data_dict['image'].append(np.array(image))
            label = filename.split('\\')[-1].split('_')[0]
            if label == 'sportscar':
                label = 0
            elif label == 'SUV':
                label = 1
            else:
                raise Exception
            self.data_dict['label'].append(label)
        self.data_dict['image'] = np.array(self.data_dict['image']).swapaxes(1, 3)
        self.data_dict['label'] = np.array(self.data_dict['label'])
        assert len(self.data_dict['image']) == len(self.data_dict['label'] )
        return self.data_dict



if __name__ == '__main__':
    pass
    #usage
    #preprocess = Preprocess()
    # data_dict = preprocess.read_image

