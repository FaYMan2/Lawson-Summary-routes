from fastapi import FastAPI
import json
from vectore_store import get_Vectors
from embedder import Embedder
from dotenv import load_dotenv
import os
load_dotenv()
process_key = os.getenv('API_KEY')
app = FastAPI()
@app.get("/")
async def ping():
    return{
        "message" : "server active"
    }

@app.get("/vectors/{docId}")
async def root(docId : str,api_key : str):
    if process_key == api_key:
        vectors = await get_Vectors(namespace=docId)
        print(vectors)
        return {"message": json.dumps(vectors)}
    else:
        return {
            "message" : "Unortharized access - invalid api key"
        }


@app.post("/emmbed")
async def embedd(url : str,docId : str,api_key : str):
    print('ROUTE CALLED')
    if process_key == api_key:
        res = await Embedder(URL=url,
                             chunkSize=10000,
                             overlap=500,
                             namespace=docId)
        if res:
            return {
                "vector_count" : res['vector_count'],
                "time" : res['time'],
                "namespace" : res['namespace']
             }
        return {
            "message" : "failed"
        }
    else :
        return {
            "message" : "Unortharized access - invalid api key"
        }
