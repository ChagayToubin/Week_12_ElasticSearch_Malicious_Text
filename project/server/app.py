from fastapi import FastAPI
from project.elastic.elastic_process import Es
import os
app = FastAPI()
uri_es=os.getenv("URI","http://localhost:9200")


es=Es(uri_es)
@app.get("/check_one_weapon")
def check_one_weapon_antisemtic():
    return es.search_antisemtic_with_weapons()

@app.get("/check_multiple_weapons")
def check_multiple_weapons():
    return es.search_docs_with_two_or_more_weapons()
