from fastapi import APIRouter, HTTPException, Depends
from db.table import orders
from utils import util
from orders import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()



# All orders
@router.get("/all_orders", response_model=Page[model.orderList])
async def find_all_orders(currentUser: model.orderList = Depends(util.get_current_active_user)):
    query = orders.select().orders_by(orders.c.order_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)

# Find orders with customer id
@router.get("/like_orders/{customer}", response_model=Page[model.orderList])
async def find_like_orders(customer: str, currentUser: model.orderList = Depends(util.get_current_active_user)):
    query = "select * from orders where cust_id like '%{}%'".format(customer)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)


#counting all orders
@router.get("/count_orderss")
async def count_all_count(currentUser: model.orderList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(orders_id) as NumberOforderss FROM orders"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one orders by ID
@router.get("/orders/{order_id}", response_model=model.orderList)
async def find_orders_by_id(order_id: str, currentUser: model.orderList = Depends(util.get_current_active_user)):
    query = orders.select().where(orders.c.order_id == order_id)
    return await database.fetch_one(query)


#Find one orders by order date
@router.get("/orders/{date}", response_model=model.orderList)
async def find_orders_by_date(date: str, currentUser: model.orderList = Depends(util.get_current_active_user)):
    query = orders.select().where(orders.c.order_date == date)
    return await database.fetch_one(query)


#Find one orders by users
@router.get("/orders_user{userId}", response_model=model.orderList)
async def find_orders_by_user(userId: str, currentUser: model.orderList = Depends(util.get_current_active_user)):
    query = orders.select().where(orders.c.user_id == userId)
    return await database.fetch_one(query)


# Find orders by status
@router.get("/orders_by_status/{status}", response_model=Page[model.orderList])
async def find_orders_by_status(status: str, currentUser: model.orderList = Depends(util.get_current_active_user)):
    query = orders.select().where(orders.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new orders
@router.post("/addOrder")
async def register_Order(ords: model.orderCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
    
    #Adding orders
    query = orders.insert().values(

            order_id=usid,

            item_id=ords.item_id,
            user_id=ords.user_id,
            cust_id=ords.cust_id,
            quantity=ords.quantity,
            total_price=ords.total_price,
            order_date=ords.order_date,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "code":"Store: " + ords.order_id,
            "Message":ords.order_id+" order has been runned",
            "status": 1
        }


#Update orders
@router.put("/orders_update")
async def update_orders(ords: model.orderUpdate, currentUser: model.orderList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = orders.update().where(orders.c.order_id == ords.order_id).values(
            
            order_id=gid,

            item_id=ords.item_id,
            user_id=ords.user_id,
            cust_id=ords.cust_id,
            quantity=ords.quantity,
            total_price=ords.total_price,
            order_date=ords.order_date,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
    )

    await database.execute(Query)
    return ({
       "Msg:":ords.orders_name+" has been Updated.Thank you for using this software"
    })


#Delete orders
@router.delete("/Delete_orders/{order_id}")
async def Delete_by_orders_id(order_id: str, currentUser: model.orderList = Depends(util.get_current_active_user)):
    query = orders.delete().where(orders.c.order_id == order_id)
    await database.execute(query)

    return ({
       "Msg:":"order has been deleted. Thank you for using this software"
    })