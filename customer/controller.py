from fastapi import APIRouter, HTTPException, Depends
from db.table import customer
from customer import model, randomId, emailsender
from utils import util
from configs.connection import database
import uuid, datetime
from fastapi.responses import FileResponse
import random
import  qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()


# All Customers
@router.get("/all_customers", response_model=Page[model.CustomerList])
async def find_allCustomer(currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.select().order_by(customer.c.cust_id.desc())
    res = await database.fetch_all(query)
    return paginate(res)


# Find Customers with names
@router.get("/like_Customer/{names}", response_model=Page[model.CustomerList])
async def find_like_customer(names: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):

    query = "select * from Customer where names like '%{}%'".format(names)
    res= await database.fetch_all(query=query, values={})
    return paginate(res)



#counting all customers
@router.get("/count_customers")
async def count_all_count(currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = "SELECT COUNT(cust_id) as NumberOfCustomers FROM customer"
    res= await database.fetch_all(query=query, values={})
    return res


#Find one Customer by ID
@router.get("/Customer/{Customer_id}", response_model=model.CustomerList)
async def find_Customer_by_id(Customer_id: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.select().where(customer.c.cust_id == Customer_id)
    return await database.fetch_one(query)


#Find one Customer by identity number
@router.get("/Customer/{identity}", response_model=model.CustomerList)
async def find_Customer_by_identity(identity: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.select().where(customer.c.identity_number == identity)
    return await database.fetch_one(query)


#Find one Customer by TIN NUMBER
@router.get("/Customer/tin/{tin_number}", response_model=model.CustomerList)
async def find_Customer_by_tin_number(tin_number: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.select().where(customer.c.tin == tin_number)
    return await database.fetch_one(query)



# Find Customers by province
@router.get("/all_Customers_by_province/{province}", response_model=Page[model.CustomerList])
async def find_Customers_by_province(province: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.select().where(customer.c.province == province)
    res = await database.fetch_all(query)
    return paginate(res)


# Find Customers by district
@router.get("/all_Customers_by_district/{district}", response_model=Page[model.CustomerList])
async def find_Customers_by_district(district: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.select().where(customer.c.district == district)
    res = await database.fetch_all(query)
    return paginate(res)


# Find Customers by phone
@router.get("/find_Customer_by_phone/{phone}", response_model=Page[model.CustomerList])
async def find_Customers_by_phone(phone: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.select().where(customer.c.phone == phone)
    res = await database.fetch_all(query)
    return paginate(res)


# Find Customers by status
@router.get("/Customer_by_status/{status}", response_model=Page[model.CustomerList])
async def find_Customer_by_status(status: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.select().where(customer.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)

# add new Customer
@router.post("/addCustomer")
async def register_Customer(customers: model.CustomerCreate):
    
    # check if customer already exists
    Cquery = customer.select().where(customer.c.tin == customers.tin)
    Cres = await database.fetch_one(Cquery)
    if Cres:
        return{
            "message": "Customer "+customers.names+" already exists",
            "status": 0
        }
    else:

        # Generate Codes
        rdm = random.randint(1, 34)
        rdm2=  random.randint(5, 14)
        code=randomId.id_all_random+ str(rdm) + str(rdm2)
        link="http://localhost:3000/reset_password/"+code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(link)
        qr.make(fit=True)  
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("customer/qrid/"+code+".png")


        gid = str(uuid.uuid1())
        gdate = str(datetime.datetime.now())

        
        #Adding Customer
        query = customer.insert().values(
            
            cust_id = gid,
            
            user_id=customers.user_id,
            names=customers.names, 
            tin=customers.tin,
            bio= customers.bio,
            email= customers.email,
            phone= customers.phone,
            identity_number=code, 
            
            province= customers.province,
            district= customers.district,
            address= customers.address,
            qr_name=code,

            created_at = gdate,
            last_update_at=gdate,
            status = "1"
        )

        await database.execute(query)

        #Email
        receiver=customers.email
        company=customers.names
        phone=customers.phone
        identity=code
    
        senderNow = emailsender.send_mail(receiver, company, phone, identity)
        print(senderNow)




        return{
            "code":"CODE" + code,
            "Message":customers.names+" has been registered",
            "Email":"Email sent",
            "status": 1
        }




#Update Customer
@router.put("/Customer_update", response_model=model.CustomerList)
async def update_Customer(cstm: model.CustomerUpdate, currentUser: model.CustomerList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = customer.update().where(customer.c.cust_id == cstm.cust_id).values(
       
        cust_id = gid,

        user_id=cstm.user_id,
        names=cstm.names, 
        tin=cstm.tin,
        bio= cstm.bio,
        email= cstm.email,
        phone= cstm.phone,

        province= cstm.province,
        district= cstm.district,
        address= cstm.address,

        created_at = gdate,
        last_update_at=gdate,
        status = "1"
    )

    await database.execute(Query)
    return await find_Customer_by_id(cstm.cust_id)


#Delete Customer
@router.delete("/Delete_Customer/{Customer_id}")
async def Delete_by_Customer_id(Customer_id: str, currentUser: model.CustomerList = Depends(util.get_current_active_user)):
    query = customer.delete().where(customer.c.cust_id == Customer_id)
    await database.execute(query)

    return ({
       "Msg:":"Customer has been deleted. Thank you for using this software"
    })