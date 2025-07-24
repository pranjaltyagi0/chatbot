from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils import MongoClient
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


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Server(GenAI)"}


app.include_router(prefix="/chat", router=chat_router)
