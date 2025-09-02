import csv

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pathlib import Path
nltk.download('vader_lexicon')
base_dir = Path(__file__).resolve().parent

class Data_process:
    @staticmethod
    def txt_load():
        txt_path=base_dir / "weapon_list.txt"
        with open(txt_path, "r",  encoding="utf-8-sig") as file:
            data = [line.strip() for line in file.readlines()]
        return data

    @staticmethod
    def csv_load_data():
        csv_path = base_dir / "tweets_injected 3.csv"
        with open(csv_path, "r", encoding="utf-8") as file:
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
