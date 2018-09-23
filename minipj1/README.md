Project 1  API Mini-Project
====

# Changelog

## version 0.1
1. Get pictures from my homeline
2. put them into a video
3. Add subtitle on each picture

## version 0.1.1
1. Get pictures from other users
2. Specify user numbers and homeline counts e.g. you enter a search keyword "messi", script will return n top queries and search their recent k homelines 

## version 0.1.2
1. Specify rate of video

## update 0921
1. remove my key for twitter developer. So user should add your own in tweep.py line13-16. -m parameter will return pictures from your own homeline
2. When having no pictures, raise error and raise warning when having more than 100 pictures.

# Usage

This library currently only works under Windows. First put your Google Vision key file under project folder (`licenseofvision.json`).

```shell
python main.py -r 1.0 -o final.mkv -k ronaldo -c 100 -n 10 (-m 1)
```

* `-r` number of pictures per minute, default=1
* `-o` output filename and directory, should be ended with `.mkv`, default=final.mkv
* `-k` search keyword, default=messi
* `-c` number of homline in each user, no larger than 20
* `-n` number of users to get from the same keyword, no larger than 200
* `-m` grap from my homeline (`-c`, `-k` will not function if you use `-m`)