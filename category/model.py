from pydantic import BaseModel, Field

class categoryCreate(BaseModel):

    user_id:str =  Field(..., example="user id")
    category_name:str =  Field(..., example="user id")
    address:str =  Field(..., example="user id")
    description:str =  Field(..., example="user id")


class categoryList(BaseModel):

    category_id:str
    
    user_id:str 
    category_name:str
    address:str
    description:str

    status: str
    created_at:str
    last_update_at:str

class categoryUpdate(BaseModel):
    
    category_id:str
    user_id:str 
    category_name:str
    address:str
    description:str

    status: str
    created_at:str
    last_update_at:str

