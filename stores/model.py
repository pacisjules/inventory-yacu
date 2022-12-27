from pydantic import BaseModel, Field

class storeCreate(BaseModel):

    user_id:str =  Field(..., example="user id")
    store_name:str =  Field(..., example="user id")
    address:str =  Field(..., example="user id")
    description:str =  Field(..., example="user id")


class storeList(BaseModel):

    store_id:str
    
    user_id:str 
    store_name:str
    address:str
    description:str

    status: str
    created_at:str
    last_update_at:str

class storeUpdate(BaseModel):
    
    store_id:str
    user_id:str 
    store_name:str
    address:str
    description:str

    status: str
    created_at:str
    last_update_at:str

