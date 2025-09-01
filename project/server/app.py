from fastapi import FastAPI
from project.elastic.core.elastic_process import Es

app = FastAPI()



@app.post("/check_one_weapon")
def check_one_weapon_antisemtic():
    return {"results": "as"}

@app.post("/check_multiple_weapons")
def check_multiple_weapons():

    return {"results": "result"}
