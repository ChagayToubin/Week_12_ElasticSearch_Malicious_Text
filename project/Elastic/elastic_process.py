from elasticsearch import Elasticsearch
from project.data.data_processor import Data_process
from elasticsearch.helpers import scan, bulk
from elasticsearch import helpers
import re


class Es:
    def __init__(self, uri):
        self.uri = uri
        self.index = "tweets"
        self.es = self.connection()
        self.data=Data_process()

    def get_URI(self):
        return self.uri

    def connection(self):
        return Elasticsearch(self.get_URI())

    def load_data(self):
        response = self.es.search(
            index=self.index,
            body={"query": {"match_all": {}}},
            size=10000
        )
        return response["hits"]["hits"]

    def delete_antisemitic(self):
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

    def add_weapons_to_docs(self, weapons_list):
        query = {
            "query": {
                "bool": {
                    "should": [
                        {"match_phrase": {"text": f" {weapon.lower().strip()}"}} for weapon in
                        weapons_list
                    ]
                }
            },
            "size": 10000,
            "highlight": {
                "fields": {
                    "text": {}
                }
            }
        }

        scroll = self.es.search(index="tweets", body=query, scroll="2m")
        scroll_id = scroll["_scroll_id"]
        hits = scroll["hits"]["hits"]
        print(f"Found {len(hits)} weapons")

        while hits:
            actions = []
            for hit in hits:
                doc_id = hit["_id"]
                highlight = hit["highlight"]["text"]
                found_weapons = []
                for high in highlight:
                    found_weapons += re.findall(r'<em>(.*?)</em>', high)
                if found_weapons:
                    actions.append({
                        "_op_type": "update",
                        "_index": "tweets",
                        "_id": doc_id,
                        "doc": {"weapons": found_weapons}
                    })

            if actions:
                success, failed = bulk(self.es, actions)
                print(f"Updated weapons field in {success} docs, failed to index {len(failed)} documents.")


            scroll = self.es.scroll(scroll_id=scroll_id, scroll="2m")
            scroll_id = scroll["_scroll_id"]
            hits = scroll["hits"]["hits"]

    def update_all_documents_sentiment(self):

        scroll = self.es.search(
            index="tweets",
            scroll="2m",
            body={
                "_source": ["text"],
                "query": {"match_all": {}},
                "size": 1000,
            }
        )

        scroll_id = scroll["_scroll_id"]
        hits = scroll["hits"]["hits"]

        while hits:
            actions = []
            for hit in hits:
                doc_id = hit["_id"]
                tweet_text = hit["_source"].get("text", "")
                sentiment = self.data.classify_sentiment(tweet_text)

                actions.append({
                    "_op_type": "update",
                    "_index": "tweets",
                    "_id": doc_id,
                    "doc": {"sentiment": sentiment}
                })

            if actions:
                success = bulk(self.es, actions)
                print(f"Updated {success} docs")

            scroll = self.es.scroll(scroll_id=scroll_id, scroll="2m")
            scroll_id = scroll["_scroll_id"]
            hits = scroll["hits"]["hits"]

    def send_data(self, data, index_name):
        mapping = self.init_mapping(index_name)

        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index, body=mapping)

        actions = []
        for i, doc in enumerate(data):
            document = {
                "text": doc["text"],
                "TweetID": str(doc["TweetID"]),
                "CreateDate": str(doc["CreateDate"]),
                "Antisemitic": doc["Antisemitic"]

            }

            actions.append({
                "_index": self.index,
                "_id": i,
                "_source": document
            })

        helpers.bulk(self.es, actions)
        print(f"Indexed {len(actions)} documents.")

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

    def search_antisemtic_with_weapons(self):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"Antisemitic": "1"}},
                        {"script": {"script": "doc['weapons'].size() >= 2"}}
                    ]
                }
            }
        }
        response = self.es.search(index=self.index, body=query)
        hits = response["hits"]["hits"]
        if not hits:
            return {"message": "לא נמצאו מסמכים מתאימים"}
        return hits

    def search_docs_with_two_or_more_weapons(self):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "script": {
                                "script": {
                                    "source": "doc['weapons'].size() >= 2"
                                }
                            }
                        }
                    ]
                }
            }
        }

        response = self.es.search(index=self.index, body=query)

        hits = response["hits"]["hits"]
        if not hits:
            return {"message": "לא נמצאו מסמכים עם 2 כלי נשק או יותר"}
        return hits

    def fount_weapons(self,text,weapons_list):
        e = [w for w in weapons_list if w.lower() in text.lower()]
        print(e)

        return e
