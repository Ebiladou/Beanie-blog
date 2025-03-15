from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import User, BlogPost  

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")  
    db = client["blogger"] 
    await init_beanie(database=db, document_models=[User, BlogPost])