import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DATABASE_URL')
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
engine = create_async_engine(DB_URL)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session