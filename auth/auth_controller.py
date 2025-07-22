import os

from .auth_model import SignUp, Login
from utils import MongoDB


class AuthController:

    def __init__(self):
        self.database = os.getenv("DATABASE")
        self.collection_name = os.getenv("COLLECTION_NAME")

    async def login(self, request: Login):
        client = MongoDB().connect()
        db = client[self.database]
        collection = db[self.collection_name]
        result = await collection.find(
            {"useremail": request.useremail, "password": request.password}
        ).to_list()
        if not result:
            return "Wrong username or password"
        return "Login Approved"

    async def signup(self, request: SignUp):
        client = MongoDB().connect()
        db = client[self.database]
        collection = db[self.collection_name]
        print(request.useremail)
        res = await collection.find({"useremail": request.useremail}).to_list()
        print(res)
        if not res:
            print("in here")
            result = await collection.insert_one(request.model_dump())
            print(result.inserted_id)
            return str(result.inserted_id)
        else:
            return {"User already exists"}
