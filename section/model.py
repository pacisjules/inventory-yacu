from pydantic import BaseModel, Field

class SectionCreate(BaseModel):

    #section_id:str =  Field(..., example="Enter currency id")
    user_id:str =  Field(..., example="user id")
    section_name:str =  Field(..., example="Section name")
    description: str = Field(..., example="description")



class SectionList(BaseModel):

    section_id:str 
    user_id:str 
    section_name:str 
    description: str

    status: str
    created_at:str
    last_update_at:str

class SectionUpdate(BaseModel):
    
    section_id:str 
    user_id:str 
    section_name:str 
    description: str

    status: str
    created_at:str
    last_update_at:str


