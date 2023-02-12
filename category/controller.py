from fastapi import APIRouter, HTTPException, Depends
from db.table import category
from utils import util
from category import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All categories
@router.get("/all_category", response_model=Page[model.categoryList])
async def find_all_categories(currentUser: model.categoryList = Depends(util.get_current_active_user)):
    query = category.select().order_by(category.c.category_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)



# Find category with names
@router.get("/like_category/{name}", response_model=Page[model.categoryList])
async def find_like_category(name: str, currentUser: model.categoryList = Depends(util.get_current_active_user)):

    query = "select * from category where category_name like '%{}%'".format(name)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)


#counting all category
@router.get("/count_categorys")
async def count_all_count(currentUser: model.categoryList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(category_id) FROM category"
    res= await database.fetch_all(query=query, values={})
    return res
# all category names
@router.get("/category_names")
async def get_category_names(currentUser: model.categoryList = Depends(util.get_current_active_user)):
    query = "SELECT category_name  FROM category"
    res= await database.fetch_all(query=query, values={})
    return res 

#Find one category by ID
@router.get("/category/{category_id}", response_model=model.categoryList)
async def find_category_by_id(category_id: str, currentUser: model.categoryList = Depends(util.get_current_active_user)):
    query = category.select().where(category.c.category_id == category_id)
    return await database.fetch_one(query)


#Find one category by users
@router.get("/category_user{userId}", response_model=model.categoryList)
async def find_category_by_user(userId: str, currentUser: model.categoryList = Depends(util.get_current_active_user)):
    query = category.select().where(category.c.user_id == userId)
    return await database.fetch_one(query)


# Find category by status
@router.get("/category_by_status/{status}", response_model=Page[model.categoryList])
async def find_category_by_status(status: str, currentUser: model.categoryList = Depends(util.get_current_active_user)):
    query = category.select().where(category.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new category
@router.post("/addcategory")
async def register_category(ctgr: model.categoryCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
    
    #Adding category
    query = category.insert().values(

            category_id = usid,
            
            user_id=ctgr.user_id,
            store_id=ctgr.store_id,
            category_name=ctgr.category_name,
            description=ctgr.description,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "code":"Store: " + ctgr.category_name,
            "Message":ctgr.category_name+" category has been registered",
            "status": 1
        }


#Update category
@router.put("/category_update")
async def update_category(ctgr: model.categoryUpdate, currentUser: model.categoryList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = category.update().where(category.c.category_id == ctgr.category_id).values(
            
            category_id = gid,
            
            user_id=ctgr.user_id,
            store_id=ctgr.store_id,
            category_name=ctgr.category_name,
            description=ctgr.description,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
    )

    await database.execute(Query)
    return ({
       "Msg:":ctgr.category_name+" has been Updated.Thank you for using this software"
    })


#Delete category
@router.delete("/Delete_category/{category_id}")
async def Delete_by_category_id(category_id: str, currentUser: model.categoryList = Depends(util.get_current_active_user)):
    query = category.delete().where(category.c.category_id == category_id)
    await database.execute(query)

    return ({
       "Msg:":"Category has been deleted. Thank you for using this software"
    })