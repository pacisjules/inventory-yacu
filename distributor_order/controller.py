from fastapi import APIRouter, HTTPException, Depends
from db.table import distr_order
from utils import util
from distributor_order import model
from configs.connection import database
import uuid
import datetime
from fastapi.responses import FileResponse

from fastapi_pagination import Page, paginate
router = APIRouter()


# All distributor orders
@router.get("/all_distributors_orders", response_model=Page[model.distributorOrderList])
async def find_all_distributor_orders(currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):
    query = distr_order.select().order_by(distr_order.c.distr_order_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)


# Find distributor with distributor ID
@router.get("/like_distributor_order_id/{distr_id}", response_model=Page[model.distributorOrderList])
async def find_like_distributor_order(distr_id: str, currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):
    query = "select * from distr_order where distr_order_id like '%{}%'".format(distr_id)
    res = await database.fetch_all(query=query, values={})
    return paginate(res)


# counting all distributors orders
@router.get("/count_distributors_orders")
async def count_all_distributor_orders_count(currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(distr_order_id) as NumberOfdstr_order FROM distr_order"
    res = await database.fetch_all(query=query, values={})
    return res

# Find one distr_order by ID
@router.get("/distr_order/{distr_order_id}", response_model=model.distributorOrderList)
async def find_distr_order_by_id(distr_order_id: str, currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):
    query = distr_order.select().where(distr_order.c.distr_order_id == distr_order_id)
    return await database.fetch_one(query)


# Find one distributor order by user
@router.get("/distr_order_user/{userId}", response_model=model.distributorOrderList)
async def find_distr_order_by_user(userId: str, currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):
    query = distr_order.select().where(distr_order.c.user_id == userId)
    return await database.fetch_one(query)


# Find one distributor order by product
@router.get("/distr_order_product/{product}", response_model=model.distributorOrderList)
async def find_distr_order_by_product(product: str, currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):
    query = distr_order.select().where(distr_order.c.product_id == product)
    return await database.fetch_one(query)


# Find item by status
@router.get("/distr_order_by_status/{status}", response_model=Page[model.distributorOrderList])
async def find_distr_order_by_status(status: str, currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):
    query = distr_order.select().where(distr_order.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)


# add new distributor order
@router.post("/add_distributor_order")
async def register_distributor_order(order: model.distributorOrderCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    # Adding distributor
    query = distr_order.insert().values(

        distr_order_id=usid,

        user_id=order.user_id,
        distributor_id=order.distributor_id,
        product_id=order.product_id,
        quantity=order.quantity,
        unit_price=order.unit_price,

        created_at=gdate,
        last_update_at=gdate,
        status="1"
    )

    await database.execute(query)

    return {
        "code": "Store: " + order.quantity,
        "Message": order.quantity+" item has been registered",
        "status": 1
    }


# Update Distributor order
@router.put("/Distributor_order_update")
async def update_item(order: model.distributorOrderUpdate, currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = distr_order.update().where(distr_order.c.distr_order_id == distr_order.distr_order_id).values(

        distr_order_id=gid,

        user_id=order.user_id,
        distributor_id=order.distributor_id,
        product_id=order.product_id,
        quantity=order.quantity,
        unit_price=order.unit_price,

        created_at=gdate,
        last_update_at=gdate,
        status="1"
    )

    await database.execute(Query)
    return ({
        "Msg:": order.quantity+" has been Updated.Thank you for using this software"
    })


# Delete distributor order
@router.delete("/Delete_distributor_order/{distributor_order_id}")
async def Delete_by_distributor_order_id(distributor_order_id: str, currentUser: model.distributorOrderList = Depends(util.get_current_active_user)):
    query = distr_order.delete().where(distr_order.c.distr_order_id == distributor_order_id)
    await database.execute(query)

    return ({
        "Msg:": "Distributor order has been deleted. Thank you for using this software"
    })
