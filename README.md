# *FlaiReddit*
FlaiReddit is an end to end web-app deployed on Heroku that classifies the flair tags from posts in r/india. The project is strurctured in 5 steps.

## RedditCrawler - Web Scraper
The data extractor extracts posts from a wide time period to eliminate the Bias towards some hot topics.
* You can save and load your progress at checkpoints too (especially useful for online collection and storage), 
* Approximately  600 posts can be extracted per second, however as a result of the moderation of the subreddit only 20% of the data is actually available. 
* All logs are made in crawler.log, warnings are displayed.
* To optimize space removed, empty flairs are removed batch wise.

```python
from modules.crawler import *
start_time = #Enter the unix timestamp of date since when scraping should begin
end_time= #Enter the unix timestamp of date since when scraping should end
scraper = Crawler(size=1000, difference=12, sleep=0.5, start=start_time)

while(scraper.current > end time):
	red.query() #Query the database
red.dump() #Dump the stats and csv
```

A commited notebook is available at [kaggle](https://www.kaggle.com/someshsingh22/redditcrawlertest)

## Exploratory Data Analysis
Extensive analysis has been done, important words are visualized through WordClouds, in depth explanation of these and preprocessing is present in my [Notebook](https://github.com/someshsingh22/FlaiReddit-MIDAS/blob/master/Notebooks/Part-2-EDA.ipynb)

>A baseline model from BOW is also implemented at the end.
## Training the Model [BERT, TFIDF]
We set the seed for reproducibility and use BERT - *uncased, base*, freezing all layes apart from the last layer and the weights are saved for easier inference at : 

**Model Summary [Inference Time]**:
| Model | Micro-F1  |Macro-F1  | CPU Inference Time
|--|--|--|--|
| TFIDF Combined | 0.51 | 0.50  | **331 Samples/s**
| BERT | **0.60** | **0.59**  |	2.37 Samples
| TFIDF , Feats | 0.49 | 0.48  | 273 Sample/s

![Confusion Matrix](Images/CM.png)


