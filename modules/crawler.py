import requests  # For querying pushlift to extract json files from reddit
import time  # For generating timestamps
import json  # To handle json files from pushlift
import logging  # Logging files for error handling
import datetime  # To convert unix timestamps to dates
import pickle  # to load and save from checkpoints
from tqdm import tqdm_notebook  # tqdm range to gauge progress
import matplotlib.pyplot as plt  # for analytics
import seaborn as sns
import pandas as pd  # convert extracted data to csv

# Create and configure logger


class Crawler:
    def __init__(self, size=250, start=time.time(), difference=7, sleep=1):

        # Data Collected by the crawler
        self.data = {
            "Title": [],
            "Flair": [],
            "Text": [],
        }

        self.stats = []  # Number of posts collected on every leap of time
        self.sleep, self.size, self.start, self.difference = (
            sleep,
            size,
            start,
            difference,
        )  # Init the parameters
        self.__validate__()  # Validate Parmaeters and log warnings
        self.difference = self.difference * 3600  # set difference to day format
        self.current = self.start  # set timer for query to time of init
        self.url_generator = self._url_generator()  # create a url generator
        self.url = "https://api.pushshift.io/reddit/search/submission/?subreddit=india&size={}&{}&fields=title,selftext,link_flair_text"  # url format for pushlift

    # Validator for Web Crawler
    def __validate__(self):
        # validate sleep value to be a number >= 1
        try:
            assert self.sleep >= 1 and (
                isinstance(self.sleep, int) or isinstance(self.sleep, float)
            )
        except:
            logging.warning(
                "Invalid sleep value, may cause DNS server blocking, set to 1"
            )
            self.sleep = 1

        # validate query size to be a number <= 500
        try:
            assert self.size <= 500 and self.size >= 100 and isinstance(self.size, int)
        except:
            logging.warning(
                "Invalid query size, may cause DNS server blocking, set to 500"
            )
            self.size = 500

        # Validate start to be valid a present\past timestamp
        try:
            self.start = int(self.start)
            assert self.start <= time.time() and isinstance(self.start, int)
        except:
            logging.warning("Invalid start time, being set to current")
            self.start = int(time.time())

        # Validate the difference to be a valid positive number
        try:
            assert isinstance(self.difference, int) and self.difference > 0
        except:
            logging.warning("Invalid difference, setting to a week")
            self.difference = 7

    # URL Generator for pushlift
    def _url_generator(self):
        while True:
            timestamp = "before={}&after={}".format(
                self.current, self.current - self.difference
            )  # Get timestamp
            yield self.url.format(self.size, timestamp)  # get URL
            self.current -= self.difference  # Update Current time

    # Process json output from pushlift to data
    def process_json(self, jsons):
        for json in jsons:
            self.data["Title"].append(json["title"] if "title" in json else None)
            self.data["Text"].append(json["selftext"] if "selftext" in json else None)
            self.data["Flair"].append(
                json["link_flair_text"] if "link_flair_text" in json else None
            )

    # Query and update the data from Web Crawler
    def query(self):
        loc_url = next(self.url_generator)  # generate URL
        try:
            r = requests.get(loc_url)  # get JSON
            data = json.loads(r.text)  # load JSON to dict format

            # filter deleted/removed and posts without text
            jsons = [
                post
                for post in data["data"]
                if "selftext" in post
                and not (
                    post["selftext"] == "[removed]"
                    or post["selftext"] == "[deleted]"
                    or post["selftext"] == ""
                )
            ]

            # process jsons to dict
            self.process_json(jsons=jsons)

            # append the datestamp and number of valid posts fetched in this leap
            self.stats.append(
                (
                    datetime.datetime.fromtimestamp(self.current).strftime("%Y-%m-%d"),
                    len(jsons),
                )
            )

            # delay interval to prevent DNS blocking
            time.sleep(self.sleep)
            logging.info("Query Successfull at {}".format(loc_url))
        except:
            logging.error("Query Failed at {}".format(loc_url))

    # to save progress for multi stop database generation and save the checkpoint to a JSON
    def save(self, pre=""):
        logging.info("Pickle dumped to {}.pkl".format(self.current))
        with open(pre + ("{}.pkl".format(self.current)), "wb+") as f:
            pickle.dump([self.data, self.stats], f)

    # to load from a previous checkpoint
    def load(self, js):
        with open(js, "rb") as f:
            self.data, self.stats = pickle.load(f)
        self.current = int(js.split("/")[-1][:-4])  # init current stamp to saved stamp
        self.timer = self._url_generator()  # init generator from loaded stamp

    # dump data to csv and stats to pkl
    def dump(self, pre=""):
        self.csv = pd.DataFrame()  # csv init
        for key, values in self.data.items():  # create csv
            self.csv[key] = values
        self.csv.to_csv(pre + "raw_data.csv", index=False)  # dump .csv
        with open(pre + "stats.pkl", "wb") as f:
            pickle.dump(self.stats, f)
