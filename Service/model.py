from pydantic import BaseModel, Field

class Vehicle_Service_Create(BaseModel):
    
    user_id:str =  Field(..., example="user id")
    customer_id:str =  Field(..., example="customer id")
    vehicle_id: str = Field(..., example="vehicle id")
    wash_type_id: str = Field(..., example="wash type id")

    comment:str =  Field(..., example="comment")
    price:float=  Field(..., example="price")



class Vehicle_Service_List(BaseModel):

    id: str

    user_id:str
    customer_id:str
    vehicle_id: str
    wash_type_id: str

    comment:str
    price:float

    service_identity:str
    qr_name:str
    process_level:str

    status: str
    created_at:str
    last_update_at:str

    month:int
    year:int
    
class Vehicle_Service_Update(BaseModel):
    
    id: str

    user_id:str
    customer_id:str
    vehicle_id: str
    wash_type_id: str

    comment:str
    price:float
    process_level:str


