from pydantic import BaseModel, Field


class distributorCreate(BaseModel):

    user_id:str =  Field(..., example="user id")
    names:str =  Field(..., example="names")
    email:str =  Field(..., example="email")
    phone:str =  Field(..., example="phone")
    address:str =  Field(..., example="address")

class distributorList(BaseModel):

    distributor_id:str
    user_id:str
    
    names:str 
    email:str
    phone:str
    address:str

    status: str
    created_at:str
    last_update_at:str


class distributorUpdate(BaseModel):
    
    distributor_id:str
    user_id:str
    
    names:str 
    email:str
    phone:str
    address:str

    status: str
    created_at:str
    last_update_at:str

