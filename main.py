import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from src.conf.config import settings
from src.routes import contacts, auth, users
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# @app.on_event('startup')
# async def startup():
#     r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding='utf-8',
#                           decode_responses=True)
#     await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Welcome to Contacts APP"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)