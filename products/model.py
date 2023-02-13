from pydantic import BaseModel, Field
from typing import Optional
class productCreate(BaseModel):

    store_id:Optional[str]=Field(..., example="Store id")
    user_id:str=Field(..., example="User Id")
    category_id:Optional[str]=Field(..., example="Category id")

    product_name:str=Field(..., example="Product name")
    product_price:float=Field(..., example="Product price")

    description:str=Field(..., example="Description")
    unity_type:str=Field(..., example="Unity type")

class productList(BaseModel):

    product_id:str
    
    store_id:str
    user_id:str
    category_id:str

    product_name:str
    product_price:float

    description:str
    unity_type:str

    status: str
    created_at:str
    last_update_at:str

class productUpdate(BaseModel):
    
    product_id:str
    
    store_id:str
    user_id:str
    category_id:str

    product_name:str
    product_price:float

    description:str
    unity_type:str

    status: str
    created_at:str
    last_update_at:str

