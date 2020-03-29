import mysql.connector
import random 
from random import randrange
import datetime 
import time
import bcrypt

mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "",
  database = "farmeasy"
)

names = ['Yash','Harshit','Aman','Amar','Shadab']
role = ['farmer','buyer','delivery agent']
address = ['Mumbai','Delhi','Pune','Banglore','Kolkata']
produce_name = ['tomato','apple','chanadal','wheat','cloves']
produce_price = [50,247,358,140,174]
produce_quantity = random.randint(1,10)
produce_category = ['vegetable','fruit','pulse','grains','spices']

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
mycursor.execute("DELETE FROM cart_items")
mydb.commit()
mycursor.execute("DELETE FROM delivery")
mydb.commit()
mycursor.execute("DELETE FROM buyer")
mydb.commit()
mycursor.execute("DELETE FROM produce")
mydb.commit()
mycursor.execute("DELETE FROM farmer")
mydb.commit()
mycursor.execute("DELETE FROM delivery_agent")
mydb.commit()
mycursor.execute("DELETE FROM delivery_agency")
mydb.commit()
mycursor.execute("DELETE FROM user")
mydb.commit()

for i in range (0,100):

    sql = "INSERT INTO user(user_id,user_name,user_email,user_phone,user_address,user_password,user_image,user_role) VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s)"
    x = random.randint(0,len(names)-1)
    y = random.randint(0,2)    
    phone = random.randrange(1000000000, 9999999999)
    user_image = "https://www.google.co.in/search?q=profile+image+&tbm=isch&ved=2ahUKEwisupSF9rroAhWGZSsKHbheCZIQ2-cCegQIABAA&oq=profile+image+&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCABQ9BxYzUtg5FVoA3AAeACAAZsBiAGMFZIBBTExLjE1mAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ei=TxV-XuzWAYbLrQG4vaWQCQ&authuser=1&bih=610&biw=1280#imgrc=L1-qFJ4VKpwwwM"
    passwd = b'abcde'
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    val = (names[x],names[x]+str(i)+'@gmail.com',phone,address[x],hashed,user_image,role[y])
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "SELECT user_id,user_role FROM user"
    mycursor.execute(sql)
    uid = mycursor.fetchall()

for i in range (0,4):
    
    agency_id = ['0834f5d1-70d0-11ea-b18a-544810dacaa5','0810ccab-70d0-11ea-b18a-544810dacaa5','0910cca0-70d0-11ea-b18a-544810dacaa5','07d5ecda-70d0-11ea-b18a-544810dacaa5']
    sql = "INSERT INTO delivery_agency(agency_id,intracity_rates,intercity_rates,agency_name) VALUES (%s, %s, %s, %s)"
    agency_name = ['Indian Post','FedX','Shipping Corp.','iThink Logistics']
    intercity_rates = [200,314,155,266]
    intracity_rates = [50,35,42,37]
    val = (agency_id[i],intracity_rates[i],intercity_rates[i],agency_name[i])
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "SELECT agency_id FROM delivery_agency"
    mycursor.execute(sql)
    aid = mycursor.fetchall()

print(aid)

for i in uid :
    print(i)

    if i[1] == 'farmer':
        fid = i[0]
        sql = "INSERT INTO farmer(farmer_id) VALUES (%s)"
        val = fid
        params = (val,)
        mycursor.execute(sql, params) 
        mydb.commit() 

    if i[1] == 'buyer':
        buid = i[0]
        sql = "INSERT INTO buyer(buyer_id) VALUES (%s)"
        val = buid
        params = (val,)
        mycursor.execute(sql, params) 
        mydb.commit() 


    if i[1] == 'delivery agent':
        daid = i[0]
        x = random.randint(0,3)
        sql = "INSERT INTO delivery_agent(delivery_agent_id,agency_id) VALUES (%s , %s)"
        val = daid
        val1 = str(aid[x][0])
        params = (val,val1,)
        mycursor.execute(sql,params)
        mydb.commit() 

sql = "SELECT buyer_id FROM buyer"
mycursor.execute(sql)
buid = mycursor.fetchall()    
print(buid)

for i in buid:

    sql = "INSERT INTO delivery(delivery_id,pickup_time,drop_time,buyer_id,delivery_status) VALUES (UUID(), %s, %s, %s, %s)"
    pickup = (randomDate("2020/03/27 8:00", "2020/03/27 20:00", random.random()))
    drop = (randomDate("2020/03/28 8:00", "2020/03/28 20:00", random.random()))

    delivery_status = ['delivered','shipping','pending']
    x = random.randint(0,2)
    if delivery_status[x] == 'delivered':
        params = (pickup,drop,i[0],delivery_status[x],)
        mycursor.execute(sql, params)
        mydb.commit()
    if delivery_status[x] == 'shipping':
        params = (pickup,"NA",i[0],delivery_status[x],)
        mycursor.execute(sql, params)
        mydb.commit()
    if delivery_status[x] == 'pending':
        params = ("NA","NA",i[0],delivery_status[x],)
        mycursor.execute(sql, params)
        mydb.commit()
    
    sql = "INSERT INTO cart_items(item_id,item_price,item_quantity,item_name,buyer_id) VALUES (UUID(), %s, %s, %s, %s)"
    x = random.randint(0,len(produce_name)-1)
    item_quantity = random.randint(1,10)
    item_name = produce_name[x]
    item_price = item_quantity*produce_price[x]
    params = (item_price,item_quantity,item_name,i[0],)
    mycursor.execute(sql, params)
    mydb.commit()

sql = "SELECT delivery_id,buyer_id FROM delivery"
mycursor.execute(sql)
did = mycursor.fetchall()    
print(did)

for i in did:
    
    sql = "INSERT INTO orders(buyer_id,order_id,order_quantity,order_date,order_price,delivery_id) VALUES (%s, UUID(), %s, %s, %s, %s)"
    order_quantity = random.randint(1,10)
    order_price = random.randint(1000,9999)
    order_date = (randomDate("2020/03/23 8:00", "2020/03/26 23:00", random.random()))
    params = (i[1],order_quantity,order_date,order_price,i[0],)
    mycursor.execute(sql, params)
    mydb.commit()

 
sql = "SELECT farmer_id FROM farmer"
mycursor.execute(sql)
fid = mycursor.fetchall()    
print(fid)

for i in fid  :
    
    sql = "INSERT INTO produce(produce_id,farmer_id,produce_name,produce_price,produce_quantity,produce_image,produce_category) VALUES (UUID(), %s, %s, %s, %s, %s, %s)"
    x = random.randint(0,len(produce_name)-1)
    y = random.randint(0,(len(fid)-1))
    params = (str(fid[y][0]),produce_name[x],produce_price[x],produce_quantity,produce_price[x],produce_category[x],)
    mycursor.execute(sql, params)
    mydb.commit()




    

    





