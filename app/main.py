from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db  
from router import users, blogpost

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(blogpost.router)