from fastapi import APIRouter, HTTPException, Depends
from db.table import usersection
from utils import util
from usersections import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All Sections
@router.get("/all_section", response_model=Page[model.SectionList])
async def find_all_sections(currentUser: model.SectionList = Depends(util.get_current_active_user)):
    query = usersection.select().order_by(usersection.c.section_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)


# Find section with name
@router.get("/like_section/{Uname}", response_model=Page[model.SectionList])
async def find_like_section(Uname: str, currentUser: model.SectionList = Depends(util.get_current_active_user)):

    query = "SELECT * FROM usersection WHERE section_name LIKE '%{}%'".format(Uname)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)



#counting all sections
@router.get("/count_sections")
async def count_all_sections(currentUser: model.SectionList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(section_id) as NumberOfSections FROM usersection"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one section by ID
@router.get("/section/{section_id}", response_model=model.SectionList)
async def find_section_by_id(section_id: str, currentUser: model.SectionList = Depends(util.get_current_active_user)):
    query = usersection.select().where(usersection.c.section_id == section_id)
    return await database.fetch_one(query)



# Find section by status
@router.get("/section_by_status/{status}", response_model=Page[model.SectionList])
async def find_section_by_status(status: str, currentUser: model.SectionList = Depends(util.get_current_active_user)):
    query = usersection.select().where(usersection.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new currency
@router.post("/addsection")
async def register_section(sections: model.SectionCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
        #Adding new section
    query = usersection.insert().values(

            section_id = usid,
            user_id=sections.user_id,
            section_name=sections.section_name, 
            description=sections.description,
            
            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "Message":sections.section_name+" code has been registered",
            "status": 1
        }



#Update currency
@router.put("/section_update")
async def update_section(cstm: model.SectionUpdate, currentUser: model.SectionList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = usersection.update().where(usersection.c.section_id == cstm.section_id).values(
            
            section_id = cstm.section_id,

            user_id=cstm.user_id,
            section_name=cstm.section_name, 
            description=cstm.description,
            
            status = "1",
            created_at = gdate,
            last_update_at=gdate
            
    )

    await database.execute(Query)
    return ({
       "Msg:":cstm.section_name+" has been Successfully Updated.Thank you for using this software"
    })



#Delete currency
@router.delete("/Delete_section/{section_id}")
async def Delete_by_section_id(section_id: str, currentUser: model.SectionList = Depends(util.get_current_active_user)):
    query = usersection.delete().where(usersection.c.section_id == section_id)
    await database.execute(query)

    return ({
       "Msg:":"Record has been deleted .Thank you for using this software"
    })