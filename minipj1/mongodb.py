from pymongo import MongoClient
import getpass
import time
import MakeVideo, tweet, visiondetection
import argparse


# This code can generate video as well as saving data in mongodb
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

    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--rate',required=False,type=float,default=1,help='number of pictures per minute, default=1')
    parser.add_argument('-o','--output',required=False,type=str,default='final.mkv',help='output filename and directory, should be .mkv default=final.mkv')
    parser.add_argument('-k','--keyword',required=False,type=str,default='jerry',help='search keyword default=messi')
    parser.add_argument('-c','--count',required=False, type=int,default=200,help='number of homline in each user, no larger than 20')
    parser.add_argument('-n',required=False,type=int,default=10,help='number of users to get from the same keyword, no larger than 200')
    parser.add_argument('-m',type=bool,required=False,help='grap from my homeline')
    args = parser.parse_args()
    try:rate = float(args.rate)
    except:rate=1.0
    try:output = args.output
    except:output = 'final.mkv'
    try:keyword = args.keyword
    except:keyword='jerry'
    try:count = int(args.count)
    except:count=200
    try:num = int(args.n)
    except:num=10

    #logging.info(print(rate, output,keyword,str(count),str(num)))

    twitter = tweet.GetJpgFromTweet()
    vd = visiondetection.VisionDetction()
    mv = MakeVideo.MakeVideo()
    if args.m == True:
        twitter.FromMyHome(count=count)
        pic_counts = count
        user_info = 'my_home'
        flag = True
    else:
        user_info, pic_counts = twitter.FromSpecificUser(keyword=keyword,count=count, numofuser=num)
        print(user_info, pic_counts)
        flag = False
    label_dict = vd.GenerateTypes()
    vd.MakeSrc(label_dict, rate=rate)
    mv.makevideo(rate=rate, output_dir=output)

    info = {
        'user_name': sysname,
        'use_time': systime,
        'keyword': keyword,
        'picture_counts': pic_counts,
        'search results': user_info,
        'rate': rate,
        'output name': output,
        'from_my_home': str(flag)
    }
    myset.insert_one(info)
    result = myset.find_one({'user_name': 'luyang'})
    print(result)





