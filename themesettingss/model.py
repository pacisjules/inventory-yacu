from pydantic import BaseModel, Field

class themesettingCreate(BaseModel):

    #theme_id_id:str =  Field(..., example="Enter currency id")
    user_id:str =  Field(..., example="user id")
    theme_name:str =  Field(..., example="Theme name")



class themesettingList(BaseModel):

    theme_id:str 
    user_id:str 
    theme_name:str 

    status: str
    created_at:str
    last_update_at:str

class themesettingUpdate(BaseModel):
    
    theme_id:str 
    user_id:str 
    theme_name:str 

    status: str
    created_at:str
    last_update_at:str


