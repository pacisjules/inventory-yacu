from fastapi import APIRouter, HTTPException, Depends
from db.table import currency
from utils import util
from currency import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All Currency
@router.get("/all_currency", response_model=Page[model.CurrencyList])
async def find_all_currency(currentUser: model.CurrencyList = Depends(util.get_current_active_user)):
    query = currency.select().order_by(currency.c.currency_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)


# Find currencys with country
@router.get("/like_currency/{country}", response_model=Page[model.CurrencyList])
async def find_like_currency(country: str, currentUser: model.CurrencyList = Depends(util.get_current_active_user)):

    query = "select * from currency where currency_country like '%{}%'".format(country)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)



#counting all currencys
@router.get("/count_currencys")
async def count_all_count(currentUser: model.CurrencyList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(currency_id) as NumberOfCountry FROM currency"
    res= await database.fetch_all(query=query, values={})
    return res
 

#Find one currency by ID
@router.get("/currency/{currency_id}", response_model=model.CurrencyList)
async def find_currency_by_id(currency_id: str, currentUser: model.CurrencyList = Depends(util.get_current_active_user)):
    query = currency.select().where(currency.c.currency_id == currency_id)
    return await database.fetch_one(query)


#Find one currency by currency code
@router.get("/currency_code/{currency_code}", response_model=model.CurrencyList)
async def find_currency_by_code(currency_code: str, currentUser: model.CurrencyList = Depends(util.get_current_active_user)):
    query = currency.select().where(currency.c.currency_code == currency_code)
    return await database.fetch_one(query)


# Find currencys by status
@router.get("/currency_by_status/{status}", response_model=Page[model.CurrencyList])
async def find_currency_by_status(status: str, currentUser: model.CurrencyList = Depends(util.get_current_active_user)):
    query = currency.select().where(currency.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new currency
@router.post("/addcurrency")
async def register_currency(currencys: model.CurrencyCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
        #Adding currency
    query = currency.insert().values(

            currency_id = usid,
            user_id=currencys.user_id,
            currency_country=currencys.currency_country, 
            description=currencys.description,
            currency_code= currencys.currency_code,
            
            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "code":"CODE: " + currencys.currency_code,
            "Message":currencys.currency_country+" code has been registered",
            "status": 1
        }



#Update currency
@router.put("/currency_update")
async def update_currency(cstm: model.CurrencyUpdate, currentUser: model.CurrencyList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = currency.update().where(currency.c.currency_id == cstm.currency_id).values(
            
            currency_id = cstm.currency_id,

            user_id=cstm.user_id,
            currency_country=cstm.currency_country, 
            currency_code= cstm.currency_code,
            description=cstm.description,
            
            status = "1",
            created_at = gdate,
            last_update_at=gdate
            
    )

    await database.execute(Query)
    return ({
       "Msg:":cstm.currency_country+" has been Updated.Thank you for using this software"
    })



#Delete currency
@router.delete("/Delete_currency/{currency_id}")
async def Delete_by_currency_id(currency_id: str, currentUser: model.CurrencyList = Depends(util.get_current_active_user)):
    query = currency.delete().where(currency.c.currency_id == currency_id)
    await database.execute(query)

    return ({
       "Msg:":"Record has been deleted .Thank you for using this software"
    })