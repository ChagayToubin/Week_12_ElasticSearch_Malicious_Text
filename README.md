# Week_12_ElasticSearch_Malicious_Text

This project loads malicious text data into Elasticsearch, processes it, and exposes a simple API.

## Features
- Load dataset into Elasticsearch with field mapping
- Detect sentiment and add it as a new field
- Detect weapon keywords and add them to each document
- Remove irrelevant documents (not antisemitic + no weapons + neutral/positive sentiment)
- Provide 2 API endpoints:
  1. All antisemitic texts with at least one weapon
  2. All texts with two or more weapons

