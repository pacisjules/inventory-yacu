from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., example="gaga")


    first_name: str = Field(..., example="Ganza")
    last_name: str = Field(..., example="Babu")
    password: str = Field(..., example="***")


    email: str    = Field(..., example="manzii5@gmail.com")
    type: str    = Field(..., example="Normal")
    role:str = Field(..., example="Manager")



    company: str    = Field(..., example="Company")
    phone: str    = Field(..., example="phone")
    living: str    = Field(..., example="Kigali")

class UserList(BaseModel):
    user_id: str
    username: str
    first_name: str 
    last_name: str 
    email: str
    type: str 
    role:str
    company: str    
    phone: str    
    living: str 
    status: str
    created_at: str
    last_update_at: str


class UserListforUpdate(BaseModel):
    user_id: str
    username: str
    password: str
    first_name: str 
    last_name: str 
    email: str
    type: str 
    role:str
    company: str    
    phone: str    
    living: str 
    status: str

class UserUpdate(BaseModel):
    id: str
    username: str
    password: str
    first_name: str 
    last_name: str 
    email: str
    type: str 
    role:str
    company: str    
    phone: str    
    living: str 



class UserPWD(UserList):
    password: str

class Token(BaseModel):
    access_token: str
    token_type  : str
    expired_in  : str
    user_info   : UserList

class TokenData(BaseModel):
    username: str = None


class UserPasswordUpdate(BaseModel):
    password: str

class KeyChange(BaseModel):
    id: str
    user_id:str
    key:str
    status:str
    created_at:str


