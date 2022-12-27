from pydantic import BaseModel, Field

class GroupCreate(BaseModel):

    #group_id:str =  Field(..., example="Enter currency id")
    user_id:str =  Field(..., example="user id")
    group_name:str =  Field(..., example="Group name")
    description: str = Field(..., example="description")



class GroupList(BaseModel):

    group_id:str 
    user_id:str 
    group_name:str 
    description: str

    status: str
    created_at:str
    last_update_at:str

class GroupUpdate(BaseModel):
    
    group_id:str 
    user_id:str 
    group_name:str 
    description: str

    status: str
    created_at:str
    last_update_at:str


