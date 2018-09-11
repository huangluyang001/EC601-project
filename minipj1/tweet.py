import tweepy
import requests as rq
from PIL import Image
from io import BytesIO
from skimage import io, transform
import os, math



class GetJpgFromTweet():
    def __init__(self):
        self.consumer_key = 'e5gO5clmQpJIAoV75iylJS0sC'
        self.consumer_secret = 's895ZsN7YamnS5nJgCqPMJo7mPLEik0pSntosubtbX7vS0OZde'
        self.access_token = '1039164455215681541-CCbN18bRzEcqYQ8oGea9hzs8360xky'
        self.access_secret = 'Y9VpDluRCxibATp9QBF5qexGA7SRxJZt3dOl85LdAhT0r'

    @staticmethod
    def GetJpgFromUrl(url, filename):
        #response = rq.get(url)
        #filename = url.split('/')[-1]
        #image = Image.open(BytesIO(response.content))
        #image.show()
        #image.show()
        #image.save(filename, 'JPEG')
        if os.path.exists('image/') != True:
            os.mkdir('image')
        path = 'image/'
        image = io.imread(url)
        height, width = image.shape[:2]
        image = transform.resize(image, (math.floor(height/2)*2, math.floor(width/2)*2))
        io.imsave(path + filename, image)

    def FromMyHome(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)

        api = tweepy.API(auth)

        public_tweets = api.home_timeline(count=50)
        error_count = 0
        true_count = 0
        url_list = []
        for tweet in public_tweets:
            try:
                media = tweet.entities['media']
                #print(media[0]['media_url'])
                url_list.append(media[0]['media_url'])
                true_count += 1
            except KeyError or AttributeError:
                error_count += 1
        print('%d tweets have pictures' %(true_count))
        i = 0
        for url in url_list:
            i += 1
            filename = str(i) + '.jpg'
            self.GetJpgFromUrl(url, filename)


if __name__ == "__main__":
    twitter = GetJpgFromTweet()
    twitter.FromMyHome()