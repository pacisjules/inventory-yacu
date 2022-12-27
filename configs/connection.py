import databases
import sqlalchemy
from functools import lru_cache
from configs import dbinfo
from db.table import metadata

@lru_cache()
def db_config():
    return dbinfo.Setting()

def DATABASE_URL(
    connection: str = "postgresql",
    username: str   = "postgres",
    password: str   ="123",
    host: str       = "127.0.0.1",
    port: str       = "5432", #5432 always for postgress
    database: str   = "inventory"
):return str(connection+"://"+username+":"+password+"@"+host+":"+port+"/"+database)

database = databases.Database(DATABASE_URL())

engine = sqlalchemy.create_engine(
    DATABASE_URL()
)

metadata.create_all(engine)