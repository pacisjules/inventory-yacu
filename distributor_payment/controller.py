from fastapi import APIRouter, HTTPException, Depends
from db.table import distr_payment
from utils import util
from distributor_payment import model
from configs.connection import database
import uuid
import datetime
from fastapi.responses import FileResponse

from fastapi_pagination import Page, paginate
router = APIRouter()


# All distributor order payment
@router.get("/all_distributors_order_payment", response_model=Page[model.distributorPaymentList])
async def find_all_distributor_orders(currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):
    query = distr_payment.select().order_by(distr_payment.c.distr_payment_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)


# Find distributor order with distributor order ID
@router.get("/like_distributor_order_payment_id/{distr_id}", response_model=Page[model.distributorPaymentList])
async def find_like_distributor_order_payment(distr_id: str, currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):
    query = "select * from distr_payment where distr_payment_id like '%{}%'".format(distr_id)
    res = await database.fetch_all(query=query, values={})
    return paginate(res)


# counting all distributors order payment
@router.get("/count_distributors_order_payment")
async def count_all_distributor_orders_payment_count(currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(distributor_id) as NumberOfdstr_order FROM distr_payment"
    res = await database.fetch_all(query=query, values={})
    return res

# Find one distr_payment_payment by ID
@router.get("/distr_payment_payment/{distr_payment_id}", response_model=model.distributorPaymentList)
async def find_distr_payment_by_id(distr_payment_id: str, currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):
    query = distr_payment.select().where(distr_payment.c.distr_payment_id == distr_payment_id)
    return await database.fetch_one(query)


# Find one distributor order by user
@router.get("/distr_payment_user/{userId}", response_model=model.distributorPaymentList)
async def find_distr_order_payment_by_user(userId: str, currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):
    query = distr_payment.select().where(distr_payment.c.user_id == userId)
    return await database.fetch_one(query)


# Find one distributor order by product
@router.get("/distr_payment_product/{product}", response_model=model.distributorPaymentList)
async def find_distr_payment_by_product(product: str, currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):
    query = distr_payment.select().where(distr_payment.c.product_id == product)
    return await database.fetch_one(query)


# Find item by status
@router.get("/distr_order_payment_by_status/{status}", response_model=Page[model.distributorPaymentList])
async def find_distr_order_payment_by_status(status: str, currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):
    query = distr_payment.select().where(distr_payment.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)


# add new distributor order payment
@router.post("/add_distributor_order_payment")
async def register_distributor_order(order: model.distributorPaymentCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    # Adding distributor
    query = distr_payment.insert().values(

        distr_payment_id=usid,

        payed_status=order.payed_status,
        payed_amount=order.payed_amount,

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
@router.put("/Distributor_order_payment_update")
async def update_item(order: model.distributorPaymentUpdate, currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = distr_payment.update().where(distr_payment.c.distr_payment_id == order.distr_payment_id).values(

        distr_payment_id=gid,

        payed_status=order.payed_status,
        payed_amount=order.payed_amount,

        created_at=gdate,
        last_update_at=gdate,
        status="1"
    )

    await database.execute(Query)
    return ({
        "Msg:": order.quantity+" has been Updated.Thank you for using this software"
    })


# Delete distributor order
@router.delete("/Delete_distributor_order_payment/{distr_payment_id}")
async def Delete_by_distributor_order_id(distr_payment_id: str, currentUser: model.distributorPaymentList = Depends(util.get_current_active_user)):
    query = distr_payment.delete().where(distr_payment.c.distr_payment_id == distr_payment_id)
    await database.execute(query)

    return ({
        "Msg:": "Distributor order payment order has been deleted. Thank you for using this software"
    })
