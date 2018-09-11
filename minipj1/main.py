import MakeVideo, tweet, visiondetection

if __name__ == '__main__':
    twitter = tweet.GetJpgFromTweet()
    vd = visiondetection.VisionDetction()
    mv = MakeVideo.MakeVideo()

    twitter.FromMyHome()
    label_dict = vd.GenerateTypes()
    vd.MakeSrc(label_dict)
    mv.makevideo()