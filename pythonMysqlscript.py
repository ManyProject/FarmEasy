import mysql.connector
import random
from random import randrange
import datetime
import time
import bcrypt
from db_connection import connect

mydb = connect()

names = ['Yash', 'Harshit', 'Aman', 'Amar', 'Shadab']
role = ['Farmer', 'Buyer', 'Delivery Agent']
address = ['Mumbai', 'Delhi', 'Pune', 'Bangalore', 'Kolkata']
produce_name = ['Tomato', 'Apple', 'Chana Dal', 'Wheat', 'Cloves']
produce_price = [40, 70, 48, 40, 800]
produce_category = ['Vegetables', 'Fruits', 'Pulses', 'Grains', 'Spices']
produce_description = (["big", "very big", "very very big", "smol", "v smol",
                       "v v smol"])
user_image = "https://nulm.gov.in/images/user.png"
passwd = b'abcde'
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)
agency_name = ['Indian Post', 'FedX', 'Shipping Corp.', 'iThink Logistics']
intercity_rates = [200, 314, 155, 266]
intracity_rates = [50, 35, 42, 37]
delivery_status = ['Delivered', 'Shipping', 'Pending']
method = ['Cash On Delivery', 'Credit/Debit Card', 'Net Banking']
produce_image = ["https://www.naturefresh.ca/wp-content/uploads/NFF-health-benefits-of-Tomatoes.jpg",
                 "https://www.dw.com/image/47429859_303.jpg","https://sastapasal.com/wp-content/uploads/2019/11/chana-dal.jpg",
                 "https://organicexpressmart.com/media/image/268/organic-khapali-wheat-whole-1-kg.jpg",
                 "https://cdn.britannica.com/s:700x500/27/171027-050-7F7889C9/flower-buds-clove-tree.jpg"]


def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y/%m/%d %H:%M', prop)


mycursor = mydb.cursor()
mycursor.execute("DELETE FROM orders")
mydb.commit()
print("deleted orders")
mycursor.execute("DELETE FROM cart_items")
mydb.commit()
print("deleted cart_items")
mycursor.execute("DELETE FROM address")
mydb.commit()
print("deleted address")
mycursor.execute("DELETE FROM buyer")
mydb.commit()
print("deleted buyer")
mycursor.execute("DELETE FROM produce")
mydb.commit()
print("deleted produce")
mycursor.execute("DELETE FROM farmer")
mydb.commit()
print("deleted farmer")
mycursor.execute("DELETE FROM delivery_agent")
mydb.commit()
print("deleted delivery_agent")
mycursor.execute("DELETE FROM delivery_agency")
mydb.commit()
print("deleted delivery_agency")
mycursor.execute("DELETE FROM user")
mydb.commit()
print("deleted user")

values = []
for i in range(0, 80):
    x = random.randint(0, len(names)-1)
    y = random.randint(0, len(role)-1)
    phone = random.randrange(9000000000, 9999999999)
    val = (names[x], names[x].lower()+str(i)+'@gmail.com', phone,address[x], hashed,user_image, role[y])
    values.append(val)

sql = "INSERT INTO user(user_id,user_name,user_email,user_phone,user_address,user_password,user_image,user_role) VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql, values)
mydb.commit()

sql = "SELECT user_id,user_role FROM user"
mycursor.execute(sql)
uid = mycursor.fetchall()

values = []
for i in range (0, len(agency_name)-1):
    val = (intracity_rates[i], intercity_rates[i],agency_name[i])
    values.append(val)

sql = "INSERT INTO delivery_agency(agency_id,intracity_rates,intercity_rates, agency_name) VALUES (UUID(), %s, %s, %s)"
mycursor.executemany(sql, values)
mydb.commit()

sql = "SELECT agency_id FROM delivery_agency"
mycursor.execute(sql)
aid = mycursor.fetchall()

for i in uid:

    if i[1] == 'Farmer':
        fid = i[0]
        sql = "INSERT INTO farmer(farmer_id) VALUES (%s)"
        val = fid
        params = (val,)
        mycursor.execute(sql, params)
        mydb.commit()

    if i[1] == 'Buyer':
        buid = i[0]
        sql = "INSERT INTO buyer(buyer_id) VALUES (%s)"
        val = buid
        params = (val,)
        mycursor.execute(sql, params)
        mydb.commit()


    if i[1] == 'Delivery Agent':
        daid = i[0]
        x = random.randint(0, len(aid)-1)
        sql = "INSERT INTO delivery_agent(delivery_agent_id,agency_id) VALUES (%s, %s)"
        val = daid
        val1 = str(aid[x][0])
        params = (val, val1,)
        mycursor.execute(sql, params)
        mydb.commit()

for i in uid:
    for j in range(random.randint(1, 3)):
        if i[1] == 'Buyer':
            sql = "INSERT INTO address VALUES (%s, UUID(), %s)"
            x = random.randint(0, len(address)-1)
            params = (i[0], address[x],)
            mycursor.execute(sql, params)
            mydb.commit()

sql = "SELECT farmer_id FROM farmer"
mycursor.execute(sql)
fid = mycursor.fetchall()

values = []
for i in fid:
    x = random.randint(0, len(produce_name)-1)
    y = random.randint(0, (len(fid)-1))
    produce_quantity = random.randint(1,1000)
    produce_date = (randomDate("2020/03/01 08:00", "2020/03/20 23:00", random.random()))
    val = (str(fid[y][0]),produce_name[x],round(random.uniform(produce_price[x]*0.8,produce_price[x]*1.2), 2),
    produce_quantity,produce_image[x],produce_category[x],produce_date,aid[random.randint(0, len(aid)-1)][0], produce_description[random.randint(0, len(produce_description)-1)],)
    values.append(val)

sql = "INSERT INTO produce(produce_id,farmer_id,produce_name,produce_price,produce_quantity,\
    produce_image,produce_category,produce_date,delivery_agency_id, produce_description) VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql, values)
mydb.commit()

sql = "SELECT produce_id, produce_name FROM produce"
mycursor.execute(sql)
pid = mycursor.fetchall()

sql = "SELECT buyer_id FROM buyer"
mycursor.execute(sql)
buid = mycursor.fetchall()

values = []
for i in buid:
    order_quantity = random.randint(1,5)
    order_price = random.randint(1000,9999)
    order_date = (randomDate("2020/03/22 08:00", "2020/03/26 23:00", random.random()))
    delivery_agency_id = aid[random.randint(0, len(aid)-1)][0]
    produce_id = pid[random.randint(0, len(aid)-1)][0]
    x = random.randint(0, len(delivery_status)-1)
    delivery_address = address[random.randint(0,len(names)-1)]
    delivery_stat = delivery_status[x]
    if delivery_stat == 'Delivered':
        pickup = (randomDate("2020/03/27 8:00", "2020/03/27 20:00", random.random()))
        drop = (randomDate("2020/03/28 8:00", "2020/03/28 20:00", random.random()))
    if delivery_stat == 'Shipping':
        pickup = (randomDate("2020/03/27 8:00", "2020/03/27 20:00", random.random()))
        drop = "NA"
    if delivery_stat == 'Pending':
        pickup = "NA"
        drop = "NA"
    val = (i[0],order_quantity,order_date,order_price,delivery_agency_id,delivery_stat, pickup, drop, method[x],delivery_address, produce_id,)
    values.append(val)

sql = "INSERT INTO orders(buyer_id,order_id,order_quantity,order_date,order_price,delivery_agency_id,\
    delivery_status,pickup_time, drop_time, payment_method, delivery_address, produce_id) VALUES (%s, UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql, values)
mydb.commit()

values = []
for i in buid:
    x = random.randint(0,len(produce_name)-1)
    item_quantity = random.randint(1,10)
    val = (item_quantity, i[0], pid[random.randint(0,len(pid)-1)][0],)
    values.append(val)

sql = "INSERT INTO cart_items(item_id, item_quantity, buyer_id, produce_id)\
        VALUES (UUID(), %s, %s, %s)"
mycursor.executemany(sql, values)
mydb.commit()

mycursor.close()
mydb.close()
