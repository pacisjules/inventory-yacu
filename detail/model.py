from pydantic import BaseModel, Field

class DetailCreate(BaseModel):

    #detail_id:str =  Field(..., example="Enter currency id")
    user_id:str =  Field(..., example="user id")
    group_id:str =  Field(..., example="Group id")
    section_id: str = Field(..., example="section id")



class DetailList(BaseModel):

    detail_id:str 
    user_id:str 
    group_id:str 
    section_id: str

    status: str
    created_at:str
    last_update_at:str

class DetailUpdate(BaseModel):
    
    detail_id:str 
    user_id:str 
    group_id:str 
    section_id: str

    status: str
    created_at:str
    last_update_at:str


