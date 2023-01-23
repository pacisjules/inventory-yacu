from fastapi import APIRouter, HTTPException, Depends
from db.table import usergroup
from utils import util
from usergroups import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All groups
@router.get("/all_group", response_model=Page[model.GroupList])
async def find_all_groups(currentUser: model.GroupList = Depends(util.get_current_active_user)):
    query = usergroup.select().order_by(usergroup.c.created_at.desc())
    res = await database.fetch_all(query)
    return paginate(res)


# Find group with name
@router.get("/like_group/{name}", response_model=Page[model.GroupList])
async def find_like_group(name: str, currentUser: model.GroupList = Depends(util.get_current_active_user)):

    query = "SELECT * FROM usergroup WHERE group_name LIKE '%{}%'".format(name)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)



#counting all groups
@router.get("/count_groups")
async def count_all_groups(currentUser: model.GroupList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(group_id) as NumberOfGroup FROM usergroup"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one group by ID
@router.get("/group/{group_id}", response_model=model.GroupList)
async def find_group_by_id(group_id: str, currentUser: model.GroupList = Depends(util.get_current_active_user)):
    query = usergroup.select().where(usergroup.c.group_id == group_id)
    return await database.fetch_one(query)



# Find section by status
@router.get("/group_by_status/{status}", response_model=Page[model.GroupList])
async def find_group_by_status(status: str, currentUser: model.GroupList = Depends(util.get_current_active_user)):
    query = usergroup.select().where(usergroup.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new group
@router.post("/addgroup")
async def register_group(groups: model.GroupCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
        #Adding new group
    query = usergroup.insert().values(

            group_id = usid,
            user_id=groups.user_id,
            group_name=groups.group_name, 
            description=groups.description,
            
            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "Message":groups.group_name+" code has been registered",
            "status": 1
        }



#Update currency
@router.put("/group_update")
async def update_group(cstm: model.GroupUpdate, currentUser: model.GroupList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = usergroup.update().where(usergroup.c.group_id == cstm.group_id).values(
            
            group_id = cstm.group_id,

            user_id=cstm.user_id,
            group_name=cstm.group_name, 
            description=cstm.description,
            
            status = "1",
            created_at = gdate,
            last_update_at=gdate
            
    )

    await database.execute(Query)
    return ({
       "Msg:":cstm.group_name+" has been Successfully Updated.Thank you for using this software"
    })



#Delete group
@router.delete("/Delete_group/{group_id}")
async def Delete_by_group_id(group_id: str, currentUser: model.GroupList = Depends(util.get_current_active_user)):
    query = usergroup.delete().where(usergroup.c.group_id == group_id)
    await database.execute(query)

    return ({
       "Msg:":"Record has been deleted .Thank you for using this software"
    })