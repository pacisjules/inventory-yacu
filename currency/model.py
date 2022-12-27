from pydantic import BaseModel, Field

class CurrencyCreate(BaseModel):

    #currency_id:str =  Field(..., example="Enter currency id")
    user_id:str =  Field(..., example="user id")
    currency_country:str =  Field(..., example="Currency country")
    description: str = Field(..., example="description")
    currency_code: str = Field(..., example="currency code")


class CurrencyList(BaseModel):

    currency_id:str 
    user_id:str 
    currency_country:str 
    currency_code: str 
    description: str

    status: str
    created_at:str
    last_update_at:str

class CurrencyUpdate(BaseModel):
    
    currency_id:str 
    user_id:str 
    currency_country:str 
    currency_code: str 
    description: str

    status: str
    created_at:str
    last_update_at:str


