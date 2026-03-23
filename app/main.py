from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from app.routers import goods, users, tasks, posts, orders, details

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://195.226.92.61"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(goods.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(details.router, prefix="/api")