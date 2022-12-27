from pydantic import BaseModel, Field

class CustomerCreate(BaseModel):

    user_id:str =  Field(..., example="user id")
    names:str =  Field(..., example="Names")
    tin:str =  Field(..., example="tin number")
    bio: str = Field(..., example="bio")
    email: str = Field(..., example="email")
    phone: str = Field(..., example="phone")

    province: str = Field(..., example="province")
    district: str = Field(..., example="district")
    address: str = Field(..., example="address")


class CustomerList(BaseModel):

    id: str

    user_id:str
    names:str 
    tin:str
    bio: str
    email: str
    phone: str
    identity_number:str 

    province: str
    district: str
    address: str
    qr_name:str
    


    status: str
    created_at:str
    last_update_at:str

class CustomerUpdate(BaseModel):
    
    id: str
    
    user_id:str
    names:str 
    tin:str
    bio: str
    email: str
    phone: str 
    
    province: str
    district: str
    address: str

