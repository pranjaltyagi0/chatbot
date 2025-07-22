from pydantic import BaseModel

class SignUp(BaseModel):
    first_name:str
    last_name:str | None = None
    useremail:str
    password:str
    
class Login(BaseModel):
    useremail:str
    password:str