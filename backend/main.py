from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import MongoClient
from auth import router as auth_router
from chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        print("Starting the application")
        mongo_client = MongoClient()
        await mongo_client.connect()
        print("Application Startup completed")
        yield
        print("Shutting Application")
    except Exception as e:
        print(f"Exeption occured in Server {e}")
        raise
    finally:
        print("Closing MongoDB Connection")
        # await mongo_client.close_connection()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",  # if you're using Vite
    "http://localhost:8000",  # if using CRA or Next.js dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Server(Backend)"}


app.include_router(prefix="/chat", router=chat_router)
app.include_router(prefix="/auth", router=auth_router)
