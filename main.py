from fastapi import FastAPI
import json
from vectore_store import get_Vectors
from embedder import Embedder
app = FastAPI()


@app.get("/")
async def ping():
    return{
        "message" : "server active"
    }

@app.get("/vectors")
async def root():
    vectors = await get_Vectors(namespace='clxd6ui070004acwb4gvwd92c')
    print(vectors)
    return {"message": json.dumps(vectors)}


@app.get("/emmbed")
async def embedd():
    print('ROUTE CALLED')
    res = await Embedder(URL='https://utfs.io/f/4741fdfc-abf3-468b-88bc-310ff8d32ba2-vykhb1.PDF',
                         chunkSize=10000,
                         overlap=500)
    if res == 1:
        return {
            "message" : "done"
        }
    return {
        "message" : "not done"
    }
