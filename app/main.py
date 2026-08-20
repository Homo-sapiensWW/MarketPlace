from fastapi import FastAPI
from app.database import engine, Base
from app.routers.auth_router import router as auth_router
from app.routers.admin_router import router as admin_router
from app.routers.items_router import router as items_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title='MarketPlace API', version="1.0.0")

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(items_router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Marketplace API is running!"}
