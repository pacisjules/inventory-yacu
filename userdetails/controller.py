from fastapi import APIRouter, HTTPException, Depends
from db.table import userdetail
from utils import util
from userdetails import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All details
@router.get("/all_details", response_model=Page[model.DetailList])
async def find_all_details(currentUser: model.DetailList = Depends(util.get_current_active_user)):
    query = userdetail.select().order_by(userdetail.c.detail_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)


# # Find group with name
# @router.get("/like_group/{name}", response_model=Page[model.GroupList])
# async def find_like_group(name: str, currentUser: model.GroupList = Depends(util.get_current_active_user)):

#     query = "SELECT * FROM userGroup WHERE group_name LIKE '%{}%'".format(name)
#     res= await database.fetch_all(query=query, values={})
#     return paginate(res)



#counting all details
@router.get("/count_detail")
async def count_all_details(currentUser: model.DetailList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(detail_id) as NumberOfDetail FROM userdetail"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one detail by ID
@router.get("/detail/{detail_id}", response_model=model.DetailList)
async def find_detail_by_id(detail_id: str, currentUser: model.DetailList = Depends(util.get_current_active_user)):
    query = userdetail.select().where(userdetail.c.detail_id == detail_id)
    return await database.fetch_one(query)



# Find detail by status
@router.get("/detail_by_status/{status}", response_model=Page[model.DetailList])
async def find_detail_by_status(status: str, currentUser: model.DetailList = Depends(util.get_current_active_user)):
    query = userdetail.select().where(userdetail.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new detail
@router.post("/adddetail")
async def register_detail(details: model.DetailCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
        #Adding new group
    query = userdetail.insert().values(

            detail_id = usid,
            user_id=details.user_id,
            group_id=details.group_id, 
            section_id=details.section_id,
            
            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "Message": "New user detail code has been registered",
            "status": 1
        }



#Update currency
@router.put("/detail_update")
async def update_detail(cstm: model.DetailUpdate, currentUser: model.DetailList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = userdetail.update().where(userdetail.c.detail_id == cstm.detail_id).values(
            
            detail_id = cstm.detail_id,

            user_id=cstm.user_id,
            group_id=cstm.group_id, 
            section_id=cstm.section_id,
            
            status = "1",
            created_at = gdate,
            last_update_at=gdate
            
    )

    await database.execute(Query)
    return ({
       "Msg:":" new update has been Successfully Updated.Thank you for using this software"
    })



#Delete group
@router.delete("/Delete_detail/{detail_id}")
async def Delete_by_detail_id(detail_id: str, currentUser: model.DetailList = Depends(util.get_current_active_user)):
    query = userdetail.delete().where(userdetail.c.detail_id == detail_id)
    await database.execute(query)

    return ({
       "Msg:":"Record has been deleted .Thank you for using this software"
    })