from imaplib import IMAP4

from project.data.data_processor import Data_process
from project.elastic.elastic_process import Es
import uvicorn


class Manager:
    def __init__(self, uri, data):
        self.data = Data_process()
        self.es = Es(uri)
        # self.es=self.es.connect()

    def manager_start(self):
        self.level1()
        # #
        self.level2()
        #
        self.level3()
        #
        self.level4()

        self.server_start()

    def level1(self):
        data_to_send = self.data.csv_load_data()
        self.es.send_data(data_to_send, "tweets")

    def level2(self):
        self.es.update_all_documents_sentiment()

    def level3(self):
        weapons_list = Data_process.txt_load()
        self.es.add_weapons_to_docs(weapons_list)

    def level4(self):
        self.es.delete_antisemitic()

    def server_start(self):
        uvicorn.run(
            app="project.server.app:app",
            host="0.0.0.0",
            port=8000
        )
