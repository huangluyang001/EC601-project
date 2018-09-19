Project 1  API Mini-Project
====  
# version 0.1
1. Get pictures from my homeline</br>
2. put them into a video</br>
3. Add subtitle on each picture
# version 0.1.1
1. Get pictures from other users
2. Specify user numbers and homeline counts e.g. you enter a search keyword "messi", script will return n top queries and search their recent k homelines 
# version 0.1.2
1. Specify rate of video
# Final version
1.Add arguments.
# Usage
Put your google vision key file under project folder
python main.py -r 1.0 -o final.mkv -k ronaldo -c 100 -n 10 (-m)
-r number of pictures per minute, default=1
-o output filename and directory, should be .mkv default=final.mkv
-k search keyword default=messi
-c number of homline in each user, no larger than 20
-n number of users to get from the same keyword, no larger than 200
-m grap from my homeline(-c,-k will have no function if you use -m)
