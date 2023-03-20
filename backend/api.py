from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId
import os


class TranscriptItem(BaseModel):
    _id: ObjectId | None = None
    client: str
    meeting_id: str
    timestamp: datetime | None = None
    time_delta: str
    participant: str
    message: str



app = FastAPI()

#MONGO
load_dotenv()
MONGO_USER=os.getenv('MONGO_USER')
MONGO_PWD=os.getenv('MONGO_PWD')
MONGO_URL=os.getenv('MONGO_URL')
MONGO_PORT=os.getenv('MONGO_PORT')
DB_NAME=os.getenv('DB_NAME')
mongo_connection_string = f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_URL}:{MONGO_PORT}/"
client = MongoClient(mongo_connection_string, ssl=True)
db = client[DB_NAME]

# CORS
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def str_id(object):
    object["_id"]=str(object["_id"])
    return object

@app.get("/transcript_item/{meeting_id}")
async def get_documents(meeting_id: str, offset: int = 0, page_size: int = 10):
    _collection = db["transcript_item"]
    return [ str_id(x) for x in _collection.find({"meeting_id":meeting_id})[offset:offset+page_size]]
    
    

@app.post("/transcript_item/")
async def create_item(item: TranscriptItem):
    print(item)
    item.timestamp = datetime.now()
    _collection = db['transcript_item']
    inserted = _collection.insert_one(dict(item))
    print(inserted)
    return item
