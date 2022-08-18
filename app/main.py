import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import models
from . database import engine
from .routers import posts,users,auth,vote
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)
origins=["https://www.google.com"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password=1234,cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("database connection was successful")
except Exception as error:
    print("connection to database failed")
    print("Error was :",error)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}



    

