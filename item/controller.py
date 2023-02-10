from fastapi import APIRouter, HTTPException, Depends
from db.table import item
from utils import util
from item import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()



# All items
@router.get("/all_item", response_model=Page[model.itemList])
async def find_all_items(currentUser: model.itemList = Depends(util.get_current_active_user)):
    query = item.select().order_by(item.c.item_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)



# Find item with names
@router.get("/like_item/{name}", response_model=Page[model.itemList])
async def find_like_item(name: str, currentUser: model.itemList = Depends(util.get_current_active_user)):
    query = "select * from item where item_name like '%{}%'".format(name)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)


#counting all item
@router.get("/count_items")
async def count_all_count(currentUser: model.itemList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(item_id) as NumberOfitems FROM item"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one item by ID
@router.get("/item/{item_id}", response_model=model.itemList)
async def find_item_by_id(item_id: str, currentUser: model.itemList = Depends(util.get_current_active_user)):
    query = item.select().where(item.c.item_id == item_id)
    return await database.fetch_one(query)

#Find one item by item price
@router.get("/item/{price}", response_model=model.itemList)
async def find_item_by_item_price(price: str, currentUser: model.itemList = Depends(util.get_current_active_user)):
    query = item.select().where(item.c.product_price == price)
    return await database.fetch_one(query)


#Find one item by users
@router.get("/item_user{userId}", response_model=model.itemList)
async def find_item_by_user(userId: str, currentUser: model.itemList = Depends(util.get_current_active_user)):
    query = item.select().where(item.c.user_id == userId)
    return await database.fetch_one(query)


# Find item by status
@router.get("/item_by_status/{status}", response_model=Page[model.itemList])
async def find_item_by_status(status: str, currentUser: model.itemList = Depends(util.get_current_active_user)):
    query = item.select().where(item.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new item
@router.post("/additem")
async def register_store(itm: model.itemCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
    
    #Adding item
    query = item.insert().values(

            item_id = usid,

            product_id=itm.product_id,
            user_id= itm.user_id,
            quantity=itm.quantity,
            product_price=itm.product_price,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "code":"Store: " + itm.item_name,
            "Message":itm.item_name+" item has been registered",
            "status": 1
        }


#Update item
@router.put("/item_update")
async def update_item(itm: model.itemUpdate, currentUser: model.itemList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = item.update().where(item.c.item_id == itm.item_id).values(
            
            item_id = gid,

            product_id=itm.product_id,
            user_id= itm.user_id,
            quantity=itm.quantity,
            product_price=itm.product_price,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
    )

    await database.execute(Query)
    return ({
       "Msg:":itm.item_name+" has been Updated.Thank you for using this software"
    })


#Delete item
@router.delete("/Delete_item/{item_id}")
async def Delete_by_item_id(item_id: str, currentUser: model.itemList = Depends(util.get_current_active_user)):
    query = item.delete().where(item.c.item_id == item_id)
    await database.execute(query)

    return ({
       "Msg:":"item has been deleted. Thank you for using this software"
    })