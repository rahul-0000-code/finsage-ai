from pymilvus import connections, Collection
import os

MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")

connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

def get_collection(name: str) -> Collection:
    return Collection(name)
