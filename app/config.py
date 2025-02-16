from elasticsearch import Elasticsearch

ES_HOST = "http://elasticsearch:9200"  # Change based on docker-compose setup

def get_es_client():
    return Elasticsearch([ES_HOST])
