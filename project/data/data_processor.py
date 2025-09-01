import csv

class Data_process:

    @staticmethod
    def load_data():

        with open("../data/tweets_injected 3.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]  # list of dictionaries
        return data








# print(Data_process.load_data())