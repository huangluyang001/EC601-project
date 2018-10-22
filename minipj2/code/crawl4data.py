from skimage import io, transform
from bs4 import BeautifulSoup as bs
import logging
import re
from selenium import webdriver
import os
import time

baseurl = 'https://www.bing.com/images/search?q='
baseurl2 = '&FORM=HDRSC2'
query = 'sportscar'

class Crawl:
    def __init__(self):
        self.url = baseurl + query + baseurl2
        self.height = 256
        self.width = 256

    # Start Search and download
    def downloadImg(self):
        chrome = webdriver.Chrome('chromedriver.exe')
        chrome.get(self.url)
        path = 'data/'
        if not os.path.exists(path):
            os.makedirs(path)

        # record image url and avoid same image
        image_set = set()

        #reference: https://blog.csdn.net/wobeatit/article/details/79559314
        position = 0
        for i in range(200):
            position += 500
            js = "document.documentElement.scrollTop=%d" % position
            chrome.execute_script(js)
            time.sleep(1)
            html = chrome.page_source
            soup = bs(html, 'html.parser')
            for urlpath in soup.select('.mimg'):
                try:
                    link = urlpath.attrs['src']
                except KeyError:
                    continue
                if link not in image_set:
                    target = path + query + '_' + str(len(image_set)) + '.jpg'
                    try:
                        image = io.imread(link)
                        image_set.add(link)
                        image = transform.resize(image, (self.height, self.width))
                        image = image[:, :, :3]
                        io.imsave(target, image)
                        print('Finish ' + str(len(image_set) + 1) + ' pictures')
                    except FileNotFoundError and OSError:
                        continue
                if len(urlpath) == 1000:
                    break

            time.sleep(1)



if __name__ == '__main__':
    crawl = Crawl()
    crawl.downloadImg()

