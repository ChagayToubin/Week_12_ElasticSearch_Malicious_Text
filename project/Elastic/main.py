from project.elastic.manager import Manager
from project.data.data_processor import Data_process
import os

uri_es=os.getenv("URI","http://localhost:9200")

data_to_send=Data_process.csv_load_data()



m=Manager(uri_es,data_to_send)
m.manager_start()

