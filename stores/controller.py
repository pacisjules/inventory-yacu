from fastapi import APIRouter, HTTPException, Depends
from db.table import stores
from utils import util
from stores import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All stores
@router.get("/all_stores", response_model=Page[model.storeList])
async def find_all_stores(currentUser: model.storeList = Depends(util.get_current_active_user)):
    query = stores.select().order_by(stores.c.store_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)



# Find stores with names
@router.get("/like_stores/{name}", response_model=Page[model.storeList])
async def find_like_stores(name: str, currentUser: model.storeList = Depends(util.get_current_active_user)):

    query = "select * from stores where stores_name like '%{}%'".format(name)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)



#counting all storess
@router.get("/count_storess")
async def count_all_count(currentUser: model.storeList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(store_id) as NumberOfStores FROM stores"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one stores by ID
@router.get("/stores/{stores_id}", response_model=model.storeList)
async def find_stores_by_id(stores_id: str, currentUser: model.storeList = Depends(util.get_current_active_user)):
    query = stores.select().where(stores.c.store_id == stores_id)
    return await database.fetch_one(query)





#Find one stores by users
@router.get("/stores_user{userId}", response_model=model.storeList)
async def find_stores_by_user(userId: str, currentUser: model.storeList = Depends(util.get_current_active_user)):
    query = stores.select().where(stores.c.user_id == userId)
    return await database.fetch_one(query)


# Find stores by status
@router.get("/stores_by_status/{status}", response_model=Page[model.storeList])
async def find_stores_by_status(status: str, currentUser: model.storeList = Depends(util.get_current_active_user)):
    query = stores.select().where(stores.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new stores
@router.post("/add_store")
async def register_store(stor: model.storeCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
    
    #Adding stores
    query = stores.insert().values(

            store_id = usid,
            
            user_id=stor.user_id,
            store_name=stor.store_name,
            address=stor.address,
            description=stor.description,
            org_setting_id=stor.org_setting_id,
            
            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "code":"Store: " + stor.store_name,
            "Message":stor.store_name+" code has been registered",
            "status": 1
        }



#Update stores
@router.put("/stores_update")
async def update_stores(stor: model.storeUpdate, currentUser: model.storeList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = stores.update().where(stores.c.store_id == stor.store_id).values(
            
            store_id = gid,
            
            user_id=stor.user_id,
            store_name=stor.store_name,
            address=stor.address,
            description=stor.description,
            org_setting_id=stor.org_setting_id,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
            
    )

    await database.execute(Query)
    return ({
       "Msg:":stor.store_name+" has been Updated.Thank you for using this software"
    })





#Delete stores
@router.delete("/Delete_stores/{store_id}")
async def Delete_by_stores_id(store_id: str, currentUser: model.storeList = Depends(util.get_current_active_user)):
    query = stores.delete().where(stores.c.store_id == store_id)
    await database.execute(query)

    return ({
       "Msg:":"Store has been deleted .Thank you for using this software"
    })