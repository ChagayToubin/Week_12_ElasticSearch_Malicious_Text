from elasticsearch import Elasticsearch

class Es:
    def __init__(self,uri):
        self.uri=uri

    def get_URI(self):
        return "http://localhost:9200"

    def connection(self):
        return Elasticsearch(self.uri)

    def send_data(self,data):

        es=self.connection()


        index_name="tweets"
        mapping = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "TweetID": {"type": "keyword"},
                    "CreateDate": {"type": "text"},
                    "Antisemitic": {"type": "integer"},
                    "sentiment": {"type": "keyword"},
                    "weapons": {"type": "keyword"}
                }
            }
        }

        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name, body=mapping)

        for i, doc in enumerate(data):
            document = {
                "text": data[i]["text"],
                "TweetID":str(data[i]["TweetID"]),
                "CreateDate":str(data[i]["CreateDate"]),
                "Antisemitic":data[i]["Antisemitic"],
                "sentiment":"empty",
                "weapons":"empty"

            }

            es.index(index=index_name, id=i, body=document)
            if i % 100 == 0:
                print(f"Indexed {i} documents.")



    # es = Elasticsearch('http://localhost:9200')
