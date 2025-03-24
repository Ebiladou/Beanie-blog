import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from app.main import app 
from beanie import init_beanie
from app.models import User, BlogPost, Comment
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient, ASGITransport
from starlette.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from fastapi import FastAPI
import asyncio

@pytest.fixture(scope="session")
async def mongo_client():
    client = AsyncMongoMockClient("mongodb://localhost:27017")
    yield client

@pytest.fixture(autouse=True)
async def test_db(mongo_client):
    db = mongo_client["blogger_test"]
    await init_beanie(database=db, document_models=[User, BlogPost, Comment])
    yield db
    collections = await db.list_collection_names()
    for collection in collections:
        await db[collection].delete_many({})

@pytest.fixture
async def client(fastapi_app: FastAPI) -> TestClient:
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as client:
        yield client


#@pytest.fixture(scope="session")
#def event_loop():
#    loop = asyncio.new_event_loop()
#    yield loop
#    loop.close()


#@pytest_asyncio.fixture
#async def test_db():
#    client = AsyncIOMotorClient("mongodb://localhost:27017")
#    db = client["blogger_test"]
#    await init_beanie(database=db, document_models=[User, BlogPost])
#    yield db 
#    await client.drop_database("blogger_test")
#    await client.close()

#@pytest_asyncio.fixture
#async def test_app():
#    async with LifespanManager(app) as manager:
#        yield manager.app

#@pytest_asyncio.fixture
#async def test_client():
#    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
#        yield client