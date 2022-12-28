from fastapi import APIRouter, HTTPException, Depends
from db.table import themesetting
from utils import util
from themesettingss import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All groups
@router.get("/all_theme", response_model=Page[model.themesettingList])
async def find_all_groups(currentUser: model.themesettingList = Depends(util.get_current_active_user)):
    query = themesetting.select().order_by(themesetting.c.theme_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)


# Find theme with name
@router.get("/like_theme/{name}", response_model=Page[model.themesettingList])
async def find_like_theme(name: str, currentUser: model.themesettingList = Depends(util.get_current_active_user)):

    query = "SELECT * FROM themesetting WHERE theme_name LIKE '%{}%'".format(name)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)



#counting all themes
@router.get("/count_themes")
async def count_all_themes(currentUser: model.themesettingList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(theme_id) as NumberOfTheme FROM themesetting"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one theme by ID
@router.get("/theme/{theme_id}", response_model=model.themesettingList)
async def find_theme_by_id(theme_id: str, currentUser: model.themesettingList = Depends(util.get_current_active_user)):
    query = themesetting.select().where(themesetting.c.theme_id == theme_id)
    return await database.fetch_one(query)



# Find theme by status
@router.get("/theme_by_status/{status}", response_model=Page[model.themesettingList])
async def find_theme_by_status(status: str, currentUser: model.themesettingList = Depends(util.get_current_active_user)):
    query = themesetting.select().where(themesetting.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new theme
@router.post("/addtheme")
async def register_group(themes: model.themesettingCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
        #Adding new group
    query = themesetting.insert().values(

            theme_id = usid,
            user_id=themes.user_id,
            theme_name=themes.theme_name, 
            
            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "Message":themes.theme_name+" code has been registered",
            "status": 1
        }



#Update theme
@router.put("/theme_update")
async def update_theme(cstm: model.themesettingUpdate, currentUser: model.themesettingList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = themesetting.update().where(themesetting.c.theme_id == cstm.theme_id).values(
            
            theme_id = cstm.theme_id,

            user_id=cstm.user_id,
            theme_name=cstm.theme_name, 
            
            status = "1",
            created_at = gdate,
            last_update_at=gdate
            
    )

    await database.execute(Query)
    return ({
       "Msg:":cstm.theme_name+" has been Successfully Updated.Thank you for using this software"
    })



#Delete theme
@router.delete("/Delete_theme/{theme_id}")
async def Delete_by_theme_id(theme_id: str, currentUser: model.themesettingList = Depends(util.get_current_active_user)):
    query = themesetting.delete().where(themesetting.c.theme_id == theme_id)
    await database.execute(query)

    return ({
       "Msg:":"Record has been deleted .Thank you for using this software"
    })