from pydantic import BaseModel, Field


class distributorPaymentCreate(BaseModel):

    user_id:str =  Field(..., example="user id")
    distributor_id:str =  Field(..., example="distributor id")
    product_id:str =  Field(..., example="product id")
    payed_status:str =  Field(..., example="payed status")
    payed_amount:float =  Field(..., example="payed amount")


class distributorPaymentList(BaseModel):

    distr_payment_id:str
    user_id:str
    distributor_id:str
    product_id:str
    
    payed_status:str 
    payed_amount:float 

    status: str
    created_at:str
    last_update_at:str


class distributorPaymentUpdate(BaseModel):
    
    distr_payment_id:str
    user_id:str
    distributor_id:str
    product_id:str
    
    payed_status:str 
    payed_amount:float 

    status: str
    created_at:str
    last_update_at:str

