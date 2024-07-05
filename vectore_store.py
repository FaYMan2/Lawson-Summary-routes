from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_index = os.getenv('PINECONE_INDEX_NAME')


async def get_Vectors(namespace : str) -> dict[list[list[int]], tuple]:
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(pinecone_index)
    index_stats = index.describe_index_stats()
    namespace_stats = index_stats['namespaces'].get(namespace,-1)
    if namespace_stats == -1:
        return -1
    vector_count = namespace_stats.get('vector_count',0)
    dimension = index_stats.get('dimension',-1)
    print(f'dimension : {dimension} namespace : {namespace} vector_count : {vector_count}')
    query_res = index.query(
        top_k=vector_count,
        namespace=namespace,
        vector=[0 for _ in range(dimension)],
        include_values=True
    )
    print(f'length of result : {len(query_res['matches'])} dimension : {len(query_res['matches'][0].get('values',[]))}')
    
    vectors = [vec['values'] for vec in query_res['matches']]
    print(f'vector array length : {len(vectors)} shape = {len(vectors) , len(vectors[0])}')
    shape = (len(vectors), len(vectors[0]))
    return {
        "vectors" : vectors,
        "shape" : shape
    }