import pymysql
import getpass
import time
import MakeVideo, tweet, visiondetection
import argparse

# 'from_my_home': if using from my home setting
# data format
# 'user_name': user's name,
# 'user_time': time using(local time),
# 'keyword': search keyword,
# 'picture_counts': picture counts,
# 'search results': users' name a string with at most 10 users' name,
# 'rate': rate of video,
# 'output name': output filename,
# 'from_my_home': if using from my home setting
if __name__ == '__main__':
    db = pymysql.connect('localhost', 'root', 'luyanghuang', 'mp3')
    cursor = db.cursor()
    sql = "INSERT INTO userinfo(" \
          "user_name,user_time,keyword,picture_counts, search_results," \
          "rate, output_name, from_my_home" \
          ") VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"

    sql2 = 'CREATE TABLE IF NOT EXISTS userinfo(user_name VARCHAR(40) NOT NULL,user_time VARCHAR(40) NOT NULL,keyword VARCHAR(40) NOT NULL,picture_counts VARCHAR(40) NOT NULL,search_results VARCHAR(40) NOT NULL,rate VARCHAR(40) NOT NULL,output_name VARCHAR(40) NOT NULL,from_my_home VARCHAR(40) NOT NULL)'
    cursor.execute(sql2)

    sysname = getpass.getuser()
    systime = time.strftime('%Y.%m.%d %H:%M', time.localtime(time.time()))

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

    user_info = ''.join(list(user_info)[:39])

    res = cursor.execute(sql, (str(sysname), str(systime), str(keyword), str(pic_counts),
                         str(user_info), str(rate), str(output), str(flag)))
    print('Insert successful? ', res)

    db.commit()
    cursor.close()
    db.close()
