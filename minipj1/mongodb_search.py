from pymongo import MongoClient
import getpass
import time
import MakeVideo, tweet, visiondetection
import argparse

# This file can be used to search
# data format
# 'user_name': user's name,
# 'use_time': time using(local time),
# 'keyword': search keyword,
# 'picture_counts': picture counts,
# 'search results': users' name a string with at most 10 users' name,
# 'rate': rate of video,
# 'output name': output filename,
# 'from_my_home': if using from my home setting
if __name__ == '__main__':
    conn = MongoClient('localhost', 27017)
    db = conn.minipj3
    sysname = getpass.getuser()
    systime = time.strftime('%Y.%m.%d %H:%M', time.localtime(time.time()))
    myset = db.useinfo

    # count
    count = myset.find().count()
    print('# of information: ', count)
    # search for certain keywords
    # results = myset.find('luyang')
    # print(results)
    # most popular keyword
    results = myset.find()
    name_dict_count = {}
    kw_dict_count = {}
    for result in results:
        try:
            name_dict_count[result['user_name']] += 1
        except:
            name_dict_count.setdefault(result['user_name'], 1)
        try:
            kw_dict_count[result['keyword']] += 1
        except:
            kw_dict_count.setdefault(result['keyword'], 1)
    name_dict_sorted = sorted(name_dict_count.items(), key=lambda x:x[1], reverse=True)
    kw_dict_sorted = sorted(kw_dict_count.items(), key=lambda x: x[1], reverse=True)
    print('most common user and count: ', name_dict_sorted[0][0], name_dict_sorted[0][1])
    print('most common keyword and count: ', kw_dict_sorted[0][0], name_dict_sorted[0][1])

    parser = argparse.ArgumentParser()
    parser.add_argument('-k','--key',required=False,type=str,default='user_name',help='search for a certain key, choosing from user_name, use_time, keyword, search results, rate, output name, from_my_home')
    parser.add_argument('-w','--keyword',required=False,type=str,default='.*',help='search for certain keyword')
    args = parser.parse_args()

    key = args.key
    keyword = args.keyword

    results = myset.find({key: {'$regex': keyword}})
    print('Search results: ')
    for result in results:
        print(result)