from fastapi import FastAPI,HTTPException
import json
from vectore_store import get_Vectors
from embedder import Embedder
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

load_dotenv()
process_key = os.getenv('API_KEY')
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

def auth(api_key: str) -> bool:
    try:
        pk = str(os.getenv('PRIVATE_KEY'))
        if pk is None:
            raise ValueError("Private key not found in environment variables")
        env_key = pk.replace('\n'," ")
        private_key = RSA.import_key(env_key)
        bytes_key = bytes.fromhex(api_key)
        cipher_rsa_d = PKCS1_OAEP.new(private_key)
        d_data = cipher_rsa_d.decrypt(bytes_key)
        input_key = d_data.decode('utf-8')
        return process_key == input_key
    except ValueError as ve:
        print("Value error occurred:", ve)
    except Exception as e:
        print("An error occurred during decryption:", e)
    return False


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
        raise HTTPException(status_code=401,detail="Unortharized access - invalid api key")


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
        
        raise HTTPException(status_code=500,detail="OOPS : SOMETHING WENT WRONG")
        
    else :
        raise HTTPException(status_code=401,detail="Unortharized access - invalid api key")
        
