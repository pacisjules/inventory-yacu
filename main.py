from configs.connection import database
from fastapi import FastAPI, Depends, Request
from functools import lru_cache
from configs import appinfo
import time
from fastapi_pagination import add_pagination
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

now = datetime.now()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/image", tags=["image Reader"])
async def main_Image():
    return FileResponse("auth/qrkey/qr1.png")


@app.get("/", tags=["Root"])
async def root():
    return{
        "message": "This Apis are for  Inventory & Sales Management System",
        "Software Engineer": "ISHIMWE JULES Pacis, NTWARI Esdras",
        "Email": "ishimwejulespacis@gmail.com and ntwariezraa@gmail.com",
        "GitHub": "https://github.com/pacisjules and https://github.com/ezran2022",
        "owner_name":"NTWARI Esdras & ISHIMWE Jules Pacis",
    }


@app.get("/app/info", tags=["App"])
async def app_info():
    return {
        "app_name"      : "Inventory Platform",
        "app_version"   : "1.0",
        "app_framework" : "FastAPI (Python)",
        "status" : "Building process...",
        "app_date_now"  : now.strftime("%Y-%m-%d %H:%M:%S"),
        "owner_name"    :"NTWARI Esdras & ISHIMWE Jules Pacis",
    }


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)

    return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


from auth import controller as authController
from users import controller as userController
from customer import controller as customerController
from currency import controller as currencyController

from companysetting import controller as companySettingsController
from stores import controller as storesController
from themesettingss import controller as themeController

from usersections import controller as sectionController
from usergroups import controller as groupController
from userdetails import controller as user_detailController
from category import controller as categoryController
from products import controller as productsController
from item import controller as itemsController
from orders import controller as ordersController
from distributor import controller as distributorController
from distributor_order import controller as distributorOrderController
from distributor_payment import controller as distributorPaymentController



#Config Parts
app.include_router(authController.router, tags=["Auth"])
app.include_router(userController.router, tags=["Users"])


#Application Parts
app.include_router(customerController.router, tags=["Customers"])
app.include_router(currencyController.router, tags=["Currency"])

app.include_router(companySettingsController.router, tags=["Company Setting"])
app.include_router(storesController.router, tags=["Stores"])


app.include_router(sectionController.router, tags=["Sections"])
app.include_router(groupController.router, tags=["Groups"])
app.include_router(themeController.router, tags=["ThemeSettings"])

app.include_router(user_detailController.router, tags=["User Details"])
app.include_router(categoryController.router, tags=["Product Category"])

app.include_router(productsController.router, tags=["Products"])
app.include_router(itemsController.router, tags=["Items"])
app.include_router(ordersController.router, tags=["Orders"])


app.include_router(distributorController.router, tags=["Distributor"])
app.include_router(distributorOrderController.router, tags=["Distributor Order"])
app.include_router(distributorPaymentController.router, tags=["Distributor Payment"])

add_pagination(app)