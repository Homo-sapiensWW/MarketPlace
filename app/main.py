from fastapi import FastAPI
from app.database import engine, Base
from app.routers.auth_router import router as auth_router
from app.routers.admin_router import router as admin_router
from app.routers.items_router import router as items_router
from app.routers.category_router import router as category_router
import asyncio
from fastapi.staticfiles import StaticFiles
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(title='MarketPlace API', version="1.0.0")

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(items_router)
app.include_router(category_router)
app.mount("/web", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/", tags=["Root"])
def root():
    return {"message": "Marketplace API is running!"}

if __name__ == "__main__":
    asyncio.run(init_db())