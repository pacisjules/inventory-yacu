from fastapi import APIRouter, HTTPException, Depends
from db.table import service, vehicle, vehicle_type, customer
from Service import model, randomId, randomId2
from utils import util
from configs.connection import database
import uuid, datetime
import  qrcode

from fastapi_pagination import Page, paginate
router = APIRouter()

# find car by Plate
@router.get("/run_service_plate/{plate}")
async def find_run_service_plate(plate:str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):

    formatNumber=plate.upper()
    query = "SELECT CU.id AS customer_id, CU.names,V.car_plate, V.car_color, V.id AS car_id,VE.id AS type_id, VE.car_brand FROM vehicle V, customer CU, vehicle_type VE WHERE  V.car_plate='{}' AND V.vehicle_type_id=VE.id AND V.customer_id=CU.id".format(formatNumber)
    res= await database.fetch_all(query=query, values={})

    if res:
        return {
            "customer_id": res[0]["customer_id"],
            "names": res[0]["names"],
            "car_plate": res[0]["car_plate"],
            "car_color": res[0]["car_color"],
            "car_id": res[0]["car_id"],
            "type_id": res[0]["type_id"],
            "car_brand": res[0]["car_brand"]
        }
    else:
        return {
            "message": "No vehicle found"
        }

# find count received service
@router.get("/count_received_service")
async def count_received_service( currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    
    fullDate = datetime.datetime.now()
    gdate = fullDate.strftime("%Y-%m-%d")
    
    query = "SELECT COUNT(*) AS number_of_serv  FROM service WHERE process_level='start' AND status='1' "
    res= await database.fetch_all(query=query, values={})
    return {
        "number_of_serv_request": res[0]["number_of_serv"]
    }

# find count Done service
@router.get("/count_done_service")
async def count_done_service( currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    
    fullDate = datetime.datetime.now()
    gdate = fullDate.strftime("%Y-%m-%d")
    
    query = "SELECT COUNT(*) AS number_of_serv  FROM service WHERE process_level='done' AND status='2' AND created_at='{}'".format(gdate)
    res= await database.fetch_all(query=query, values={})
    return {
        "number_of_serv_done": res[0]["number_of_serv"]
    }

# find count service in processing
@router.get("/count_inprocess_service")
async def count_inprocess_service( currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    
    fullDate = datetime.datetime.now()
    gdate = fullDate.strftime("%Y-%m-%d")

    query = "SELECT COUNT(*) AS number_of_serv  FROM service WHERE process_level='inprogress' AND status='1'"
    res= await database.fetch_all(query=query, values={})
    return {
        "number_of_serv_inprocess": res[0]["number_of_serv"]
    }

# find count service in canceled today
@router.get("/count_canceled_service_today")
async def count_canceled_service_today( currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    
    fullDate = datetime.datetime.now()
    gdate = fullDate.strftime("%Y-%m-%d")
    
    query = "SELECT COUNT(*) AS number_of_serv  FROM service WHERE process_level='processing' AND status='0' AND created_at={}".format(gdate)
    res= await database.fetch_all(query=query, values={})
    return {
        "number_of_serv_cancelled_today": res[0]["number_of_serv"]
    }

# find count service in canceled month
@router.get("/count_canceled_service_month")
async def count_canceled_service_month( currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    
    fullDate = datetime.datetime.now()
    monthnow =int(fullDate.strftime("%m"))
    yearnow=int(fullDate.strftime("%Y"))
    query = "SELECT COUNT(*) AS number_of_serv  FROM service WHERE process_level='processing' AND status='0' AND month={} AND year={}".format(monthnow, yearnow)
    res= await database.fetch_all(query=query, values={})
    return {
        "number_of_serv_cancelled_today": res[0]["number_of_serv"]
    }

# find count income today
@router.get("/count_income_today")
async def count_income_today( currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    
    fullDate = datetime.datetime.now()
    gdate = fullDate.strftime("%Y-%m-%d")
    query = "SELECT SUM(price) AS cash_today FROM service where created_at='{}' AND status='2' AND process_level='payed'".format(gdate)
    res= await database.fetch_all(query=query, values={})
    if res[0]["cash_today"] is None:
        return {
            "cash_today": 0
        }
    else:
        return {
            "cash_today": res[0]["cash_today"]
        }

# find count income month
@router.get("/count_income_month")
async def count_income_month( currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    
    fullDate = datetime.datetime.now()
    monthnow =int(fullDate.strftime("%m"))
    yearnow=int(fullDate.strftime("%Y"))
    
    query = "SELECT SUM(price) AS cash_month FROM service where month={} AND year={} AND status='2' AND process_level='payed'".format(monthnow, yearnow)
    res= await database.fetch_all(query=query, values={})

    if res[0]["cash_month"] is None:
        return {
            "cash_this_Month": 0
        }
    else:
        return {
            "cash_this_Month": res[0]["cash_month"]
        }

# All services
@router.get("/all_services")
async def find_allVehicle_Type(currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = "SELECT SE.id, SE.service_identity,SE.created_at,SE.status, SE.process_level,SE.price,WA.title, WA.description, VE.car_plate,CU.names, concat(CU.province,', ', CU.district) AS loc, VT.car_brand  FROM service SE, vehicle VE, customer CU, vehicle_type VT, wash_type WA WHERE CU.id=SE.customer_id AND VE.id=SE.vehicle_id AND WA.id=SE.wash_type_id AND VE.vehicle_type_id=VT.id"
    res = await database.fetch_all(query)
    count=len(res)
    return {
        "results": res,
        "count": count,
        "page:": 1
    }

# All services canceled
@router.get("/all_services_canceled")
async def all_services_canceled(currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = "SELECT * FROM service where process_level='canceled' AND status='0'"
    res = await database.fetch_all(query)
    return res


# Find Service with vehicle id
@router.get("/service_vehicle_id/{id}", response_model=model.Vehicle_Service_List)
async def find_service_vehicle_id(id: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.select().where(service.c.vehicle_id == id)
    return await database.fetch_one(query)

#Find one Service by ID
@router.get("/Service_by_id/{id}", response_model=model.Vehicle_Service_List)
async def find_service_by_id(id: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.select().where(service.c.id == id)
    return await database.fetch_one(query)


#Find one Service by Service Unique Num
@router.get("/Service_by_service_number/{number}", response_model=model.Vehicle_Service_List)
async def find_service_by_service_number(number: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.select().where(service.c.service_identity == number)
    return await database.fetch_one(query)

#counting all services
@router.get("/count_service")
async def find_all_count(currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    
    query = "SELECT COUNT(id) FROM service"
    res= await database.fetch_all(query=query, values={})
    return res


#Find one Service by Customer ID
@router.get("/Service_by_customer_id/{id}", response_model=model.Vehicle_Service_List)
async def find_service_by_customer_id(id: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.select().where(service.c.customer_id == id)
    return await database.fetch_one(query)

#Find one Service by User ID
@router.get("/Service_by_user_id/{id}", response_model=model.Vehicle_Service_List)
async def find_service_by_user_id(id: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.select().where(service.c.user_id == id)
    return await database.fetch_one(query)


#Find one Service by process
@router.get("/Service_by_process/{prcs}", response_model=model.Vehicle_Service_List)
async def find_service_by_process(prcs: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.select().where(service.c.process_level == prcs)
    return await database.fetch_one(query)


#Find one Service by wash type ID
@router.get("/Service_by_wash_type_id/{id}", response_model=model.Vehicle_Service_List)
async def find_service_by_wash_type_id(id: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.select().where(service.c.wash_type_id == id)
    return await database.fetch_one(query)


# Find service by status
@router.get("/service_by_status/{status}", response_model=Page[model.Vehicle_Service_List])
async def find_Vehicle_Type_by_status(status: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.select().where(service.c.status == status)
    res = await database.fetch_all(query)
    return paginate(res)



# add new Service
@router.post("/addVehicle_service")
async def registerVehicle_service(vsr: model.Vehicle_Service_Create):

    code=randomId.id_all_random
    gid = str(uuid.uuid1())
    fullDate = datetime.datetime.now()
    gdate = fullDate.strftime("%Y-%m-%d")
    
    seeqry=service.select().where(service.c.service_identity == code)
    res = await database.fetch_all(seeqry)

    if res:
        code=randomId2.id_all_random2
        seevehqry=service.select().where(service.c.vehicle_id == vsr.vehicle_id and service.c.status == "start")
        vehres = await database.fetch_all(seevehqry)
        
        if vehres:
            return {
                "message": "Vehicle is already in service",
                "code":"0"
            }
        else:
            link="http://localhost:3000/reset_password/"+code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(link)

            qr.make(fit=True)  
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("Service/qrservice/"+code+".png")

            monthnow =int(fullDate.strftime("%m"))
            yearnow=int(fullDate.strftime("%Y"))



            query = service.insert().values(
                
                id = gid,
                user_id=vsr.user_id,
                customer_id=vsr.customer_id,
                vehicle_id= vsr.vehicle_id,
                wash_type_id= vsr.wash_type_id,


                comment=vsr.comment,
                price=vsr.price,
                service_identity=code,
                qr_name=code,
                process_level="start",

                created_at = gdate,
                last_update_at=gdate,
                status = "1",

                month=monthnow,
                year=yearnow,
            )

            await database.execute(query)
            
            return {
                "message": "Successfully created a new Service",
                "qr_name": code,
                "date": gdate,
                "code":"1"
            }
    else:
        seevehqry=service.select().where(service.c.vehicle_id == vsr.vehicle_id and service.c.status == "start") 
        vehres = await database.fetch_all(seevehqry)
        
        if vehres:
            return {
                "message": "Vehicle is already in service",
                "code":"0"
            }
        else:
            
            code=randomId.id_all_random
            link="http://localhost:3000/reset_password/"+code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(link)

            qr.make(fit=True)  
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("Service/qrservice/"+code+".png")

            monthnow =int(fullDate.strftime("%m"))
            yearnow=int(fullDate.strftime("%Y"))



            query = service.insert().values(
                
                id = gid,
                user_id=vsr.user_id,
                customer_id=vsr.customer_id,
                vehicle_id= vsr.vehicle_id,
                wash_type_id= vsr.wash_type_id,


                comment=vsr.comment,
                price=vsr.price,
                service_identity=code,
                qr_name=code,
                process_level="start",

                created_at = gdate,
                last_update_at=gdate,
                status = "1",

                month=monthnow,
                year=yearnow,
            )

            await database.execute(query)
            
            return {
                "message": "Successfully created a new Service",
                "qr_name": code,
                "date": gdate,
                "code":"1"
            }

        

#Update Vehicle_Type
@router.put("/Vehicle_service_update", response_model=model.Vehicle_Service_List)
async def update_Vehicle_service(vsr: model.Vehicle_Service_Update, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = service.update().where(service.c.id == vsr.id).values(
        id = gid,

        user_id=vsr.user_id,
        customer_id=vsr.customer_id,
        vehicle_id= vsr.vehicle_id,
        wash_type_id= vsr.wash_type_id,


        comment=vsr.comment,
        price=vsr.price,
        process_level=vsr.process_level,
        

        created_at = gdate,
        last_update_at=gdate,
        status = "1"
    )

    await database.execute(Query)
    return await find_service_by_id(vsr.id)


#Delete Service
@router.delete("/Delete_services/{id}", response_model=model.Vehicle_Service_List)
async def Delete_by_Vehicle_Type_id(id: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.delete().where(service.c.id == id)
    return await database.execute(query)





#View Query of Customer, vehicle and type
@router.get("/get_vehicle/{plate}")
async def get_vehicle_withAll_Info(plate: str):
    plate_query=vehicle.select().where(vehicle.c.car_plate == plate)
    plate_check= await database.fetch_one(plate_query)

    if not plate_check:
        return {
            "Addition":"Plate not Found in our System",
            "action":0
        }
    else:
        customer_id = plate_check['customer_id']
        vehicle_type_id = plate_check['vehicle_type_id']
        occupation=plate_check['occupation']
        car_plate=plate_check['car_plate']
        car_color=plate_check['car_color']
        car_year=plate_check['car_year']

    cust_query=customer.select().where(customer.c.id == customer_id)
    cust_check= await database.fetch_one(cust_query)
    
    customer_names = cust_check['names']
    customer_tin = cust_check['tin']
    customer_phone = cust_check['phone']
    customer_district = cust_check['district']
    customer_province = cust_check['province']

    veh_type_query=vehicle_type.select().where(vehicle_type.c.id == vehicle_type_id)
    veh_type_check= await database.fetch_one(veh_type_query)


    veh_type_names = veh_type_check['car_brand']
    veh_type_status = veh_type_check['status']

    return {

        "plate_number":car_plate,
        "occupation":occupation,
        "year":car_year,
        "color":car_color,
        
        "customer":{
        "customer_id":customer_id,
        "customer_names":customer_names,
        "customer_TIN":customer_tin,
        "customer_phone":customer_phone,
        "customer_district":customer_district,
        "customer_province":customer_province,
        },
        "type":{
        "type_id":vehicle_type_id,
        "car_brand":veh_type_names,
        "status":veh_type_status,
        }
    }


# Updating status of services
@router.put("/update_service_status/{service_id}/{status}")
async def update_service_status(service_id: str, status: str, currentUser: model.Vehicle_Service_List = Depends(util.get_current_active_user)):
    query = service.update().where(service.c.id == service_id).values(
        process_level = status
    )
    res = await database.execute(query)
    return {
        "action":res,
        "message": "Successfully updated the service status",
    }