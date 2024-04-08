import os

from pymongo import MongoClient
from pymongo.database import Database
from fastapi import FastAPI
from dotenv import load_dotenv


load_dotenv()

MONGO_DB_URL = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_CLUSTER')}.mongodb.net/?retryWrites=true&w=majority&appName=LMS-Cluster"

app = FastAPI()
client = MongoClient(MONGO_DB_URL)
database = client.get_database("LMS-Cluster")


@app.on_event("startup")
async def startup_db_client():
    await database.client.start_session()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.client.close()


def get_db() -> Database:
    return database
