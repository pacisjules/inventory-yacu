import sqlalchemy
from sqlalchemy import ForeignKey
metadata = sqlalchemy.MetaData()
#Start and Configuration

#1 Table App Admins
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("username"  , sqlalchemy.String, unique=True),
    sqlalchemy.Column("password"  , sqlalchemy.String),
    
    sqlalchemy.Column("first_name"  , sqlalchemy.String),
    sqlalchemy.Column("last_name"  , sqlalchemy.String),


    sqlalchemy.Column("email"     , sqlalchemy.String, unique=True),
    sqlalchemy.Column("type"     , sqlalchemy.String),
    sqlalchemy.Column("role"     , sqlalchemy.String),

    sqlalchemy.Column("company"     , sqlalchemy.String),
    sqlalchemy.Column("organization_ID", sqlalchemy.String),
    sqlalchemy.Column("phone"     , sqlalchemy.String, unique=True),
    sqlalchemy.Column("living"     , sqlalchemy.String),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)

#2 Table Customers
customer  = sqlalchemy.Table(
    "customer",
    metadata,
    sqlalchemy.Column("cust_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("names"  , sqlalchemy.String),
    sqlalchemy.Column("tin"  , sqlalchemy.String),

    sqlalchemy.Column("bio"    , sqlalchemy.String),
    sqlalchemy.Column("email"  , sqlalchemy.String),
    sqlalchemy.Column("phone"  , sqlalchemy.String),
    sqlalchemy.Column("province"    , sqlalchemy.String),
    sqlalchemy.Column("district"    , sqlalchemy.String),
    sqlalchemy.Column("address"    , sqlalchemy.String),
    sqlalchemy.Column("identity_number"  , sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("qr_name"  , sqlalchemy.String),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#3 Table account recovery Keys
account_keys  = sqlalchemy.Table(
    "account_keys",
    metadata,
    sqlalchemy.Column("id"        , sqlalchemy.String , primary_key=True),
     sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),

    sqlalchemy.Column("key"  , sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
)



#4 Table currency
currency = sqlalchemy.Table(
    "currency",
    metadata,
    sqlalchemy.Column("currency_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),

    sqlalchemy.Column("currency_country"  , sqlalchemy.String),
    sqlalchemy.Column("currency_code"  , sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)

#5 Table companySetting
companysetting = sqlalchemy.Table(
    "companysetting",
    metadata,
    sqlalchemy.Column("org_setting_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("currency_id", sqlalchemy.String, ForeignKey(currency.c.currency_id), nullable=False),
    sqlalchemy.Column("organization_name"  , sqlalchemy.String),
    sqlalchemy.Column("organization_tel"  , sqlalchemy.String),
    sqlalchemy.Column("organization_tel2"  , sqlalchemy.String),
    sqlalchemy.Column("organization_fax"  , sqlalchemy.String),
    sqlalchemy.Column("organization_email"  , sqlalchemy.String),
    sqlalchemy.Column("organization_address"  , sqlalchemy.String),
    sqlalchemy.Column("organization_address2"  , sqlalchemy.String),
    sqlalchemy.Column("organization_street"  , sqlalchemy.String),
    sqlalchemy.Column("organization_city"  , sqlalchemy.String),
    sqlalchemy.Column("organization_state"  , sqlalchemy.String),
    sqlalchemy.Column("zip_code"  , sqlalchemy.String),
    sqlalchemy.Column("organization_website"  , sqlalchemy.String),
    sqlalchemy.Column("organization_description"  , sqlalchemy.String),
    sqlalchemy.Column("country_id"  , sqlalchemy.Integer),
    sqlalchemy.Column("organization_reg_number"  , sqlalchemy.String),
    sqlalchemy.Column("organization_affiliation_num"  , sqlalchemy.String),
    sqlalchemy.Column("organization_logo"  , sqlalchemy.String),
    sqlalchemy.Column("organization_head"  , sqlalchemy.String),
    sqlalchemy.Column("organization_footer_note"  , sqlalchemy.String),
    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#6 Table store
stores = sqlalchemy.Table(
    "stores",
    metadata,
    sqlalchemy.Column("store_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("org_setting_id"  , sqlalchemy.String, ForeignKey(companysetting.c.org_setting_id)),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),

    sqlalchemy.Column("store_name"  , sqlalchemy.String),
    sqlalchemy.Column("address"  , sqlalchemy.String),
    sqlalchemy.Column("description"     , sqlalchemy.String),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)



#7 Table category
category = sqlalchemy.Table(
    "category",
    metadata,
    sqlalchemy.Column("category_id", sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("store_id", sqlalchemy.String , ForeignKey(stores.c.store_id), nullable=False),
    
    sqlalchemy.Column("category_name"  , sqlalchemy.String),
    sqlalchemy.Column("description"  , sqlalchemy.String),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#8 Table product
product = sqlalchemy.Table(
    "product",
    metadata,
    sqlalchemy.Column("product_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("store_id"        , sqlalchemy.String , ForeignKey(stores.c.store_id), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("category_id", sqlalchemy.String, ForeignKey(category.c.category_id), nullable=False),

    sqlalchemy.Column("product_name"  , sqlalchemy.String),
    sqlalchemy.Column("product_price"  , sqlalchemy.Float),

    sqlalchemy.Column("description"     , sqlalchemy.String),
    sqlalchemy.Column("unity_type"  , sqlalchemy.String),
    sqlalchemy.Column("barcode"  , sqlalchemy.Integer),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#9 Table item
item = sqlalchemy.Table(
    "item",
    metadata,
    sqlalchemy.Column("item_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("product_id"        , sqlalchemy.String , ForeignKey(product.c.product_id), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    
    sqlalchemy.Column("quantity"  , sqlalchemy.Integer),
    sqlalchemy.Column("product_price"  , sqlalchemy.Float),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#10 Table orders
orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("order_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("item_id", sqlalchemy.String, ForeignKey(item.c.item_id), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("cust_id", sqlalchemy.String, ForeignKey(customer.c.cust_id), nullable=False),
    
    sqlalchemy.Column("quantity"  , sqlalchemy.Integer),
    sqlalchemy.Column("total_price"  , sqlalchemy.Float),
    sqlalchemy.Column("order_date", sqlalchemy.String),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)

#11 Table userSection
usersection = sqlalchemy.Table(
    "usersection",
    metadata,
    sqlalchemy.Column("section_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("section_name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)

#12 Table UserGroup table
usergroup = sqlalchemy.Table(
    "usergroup",
    metadata,
    sqlalchemy.Column("group_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("group_name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#13 Table UserDetail table
userdetail = sqlalchemy.Table(
    "userdetail",
    metadata,
    sqlalchemy.Column("detail_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("group_id", sqlalchemy.String, ForeignKey(usergroup.c.group_id), nullable=False),
    sqlalchemy.Column("section_id", sqlalchemy.String, ForeignKey(usersection.c.section_id), nullable=False),
    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)

#currency


#14 Table Theme setting
themesetting = sqlalchemy.Table(
    "themesetting",
    metadata,
    sqlalchemy.Column("theme_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("theme_name"    , sqlalchemy.String),
    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#15 Table distributor
distributor = sqlalchemy.Table(
    "distributor",
    metadata,
    sqlalchemy.Column("distributor_id"        , sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    
    sqlalchemy.Column("names"  , sqlalchemy.String),
    sqlalchemy.Column("email"  , sqlalchemy.String),
    sqlalchemy.Column("phone"  , sqlalchemy.String),
    sqlalchemy.Column("address"  , sqlalchemy.String),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#16 Distributor order
distr_order = sqlalchemy.Table(
    "distr_order",
    metadata,
    sqlalchemy.Column("distr_order_id", sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("distributor_id", sqlalchemy.String, ForeignKey(distributor.c.distributor_id), nullable=False),
    sqlalchemy.Column("product_id", sqlalchemy.String , ForeignKey(product.c.product_id), nullable=False),
    
    sqlalchemy.Column("quantity"  , sqlalchemy.Integer),
    sqlalchemy.Column("unit_price"  , sqlalchemy.Float),
    sqlalchemy.Column("total"  , sqlalchemy.Float),

    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)


#17 Distributor payments
distr_payment = sqlalchemy.Table(
    "distr_payment",
    metadata,
    sqlalchemy.Column("distr_payment_id", sqlalchemy.String , primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey(users.c.user_id), nullable=False),
    sqlalchemy.Column("distributor_id", sqlalchemy.String, ForeignKey(distributor.c.distributor_id), nullable=False),
    sqlalchemy.Column("product_id", sqlalchemy.String , ForeignKey(product.c.product_id), nullable=False),
    
    sqlalchemy.Column("payed_status"  , sqlalchemy.String),
    sqlalchemy.Column("payed_amount"  , sqlalchemy.Float),
    
    sqlalchemy.Column("status"    , sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("last_update_at", sqlalchemy.String),
)















