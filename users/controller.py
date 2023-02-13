from fastapi import APIRouter, Depends
from auth import model, randompassword
from utils import util

from db.table import users, account_keys
from configs.connection import database
from fastapi_pagination import Page, paginate
import uuid, datetime
import  qrcode

router = APIRouter()

#Current User
@router.get("/users/me", response_model=model.UserList)
async def read_user_me(currentUser: model.UserList = Depends(util.get_current_active_user)):
    return currentUser

#find all users
@router.get("/users", response_model=Page[model.UserList])
async def find_all_user(
    currentUser: model.UserList = Depends(util.get_current_active_user)
):
    query = "select * from users"
    res= await database.fetch_all(query=query, values={})
    return paginate(res)


#Find one User by ID
@router.get("/users/{User_id}", response_model=model.UserList)
async def find_user_by_id(User_id: str, currentUser: model.UserList = Depends(util.get_current_active_user)):
    query = users.select().where(users.c.user_id == User_id)
    return await database.fetch_one(query)


#Update User
@router.put("/auth/update", response_model=model.UserListforUpdate)
async def update_user(user: model.UserUpdate, currentUser: model.UserList = Depends(util.get_current_active_user)):

    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())

    Query = users.update().where(users.c.user_id == user.user_id).values(
        # user_id = gid,
        #username = user.username,
        #password = util.get_password_hash(user.password),

        #first_name= user.first_name,
        #last_name=user.last_name,

        #email = user.email,
        # type = user.type,
        # role = user.role,
        #company= user.company,
        organization_ID=user.organization_ID,
        # phone= user.phone,    
        # living= user.living,

        #last_update_at = gdate,
        #status = "1"
    )

    await database.execute(Query)
    return await find_user_by_id(user.user_id)



#Delete User
@router.delete("/users/{User_id}", response_model=model.UserList)
async def Delete_by_id(User_id: str, currentUser: model.UserList = Depends(util.get_current_active_user)):
    query = users.delete().where(users.c.id == User_id)
    return await database.execute(query)


#Password Recover

@router.get("/Password_recover/{email}")
async def password_recover_password(email: str):
    gid = str(uuid.uuid1())
    query=users.select().where(users.c.email == email)
    email_checker= await database.fetch_one(query)
    gdate = str(datetime.datetime.now())

    if not email_checker:
        return {
            "Addition":"Email not Found in our System",
            "action":0
        }
    else:
        user_found_id =email_checker['id']
        user_found_email =email_checker['email']
        user_found_status =email_checker['status']
        user_found_username =email_checker['username']
        user_info_status=""
        if user_found_status == "1":
            user_info_status="User is active"
        else:
            user_info_status="User is not active"
    
    message_help="Dear "+user_found_username+" check your email box ("+user_found_email+") we have been sent you new password you can change later"
    new_user_password=randompassword.all_random
    key_run=randompassword.random_key
    
    #Qr Creation for Key
        
    content=key_run
    link="http://localhost:3000/reset_password/"+content
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)  
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("auth/qrkey/"+content+".png")
    
#Update,Key and Send Message

    #Update password
    Query_update = users.update().where(users.c.id == user_found_id).values(
    password = util.get_password_hash(new_user_password),
    last_update_at = gdate,
    status = "1"
    )
    await database.execute(Query_update)

        #Give system key
    Query_key=account_keys.insert().values(
        id=gid,
         user_id=user_found_id,
        key=key_run,
        status="1",
        created_at=gdate,
    )
    await database.execute(Query_key)
       

    from auth import emailsender
        
        #Email
    receiver=user_found_email
    password=new_user_password
    username=user_found_username

    emailsender.send_mail(receiver,username,key_run, password,)
        
    #Messages
    return {
            "user Id":user_found_id,
            "username":user_found_username,
            "new password":new_user_password,
            "user Email":user_found_email,
            "user Status":user_info_status,
            "Message":message_help,
            "Key":key_run,
            "action":1
        }

#Password Update Link Finisher
@router.put("/Account_passwordUpdate/{Key}")
async def update_user_password(key:str, kys:model.UserPasswordUpdate):
    gdate = str(datetime.datetime.now())
    query=account_keys.select().where(account_keys.c.key == key)
    key_checker= await database.fetch_one(query)

    if not key_checker:
        return{
            "Message": "Key is not Valid",
            "action": 0,
        }
    elif key_checker['status']=="0":
        return{
            "Message": "Key is Expired",
            "action": 0,
        }
    
    else:
        
        Mykey=key_checker['key']
        MykeyDate= key_checker['created_at']
        User_id=key_checker['user_id']

        #Update Key
        Key_update = account_keys.update().where(account_keys.c.key == Mykey).values(
        status = "0"
        )
        await database.execute(Key_update)
        
        #Update password
        Update_password = users.update().where(users.c.id == User_id).values(
        password = util.get_password_hash(kys.password),
        last_update_at = gdate,
        status = "1"
        )
        await database.execute(Update_password)

        return{
            "My_key":Mykey,
            "My_key_Status":"Key now Done",
            "My_key_Date":MykeyDate,
            "User_id":User_id,
            "action": 1,
        }





#Account Confirmation
@router.put("/NewAccount/account_confirmation", response_model=model.UserListforUpdate)
async def update_user(user: model.UserUpdate):

    #gid = str(uuid.uuid1())

    gdate = str(datetime.datetime.now())

    Query = users.update().where(users.c.id == user.id).values(
        last_update_at = gdate,
        status = "1"
    )

    await database.execute(Query)
    return await find_user_by_id(user.id)