from pydantic import BaseModel, Field

class orderCreate(BaseModel):

    item_id:str =  Field(..., example="item id")
    user_id:str =  Field(..., example="user id")
    cust_id:str =  Field(..., example="customer id")
    
    quantity:int =  Field(..., example="Quantity")
    total_price:float =  Field(..., example="price")

class orderList(BaseModel):

    order_id:str

    item_id:str 
    user_id:str 
    cust_id:str 
    quantity:int 
    total_price:float 

    order_date:str 
    status: str
    created_at:str
    last_update_at:str

class orderUpdate(BaseModel):
    

    order_id:str

    item_id:str 
    user_id:str 
    cust_id:str 
    quantity:int 
    total_price:float 
    
    order_date:str 
    status: str
    created_at:str
    last_update_at:str

