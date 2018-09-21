import tweepy
import requests as rq
from PIL import Image
from io import BytesIO
from skimage import io, transform
import os, math
import shutil, logging, time



class GetJpgFromTweet():
    def __init__(self):
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token = ''
        self.access_secret = ''
        if os.path.exists('image/') == True:
            shutil.rmtree('image')
        time.sleep(1)
        os.mkdir('image')

    # Get pictures from homelines of a user
    @staticmethod
    def GetJpgFromUrl(url, filename):
        #response = rq.get(url)
        #filename = url.split('/')[-1]
        #image = Image.open(BytesIO(response.content))
        #image.show()
        #image.show()
        #image.save(filename, 'JPEG')
        path = 'image/'
        image = io.imread(url)
        height, width = image.shape[:2]
        if height < width:
            image = transform.resize(image, (math.floor(height/2)*2, math.floor(height/2)*2))
        else:
            image = transform.resize(image, (math.floor(height / 2) * 2, math.floor(width / 2) * 2))
        io.imsave(path + filename, image)

    # Get pictures from developer's homeline
    def FromMyHome(self, count=100):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)

        api = tweepy.API(auth)

        public_tweets = api.home_timeline(count=count)
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

    # Input keywords and count, search pictures from users' homelines.
    def FromSpecificUser(self, keyword='Messi', numofuser=5, count=100):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)

        api = tweepy.API(auth)

        users = api.search_users(keyword, page=math.ceil(numofuser/20), per_page=numofuser)
        logging.info('num of users:{num}'.format(num=len(users)))
        user_list = []
        for i in range(numofuser):
            try:
                user_list.append(users[i].name)
            except IndexError:
                print('Userss are not enough, only {number} users are found'.format(number=i))
                break
            print('No.{number} User id: {name}'.format(number=i, name=users[i].id))
            print('No.{number} User {name}: '.format(number=i, name=users[i].name))
            print('No.{number} User screenname: {name}'.format(number=i,name=users[i].screen_name))

        error_count = 0
        true_count = 0
        url_list = []
        if len(user_list) == 0:
            raise Exception('No valid users found, please change keyword.')
        for j in range(len(user_list)):
            name = user_list[j]
            try:
                public_tweets = api.user_timeline(screen_name=name, count=count)
            except Exception:
                print('user {name} doesn\'t have timeline.'.format(name=name))
                continue
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






#
# if __name__ == "__main__":
    # logging.basicConfig(level='INFO')
    # twitter = GetJpgFromTweet()
    # #twitter.FromMyHome()
    # twitter.FromSpecificUser(keyword='ronaldo',count=100, numofuser=50)