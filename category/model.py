from pydantic import BaseModel, Field
from typing import List, Optional
class categoryCreate(BaseModel):

    user_id:str =  Field(..., example="user id")
    store_id:Optional[str]= Field(..., example="store id")  
    category_name:str =  Field(..., example="category name")
    description:str =  Field(..., example="category description")

class categoryList(BaseModel):

    category_id:str
    
    user_id:str
    store_id:str
    category_name:str
    description:str

    status: str
    created_at:str
    last_update_at:str

class categoryUpdate(BaseModel):
    
    category_id:str
    user_id:str
    store_id:Optional[str]  
    category_name:str
    description:str

    status: str
    created_at:str
    last_update_at:str

