import pymysql
import getpass
import time
import MakeVideo, tweet, visiondetection
import argparse

# 'from_my_home': if using from my home setting
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
    db = pymysql.connect('localhost', 'root', 'luyanghuang', 'mp3')
    cursor = db.cursor()
    sql = "SELECT * FROM userinfo"
    cursor.execute(sql)
    results = cursor.fetchall()
    print('# of information: ', len(results))
    name_dict_count = {}
    kw_dict_count = {}
    for result in results:
        try:
            name_dict_count[result[0]] += 1
        except:
            name_dict_count.setdefault(result[0], 1)
        try:
            kw_dict_count[result[2]] += 1
        except:
            kw_dict_count.setdefault(result[2], 1)
    name_dict_sorted = sorted(name_dict_count.items(), key=lambda x:x[1], reverse=True)
    kw_dict_sorted = sorted(kw_dict_count.items(), key=lambda x: x[1], reverse=True)
    print('most common user and count: ', name_dict_sorted[0][0], name_dict_sorted[0][1])
    print('most common keyword and count: ', kw_dict_sorted[0][0], name_dict_sorted[0][1])


    parser = argparse.ArgumentParser()
    parser.add_argument('-w','--keyword',required=False,type=str,default='*',help='search for certain keyword')
    args = parser.parse_args()

    keyword = args.keyword
    sql = "SELECT %s FROM userinfo" %keyword
    cursor.execute(sql)
    results = cursor.fetchall()
    print('# of information under your keyword: ', len(results))
    name_dict_count = {}
    kw_dict_count = {}
    for result in results:
        try:
            name_dict_count[result[0]] += 1
        except:
            name_dict_count.setdefault(result[0], 1)
        try:
            kw_dict_count[result[2]] += 1
        except:
            kw_dict_count.setdefault(result[2], 1)
    name_dict_sorted = sorted(name_dict_count.items(), key=lambda x:x[1], reverse=True)
    kw_dict_sorted = sorted(kw_dict_count.items(), key=lambda x: x[1], reverse=True)
    print('most common user and count under your keyword: ', name_dict_sorted[0][0], name_dict_sorted[0][1])
    print('most common keyword and count under your keyword: ', kw_dict_sorted[0][0], name_dict_sorted[0][1])