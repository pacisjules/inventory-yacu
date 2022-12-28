from pydantic import BaseModel, Field

class itemCreate(BaseModel):

    #item_id:str =  Field(..., example="user id")
    product_id:str =  Field(..., example="Product id")
    user_id:str =  Field(..., example="user id")
    
    quantity:int =  Field(..., example="Quantity")
    product_price:float =  Field(..., example="price")

class itemList(BaseModel):

    item_id:str
    
    product_id:str 
    user_id:str 
    quantity:int 
    product_price:float

    status: str
    created_at:str
    last_update_at:str

class itemUpdate(BaseModel):
    
    item_id:str

    product_id:str 
    user_id:str 
    quantity:int 
    product_price:float

    status: str
    created_at:str
    last_update_at:str

