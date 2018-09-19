import MakeVideo, tweet, visiondetection
import argparse
import logging

if __name__ == '__main__':
    #logging.basicConfig(level='INFO')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--rate',required=False,type=float,default=1,help='number of pictures per minute, default=1')
    parser.add_argument('-o','--output',required=False,type=str,default='final.mkv',help='output filename and directory, should be .mkv default=final.mkv')
    parser.add_argument('-k','--keyword',required=False,type=str,default='messi',help='search keyword default=messi')
    parser.add_argument('-c','--count',required=False, type=int,default=200,help='number of homline in each user, no larger than 20')
    parser.add_argument('-n',required=False,type=int,default=10,help='number of users to get from the same keyword, no larger than 200')
    parser.add_argument('-m',type=bool,required=False,help='grap from my homeline')
    args = parser.parse_args()
    try:rate = float(args.rate)
    except:rate=1.0
    try:output = args.output
    except:output = 'final.mkv'
    try:keyword = args.keyword
    except:keyword='messi'
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
    else:
        twitter.FromSpecificUser(keyword=keyword,count=count, numofuser=num)
    label_dict = vd.GenerateTypes()
    vd.MakeSrc(label_dict, rate=rate)
    mv.makevideo(rate=rate, output_dir=output)
