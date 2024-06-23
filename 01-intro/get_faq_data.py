import requests 
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm

es_client = Elasticsearch("http://localhost:9200")

docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []


# Index the data in the same way as was shown in the course videos. Make the `course` field a keyword and the rest should be text. 

for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)



index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"} 
        }
    }
}

index_name = "course_faq"


es_client.indices.create(index = index_name, body = index_settings)

for doc in tqdm(documents):
    es_client.index(index = index_name, document = doc)