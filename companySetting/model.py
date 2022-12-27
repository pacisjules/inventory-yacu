from pydantic import BaseModel, Field

class companySettingCreate(BaseModel):
    user_id:str =  Field(..., example="user id")
    currency_id:str =  Field(..., example="currency id")
    organization_name:str =  Field(..., example="Organisation names")
    organization_tel:str =  Field(..., example="org tel")
    organization_tel2:str =  Field(..., example="org tel2")
    organization_fax:str =  Field(..., example="org fax")
    organization_email:str =  Field(..., example="org email")
    organization_address:str =  Field(..., example="org address 1")
    organization_address2:str =  Field(..., example="org address 2")
    organization_street:str =  Field(..., example="org street")
    organization_city:str =  Field(..., example="org city")
    organization_state:str =  Field(..., example="org state")
    zip_code:str =  Field(..., example="org code")
    organization_website:str =  Field(..., example="org website")
    organization_description:str =  Field(..., example="org description")
    country_id:str =  Field(..., example="org country")
    organization_reg_number:str =  Field(..., example="org registration number")
    organization_affiliation_num:str =  Field(..., example="org Affiliation")
    organization_logo:str =  Field(..., example="org logo")
    organization_head:str =  Field(..., example="org head")
    organization_footer_note:str =  Field(..., example="org note")
    status:str = Field(..., example="org Status")
    created_at:str =  Field(..., example="created_at")
    last_update_at:str =  Field(..., example="Last Update")

class companySettingList(BaseModel):

    org_setting_id:str
    user_id:str 
    currency_id:str 
    organization_name:str
    organization_tel:str 
    organization_tel2:str
    organization_email:str
    organization_address:str
    organization_address2:str
    organization_street:str
    organization_city:str
    organization_state:str 
    zip_code:str 
    organization_website:str 
    organization_description:str 
    country_id:str 
    organization_reg_number:str
    organization_affiliation_num:str
    organization_logo:str 
    organization_head:str 
    organization_footer_note:str
    status:str
    created_at:str
    last_update_at:str

class companySettingUpdate(BaseModel):
    
    org_setting_id:str
    user_id:str 
    currency_id:str 
    organization_name:str
    organization_tel:str 
    organization_tel2:str
    organization_email:str
    organization_address:str
    organization_address2:str
    organization_street:str
    organization_city:str
    organization_state:str 
    zip_code:str 
    organization_website:str 
    organization_description:str 
    country_id:str 
    organization_reg_number:str
    organization_affiliation_num:str
    organization_logo:str 
    organization_head:str 
    organization_footer_note:str
    status:str
    created_at:str
    last_update_at:str


