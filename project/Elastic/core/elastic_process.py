from elasticsearch import Elasticsearch
from project.data.data_processor import Data_process


class Es:
    def __init__(self, uri):
        self.uri = self.get_URI(uri)
        self.index = "tweets"
        self.es = self.connection()

    def get_URI(self, uri):
        return "http://localhost:9200"

    def connection(self):
        return Elasticsearch(self.uri)

    def load_data(self):
        response = self.es.search(
            index=self.index,
            body={"query": {"match_all": {}}},
            size=10000
        )
        return response["hits"]["hits"]

    def delet_Antisemitic(self):
        # docs = es.search(
        #     index=index_name,
        #     body={
        #         "query": {
        #             "bool": {
        #                 "must": [
        #                     {"term": {"Antisemitic": 0}},
        #                     {"term": {"weapons": "not found"}},
        #                     {"terms": {"sentiment": ["neutral", "positive"]}}
        #                 ]
        #             }
        #         }
        #     },
        self.es.delete_by_query(
            index="tweets",
            body={
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"Antisemitic": 0}},
                            {"term": {"weapons": "not found"}},
                            {"terms": {"sentiment": ["Neutral", "Positive"]}}
                        ],

                    }
                }
            }
        )

    def add_weapons_to_docs(self, weapons_list, data):
        for hit in data:
            doc_id = hit["_id"]
            text = hit["_source"].get("text", "")

            found = [w for w in weapons_list if w in text]
            if found:
                weapons_value = found
            else:
                weapons_value = "dount found"

            if found:
                self.es.update(
                    index=self.index,
                    id=doc_id,
                    body={
                        "doc": {
                            "weapons": weapons_value
                        }
                    }
                )
                print(f"Updated {doc_id} with weapons={found}")

    def update_all_documents_sentiment(self, data):
        docs = data
        for hit in docs:
            doc_id = hit["_id"]
            source = hit["_source"]
            text = source.get("text", "")
            sentiment = Data_process.classify_sentiment(text)
            self.es.update(
                index=self.index,
                id=doc_id,
                body={"doc": {"sentiment": sentiment}}
            )
            print(f"Updated doc {doc_id} with sentiment={sentiment}")

    def send_data(self, data, index_name):
        mapping = self.init_mapping(index_name)

        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index, body=mapping)

        for i, doc in enumerate(data):
            document = {
                "text": data[i]["text"],
                "TweetID": str(data[i]["TweetID"]),
                "CreateDate": str(data[i]["CreateDate"]),
                "Antisemitic": data[i]["Antisemitic"],
                "sentiment": "empty",
                "weapons": "empty"

            }
            self.es.index(index=self.index, id=i, body=document)
            if i % 100 == 0:
                print(f"Indexed {i} documents.")

    def init_mapping(self, index_name):
        self.index = index_name
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
        return mapping
