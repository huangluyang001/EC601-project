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

python main.py -r 1.0 -o final.mkv -k ronaldo -c 100 -n 10 (-m 1)

-r number of pictures per minute, default=1

-o output filename and directory, should be .mkv default=final.mkv

-k search keyword default=messi

-c number of homline in each user, no larger than 20

-n number of users to get from the same keyword, no larger than 200

-m grap from my homeline(-c,-k will have no function if you use -m)

# update 0921
1. remove my key for twitter developer. So user should add your own in tweep.py line13-16. -m parameter will return pictures from your own homeline
2. When having no pictures, raise error and raise warning when having more than 100 pictures.

# update pj3
1. mongodb.py store information in mongodb.  
# Usage  
Put your google vision key file under project folder

python mongodb.py -r 1.0 -o final.mkv -k ronaldo -c 100 -n 10 (-m 1)

-r number of pictures per minute, default=1

-o output filename and directory, should be .mkv default=final.mkv

-k search keyword default=messi

-c number of homline in each user, no larger than 20

-n number of users to get from the same keyword, no larger than 200

-m grap from my homeline(-c,-k will have no function if you use -m)

# Format of data  
'user_name': user's name,  
'use_time': time using(local time),  
'keyword': search keyword,  
'picture_counts': picture counts,  
'search results': users' name a string with at most 10 users' name,  
'rate': rate of video,  
'output name': output filename,  
'from_my_home': if using from my home setting  

# Mongodb_search.py  
## Usage  
-k search for a certain key, choosing from user_name, use_time, keyword, search results, rate, output name, from_my_home  
-w search for certain keyword  
The code will also generate some useful statistic info:  
sample output:  
# of information:  1
most common user and count:  luyang 1  
most common keyword and count:  jerry 1  
Search results:   
{'_id': ObjectId('5c01e6ce89c68c651018adce'), 'user_name': 'luyang', 'use_time': '2018.11.30 20:40', 'keyword': 'jerry', 'picture_counts': 45, 'search results': 'JerrySeinfeld\nJerryLawler\nJerryBrownGov\nRepJerryNadler\nbenandjerrys\nJerryRice\nJerryMoran\nBRUCKHEIMERJB\njerrytrainor\nJerryDouglas\n', 'rate': 1.0, 'output name': 'final.mkv', 'from_my_home': 'False'}  

# sql.py  
To use sql.py, you need to create a database in your own localhost first.  
username: root  
password: luyanghuang (you can change in line 18 to change your password)  
dbname: mp3  
table name: userinfo  
you can use following command to generate table of my format  
CREATE TABLE IF NOT EXISTS userinfo(user_name VARCHAR(40) NOT NULL,user_time VARCHAR(40) NOT NULL,keyword VARCHAR(40) NOT NULL,picture_counts VARCHAR(40) NOT NULL,search_results VARCHAR(40) NOT NULL,rate VARCHAR(40) NOT NULL,output_name VARCHAR(40) NOT NULL,from_my_home VARCHAR(40) NOT NULL);  
data format  
'user_name': user's name,  
'user_time': time using(local time),  
'keyword': search keyword,  
'picture_counts': picture counts,  
'search results': users' name a string with at most 10 users' name,  
'rate': rate of video,  
'output name': output filename,  
'from_my_home': if using from my home setting  
## Usage  
sql.py will make video and save data in database.  
The usage is similar to mongodb.py  

# sql_query.py  
## Usage  
-w search for certain keyword  
sample output:  
# of information:  4  
most common user and count:  luyang 3  
most common keyword and count:  jerry 3  
number of information under your keyword:  4  
most common user and count under your keyword:  luyang 3  
most common keyword and count under your keyword:  jerry 3  
