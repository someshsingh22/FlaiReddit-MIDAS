# *FlaiReddit*
FlaiReddit is a web-app deployed on Heroku that classifies the flair tags from posts in r/india. The repository can be defined in 5 stages

## RedditCrawler
The data extractor extracts posts from a wide time period to eliminate the Bias towards some hot topics, you can save and load your progress as checkpoints, Approximately  600 posts can be extracted per second, however as a result of the moderation of the subreddit only 20% of the data is actually available. All logs are made in crawler.log . 
