# Basic
import time
import pandas as pd
from collections import Counter
from tfidf_model import clean


def merge_label_pairs(data, pairs):
    """
    Merge labels with slightly different names, for e.g AskIndia and Askindia for all given pairs
    """
    for pair in pairs:
        data["Flair"].replace(pair[0], pair[1], inplace=True)


def drop_removed(data):
    """
    Removes posts that were deleted
    """
    return data[data["Text"].apply(lambda x: x.count("[removed]")) == 0]


def drop_rare_labels(data, thresh=1000):
    """
    Drops labels with less than threshold samples
    """
    counter = Counter(data["Flair"])
    return data[data["Flair"].apply(lambda x: counter[x]) > thresh]


if __name__ == "__main__":
    # Load Data
    DATA_PATH = "raw_data.csv"
    raw_df = pd.read_csv(open(DATA_PATH), encoding="utf-8").dropna()
    mergers = [
        ("Science &amp; Technology", "Science/Technology"),
        ("Policy &amp; Economy", "Policy/Econonmy"),
        ("Non-Political ", "Non-Political"),
        ("Askindia", "AskIndia"),
    ]
    merge_label_pairs(raw_df, mergers)
    raw_df = drop_removed(raw_df)
    raw_df = drop_rare_labels(raw_df)
    raw_df.to_csv("data.csv")
