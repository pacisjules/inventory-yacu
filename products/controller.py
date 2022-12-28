from fastapi import APIRouter, HTTPException, Depends
from db.table import product
from utils import util
from products import model
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()




# All products
@router.get("/all_product", response_model=Page[model.productList])
async def find_all_products(currentUser: model.productList = Depends(util.get_current_active_user)):
    query = product.select().order_by(product.c.product_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)



# Find product with name
@router.get("/like_product/{name}", response_model=Page[model.productList])
async def find_like_product(name: str, currentUser: model.productList = Depends(util.get_current_active_user)):

    query = "select * from product where product_name like '%{}%'".format(name)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)



#counting all product
@router.get("/count_products")
async def count_all_count(currentUser: model.productList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(product_id) as NumberOfproducts FROM product"
    res= await database.fetch_all(query=query, values={})
    return res
 
 
#Find one product by ID
@router.get("/product/{product_id}", response_model=model.productList)
async def find_product_by_id(product_id: str, currentUser: model.productList = Depends(util.get_current_active_user)):
    query = product.select().where(product.c.product_id == product_id)
    return await database.fetch_one(query)





#Find one product by users
@router.get("/product_user{userId}", response_model=model.productList)
async def find_product_by_user(userId: str, currentUser: model.productList = Depends(util.get_current_active_user)):
    query = product.select().where(product.c.user_id == userId)
    return await database.fetch_one(query)


# Find product by status
@router.get("/product_by_status/{status}", response_model=Page[model.productList])
async def find_product_by_status(status: str, currentUser: model.productList = Depends(util.get_current_active_user)):
    query = product.select().where(product.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)




# add new product
@router.post("/addstore")
async def register_store(pdcts: model.productCreate):

    usid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
    
    #Adding product
    query = product.insert().values(

            product_id=usid,
    
            user_id=pdcts.user_id,
            category_id=pdcts.category_id,
            product_name=pdcts.product_name,
            product_price=pdcts.product_price,
            description=pdcts.description,
            unity_type=pdcts.unity_type,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

    await database.execute(query)

    return{
            "code":"Store: " + pdcts.product_name,
            "Message":pdcts.product_name+" product has been registered",
            "status": 1
        }


#Update product
@router.put("/product_update")
async def update_product(pdcts: model.productUpdate, currentUser: model.productList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = product.update().where(product.c.product_id == pdcts.product_id).values(
            
            product_id=gid,
    
            user_id=pdcts.user_id,
            category_id=pdcts.category_id,
            product_name=pdcts.product_name,
            product_price=pdcts.product_price,
            description=pdcts.description,
            unity_type=pdcts.unity_type,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
    )

    await database.execute(Query)
    return ({
       "Msg:":pdcts.product_name+" has been Updated.Thank you for using this software"
    })


#Delete product
@router.delete("/Delete_product/{product_id}")
async def Delete_by_product_id(product_id: str, currentUser: model.productList = Depends(util.get_current_active_user)):
    query = product.delete().where(product.c.product_id == product_id)
    await database.execute(query)

    return ({
       "Msg:":"product has been deleted. Thank you for using this software"
    })