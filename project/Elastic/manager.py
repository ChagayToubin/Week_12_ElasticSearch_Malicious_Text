from project.data.data_processor import Data_process
from project.elastic.core.elastic_process import Es


class Manager:
    def __init__(self, uri, data):
        self.data = Data_process()
        self.es = Es(uri)
        # self.es=self.es.connect()

    def manager_start(self):
        # self.level1()
        #
        # self.level2()
        #
        self.level3()
        #
        # self.level4()
        print(4)
    def level1(self):
        data_to_send = self.data.csv_load_data()
        self.es.send_data(data_to_send, "tweets")

    def level2(self):
        data = self.es.load_data()
        self.es.update_all_documents_sentiment(data)

    def level3(self):
        path = "../data/weapon_list.txt"
        weapons_list = Data_process.txt_load(path)
        data = self.es.load_data()
        self.es.add_weapons_to_docs(weapons_list, data)

    def level4(self):
        self.es.delet_Antisemitic()

