from pydantic import BaseModel, Field


class distributorOrderCreate(BaseModel):

    user_id:str =  Field(..., example="user id")
    distributor_id:str =  Field(..., example="distributor id")
    product_id:str =  Field(..., example="product id")
    quantity:int =  Field(..., example="quantity")
    unit_price:int =  Field(..., example="unit price")


class distributorOrderList(BaseModel):

    distr_order_id:str
    user_id:str
    distributor_id:str
    
    user_id:str
    distributor_id:str 
    product_id:str
    quantity:int 
    unit_price:int

    status: str
    created_at:str
    last_update_at:str


class distributorOrderUpdate(BaseModel):
    
    distr_order_id:str
    user_id:str
    distributor_id:str
    
    user_id:str
    distributor_id:str 
    product_id:str
    quantity:int 
    unit_price:int

    status: str
    created_at:str
    last_update_at:str

