import csv

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')


class Data_process:
    @staticmethod
    def txt_load(path):
        with open(path, "r",  encoding="utf-8-sig") as file:
            data = [line.strip() for line in file.readlines()]
        return data

    @staticmethod
    def csv_load_data():
        with open("../data/tweets_injected 3.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]  # list of dictionaries
        return data

    @staticmethod
    def classify_sentiment(text):
        score = SentimentIntensityAnalyzer().polarity_scores(text)
        if score['compound'] >= 0.5:
            return "Positive"
        elif score['compound'] <= -0.5:
            return "Negative"
        else:
            return "Neutral"
