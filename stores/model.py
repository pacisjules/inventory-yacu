from pydantic import BaseModel, Field

class storeCreate(BaseModel):

    user_id:str =  Field(..., example="user id")
    store_name:str =  Field(..., example="Store name")
    org_setting_id:str = Field(..., example="Organization id")
    address:str =  Field(..., example="address")
    description:str =  Field(..., example="description")


class storeList(BaseModel):

    store_id:str
    
    user_id:str 
    store_name:str
    address:str
    description:str
    org_setting_id:str

    status: str
    created_at:str
    last_update_at:str

class storeUpdate(BaseModel):
    
    store_id:str
    user_id:str 
    store_name:str
    address:str
    description:str
    org_setting_id:str

    status: str
    created_at:str
    last_update_at:str

