from project.data.data_processor import Data_process as D
from project.Elastic.core.elastic_process import Es

class Manager:
    def __init__(self,uri,data):
        self.data=D()
        self.es=Es(uri)
        # self.es=self.es.connect()

    def manager_start(self):
        # level 1
        self.level1()


    def level1(self):
        data_to_send = self.data.load_data()
        self.es.send_data(data_to_send)








