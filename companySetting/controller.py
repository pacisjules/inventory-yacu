from fastapi import APIRouter, HTTPException, Depends
from db.table import companySetting
from utils import util
from companySetting import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All companySetting
@router.get("/all_companySetting", response_model=Page[model.companySettingList])
async def find_all_companySettings(currentUser: model.companySettingList = Depends(util.get_current_active_user)):
    query = companySetting.select().order_by(companySetting.c.org_setting_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)




# Find companySettings with names
@router.get("/like_companySetting/{names}", response_model=Page[model.companySettingList])
async def find_like_companySetting(names: str, currentUser: model.companySettingList = Depends(util.get_current_active_user)):

    query = "select * from companySetting where organization_name like '%{}%'".format(names)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)

#counting all companySettings
@router.get("/count_companySettings")
async def count_all_companies(currentUser: model.companySettingList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(org_setting_id) as NumberOfCompanies FROM companySetting"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one companySetting by ID
@router.get("/companySetting/{org_setting_id}", response_model=model.companySettingList)
async def find_companySetting_by_id(org_setting_id: str, currentUser: model.companySettingList = Depends(util.get_current_active_user)):
    query = companySetting.select().where(companySetting.c.org_setting_id == org_setting_id)
    return await database.fetch_one(query)





#Find one companySetting by tel 1
@router.get("/companySetting_tel/{organization_tel}", response_model=model.companySettingList)
async def find_companySetting_by_telephone(organization_tel: str, currentUser: model.companySettingList = Depends(util.get_current_active_user)):
    query = companySetting.select().where(companySetting.c.organization_tel == organization_tel)
    return await database.fetch_one(query)


#Find one companySetting by tel 2
@router.get("/companySetting_tel1/{organization_tel2}", response_model=model.companySettingList)
async def find_companySetting_by_telephone(organization_tel2: str, currentUser: model.companySettingList = Depends(util.get_current_active_user)):
    query = companySetting.select().where(companySetting.c.organization_tel2 == organization_tel2)
    return await database.fetch_one(query)


# Find companySettings by status
@router.get("/companySetting_by_status/{status}", response_model=Page[model.companySettingList])
async def find_companySetting_by_status(status: str, currentUser: model.companySettingList = Depends(util.get_current_active_user)):
    query = companySetting.select().where(companySetting.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)






# add new companySetting
@router.post("/addcompanySetting")
async def register_companySetting(companySettings: model.companySettingCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
   

    #Adding companySetting
    query = companySetting.insert().values(

            org_setting_id= usid,

            user_id=companySettings.user_id,
            currency_id=companySettings.currency_id, 
            organization_name=companySettings.organization_name,
            organization_tel=companySettings.organization_tel, 
            organization_tel2=companySettings.organization_tel2,
            organization_email=companySettings.organization_email,
            organization_address=companySettings.organization_address,
            organization_address2=companySettings.organization_address2,
            organization_street=companySettings.organization_street,
            organization_city=companySettings.organization_city,
            organization_state=companySettings.organization_state, 
            zip_code=companySettings.zip_code, 
            organization_website=companySettings.organization_website,
            organization_description=companySettings.organization_description,
            country_id=companySettings.country_id,
            organization_reg_number=companySettings.organization_reg_number,
            organization_affiliation_num=companySettings.organization_affiliation_num,
            organization_logo=companySettings.organization_logo,
            organization_head=companySettings.organization_head, 
            organization_footer_note=companySettings.organization_footer_note,
            
            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "code":"ORGANISATION: " + companySettings.organization_name,
            "Message":companySettings.organization_name+"  has been registered",
            "status": 1
        }



#Update companySetting
@router.put("/companySetting_update")
async def update_companySetting(companySettings: model.companySettingUpdate, currentUser: model.companySettingList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = companySetting.update().where(companySetting.c.org_setting_id == companySettings.org_setting_id).values(
            
            org_setting_id= gid,

            user_id=companySettings.user_id,
            currency_id=companySettings.currency_id, 
            organization_name=companySettings.organization_name,
            organization_tel=companySettings.organization_tel, 
            organization_tel2=companySettings.organization_tel2,
            organization_email=companySettings.organization_email,
            organization_address=companySettings.organization_address,
            organization_address2=companySettings.organization_address2,
            organization_street=companySettings.organization_street,
            organization_city=companySettings.organization_city,
            organization_state=companySettings.organization_state, 
            zip_code=companySettings.zip_code, 
            organization_website=companySettings.organization_website,
            organization_description=companySettings.organization_description,
            country_id=companySettings.country_id,
            organization_reg_number=companySettings.organization_reg_number,
            organization_affiliation_num=companySettings.organization_affiliation_num,
            organization_logo=companySettings.organization_logo,
            organization_head=companySettings.organization_head, 
            organization_footer_note=companySettings.organization_footer_note,
            
            created_at = gdate,
            last_update_at=gdate,
            status = "1"
            
    )

    await database.execute(Query)
    return ({
       "Msg:":companySettings.organization_name+" has been Updated. Thank you for using this software"
    })



#Delete companySetting
@router.delete("/Delete_companySetting/{org_setting_id}")
async def Delete_by_companySetting_id(org_setting_id: str, currentUser: model.companySettingList = Depends(util.get_current_active_user)):
    query = companySetting.delete().where(companySetting.c.org_setting_id == org_setting_id)
    await database.execute(query)

    return ({
       "Msg:":"Record has been deleted .Thank you for using this software"
    })