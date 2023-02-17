from fastapi import APIRouter, HTTPException, Depends
from db.table import distributor
from utils import util
from distributor import model
from configs.connection import database
import uuid
import datetime
from fastapi.responses import FileResponse


from fastapi_pagination import Page, paginate
router = APIRouter()


# All distributors
@router.get("/all_distributors", response_model=Page[model.distributorList])
async def find_all_distributors(currentUser: model.distributorList = Depends(util.get_current_active_user)):
    query = distributor.select().order_by(distributor.c.distributor_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)

# Find distributor with names


@router.get("/like_distributor/{name}", response_model=Page[model.distributorList])
async def find_like_distributor(name: str, currentUser: model.distributorList = Depends(util.get_current_active_user)):
    query = "select * from distributor where names like '%{}%'".format(name)
    res = await database.fetch_all(query=query, values={})
    return paginate(res)


# counting all distributors
@router.get("/count_distributors")
async def count_all_distributors_count(currentUser: model.distributorList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(distributor_id) as NumberOfdstr FROM distributor"
    res = await database.fetch_all(query=query, values={})
    return res


# Find one distributor by ID
@router.get("/distributor/{distributor_id}", response_model=model.distributorList)
async def find_distributor_by_id(distributor_id: str, currentUser: model.distributorList = Depends(util.get_current_active_user)):
    query = distributor.select().where(distributor.c.distributor_id == distributor_id)
    return await database.fetch_one(query)


# Find one distributor by phone
@router.get("/distributor_phone/{phone}", response_model=model.distributorList)
async def find_distributor_by_phone(phone: str, currentUser: model.distributorList = Depends(util.get_current_active_user)):
    query = distributor.select().where(distributor.c.phone == phone)
    return await database.fetch_one(query)


# Find one distributor by user
@router.get("/distributor_user/{userId}", response_model=model.distributorList)
async def find_distributor_by_user(userId: str, currentUser: model.distributorList = Depends(util.get_current_active_user)):
    query = distributor.select().where(distributor.c.user_id == userId)
    return await database.fetch_one(query)


# Find distributor by status
@router.get("/distributor_by_status/{status}", response_model=Page[model.distributorList])
async def find_distributor_by_status(status: str, currentUser: model.distributorList = Depends(util.get_current_active_user)):
    query = distributor.select().where(distributor.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)


# add new distributor
@router.post("/add_distributor")
async def register_distributor(dsrt: model.distributorCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    # Adding distributor
    query = distributor.insert().values(

        distributor_id=usid,

        user_id=dsrt.user_id,
        names=dsrt.names,
        email=dsrt.email,
        phone=dsrt.phone,
        address=dsrt.address,

        created_at=gdate,
        last_update_at=gdate,
        status="1"
    )

    await database.execute(query)

    return {
        "code": "Store: " + dsrt.names,
        "Message": dsrt.names+" Distributor has been registered",
        "status": 1
    }


# Update distributor
@router.put("/distributor_update")
async def update_distributor(dsrt: model.distributorUpdate, currentUser: model.distributorList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = distributor.update().where(distributor.c.distributor_id == distributor.distributor_id).values(

        distributor_id=gid,

        user_id=dsrt.user_id,
        names=dsrt.names,
        email=dsrt.email,
        phone=dsrt.phone,
        address=dsrt.address,

        created_at=gdate,
        last_update_at=gdate,
        status="1"
    )

    await database.execute(Query)
    return ({
        "Msg:": dsrt.names+" has been Updated.Thank you for using this software"
    })


# Delete distributor
@router.delete("/Delete_distributor/{distributor_id}")
async def Delete_by_distributor_id(distributor_id: str, currentUser: model.distributorList = Depends(util.get_current_active_user)):
    query = distributor.delete().where(distributor.c.distributor_id == distributor_id)
    await database.execute(query)

    return ({
        "Msg:": "Distributor has been deleted. Thank you for using this software"
    })
