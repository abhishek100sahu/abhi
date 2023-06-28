
"""
Created on Fri Mar 26 10:17:24 2021

@author:taterao, kaviya 
"""


from flask import Flask,render_template,request,redirect,jsonify,make_response
# from flask_mysqldb import MySQL
import psycopg2
from flask_cors import CORS
 


import socket       #import socket module
import psycopg2  #import postgres module
from datetime import datetime  #import datetime module
import time         #import time module
import random            # importing the random module
from threading import Thread  # importing threading module
import yaml      # importing yaml module

with open(r'postgres_config.yaml') as file: # opening yaml config file
    Config_File= yaml.load(file, Loader=yaml.FullLoader)
    HOST=Config_File['host']
    PORT=Config_File['Port']
    DB_Uname=Config_File['Database_Username']
    #print(DB_Uname)
    DB_password=Config_File['Database_pass']
    #print(DB_password)
    DB_name=Config_File['Database_name']
    print(DB_name)
    DB_Id=Config_File['Database_hostid']
    #print(DB_Id)
    UID=Config_File['Randum_no_range_2']
    Port_no=Config_File['Port_no']
    
    #print(UID)
#conn = mysql.connector.connect(user=DB_Uname, password=DB_password, host= DB_Id, database=DB_name)  
timestr = datetime.now()
 
#CURRENT_TIMESTAMP= now.strftime("%H:%M:%S")
#CURRENT_TIMESTAMP = time.strftime("%Y-%m-%d %H:%M:%S")
#CURRENT_TIMESTAMP=str(CURRENT_TIMESTAMP)

#creating socket connection
Serv_Socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #ip addresss and type of communication
Serv_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #to reuse the file
Serv_Socket.setblocking(1)
host=socket.gethostname()
#host='192.168.2.20'
#try:
# Serv_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

Serv_Socket.bind((HOST,PORT))  #bind with ip and host
#Serv_Socket.bind((host,8090)) 
#except:
    #print("ERROR TO CONNECT...")
    
Serv_Socket.listen(20)  #listen number of connection
#print("server has started")  
threads = [] 

def getConnection():
    print("INSIDE GET CONNECTION")
    mydb = psycopg2.connect(user=DB_Uname, password=DB_password, host= DB_Id, database=DB_name,port=Port_no)
    # conn = psycopg2.connect(database = "sample_ts_db", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")
    #print("mydb:",mydb) 
    return mydb
 
  
def formating(data):   #function to formate response data to readable formate
    Response=str(data)
 	#Response=Response.replace("\\n\\r","")
    Response=Response.replace("b'","")
    Repsonse=Response.replace("\\x","")
    Response=Response.replace("EM","")
    Response=Response.replace("'","")
    Response=Response.replace("\\x0","")
    Response=Response.replace("\\x01","")
    return  Response 

def data_base(Uid,Tem,RH,Lux,CO2,PM2_5,PM10): #function to connect mysql database and insert data to database
     conn=getConnection()
     #print('conn',conn)	
    # conn = mysql.connector.connect(user=DB_Uname, password=DB_password, host= DB_Id, database=DB_name)
     CURRENT_TIMESTAMP = time.strftime("%Y-%m-%d %H:%M:%S")

     #print("Inside DATABSE FUN CON ..",conn)
     CURRENT_TIMESTAMP=str(CURRENT_TIMESTAMP)
     #print(CURRENT_TIMESTAMP)
     Tem=str(Tem)
     #print('temp',Tem)
     Uid=str(Uid)
     #print(Uid)
     RH=str(RH)
     #print(RH)
     Lux=str(Lux)
     #print(Lux)
     CO2=str(CO2)
     #print(CO2)
     PM2_5=str(PM2_5)
     #print(PM2_5)
     PM10=str(PM10)
     sql = "INSERT INTO sensor_data (nodeid, temp, humidity, lightIntensity, co2, pm2_5, pm10, time) VALUES (%s , %s , %s , %s ,%s,%s , %s, %s)"
     val = (Uid,Tem,RH,Lux,CO2,PM2_5,PM10,CURRENT_TIMESTAMP)
     #create connection with database
      
     #conn = mysql.connector.connect(user='root', password='cdac', host='10.182.1.175', database='SATServerTCP') 
     #print("conn",conn)
     cur = conn.cursor()
     #print("cur",cur)
     try: #try block to execute sql query 
       cur.execute(sql,val)
       conn.commit()  
     except mysql.connector.Error as err:
      #print("error",err)
      conn.rollback() # Rolling back in case of error
      conn.close()   
     return
def data_extract(Data): # function to exratct data from receive packet     
    length=len(Data)
    if length>0:
     #print("inside exreact pack",Data)
     #Data=data.split(";") 
     #print("DATA:",Data)
     Uid=Data[1]
     #print("uid",Uid)
     Tem=Data[2]
     #print("TEM",Tem)
     RH=Data[3]
     Lux=Data[4]
     CO2=Data[5]
     PM2_5=Data[6]
     PM10=Data[7]
     data_base(Uid,Tem,RH,Lux,CO2,PM2_5,PM10)
  
    else:
     pass     
def connect(Client):   #Function to connect tcp client get data and send response back
    while True:    
       # global timestr
        conn=getConnection()
        id=str(random.randint(100,UID))  #generate random number or Uid
        #print("id...",id)
        data=Client.recv(1024)  #receive the data
        #print("recvdata:",data)
        length=len(data)
        if length>0:
         Response=formating(data)
         #print("format resp:",Response)
         Data=Response.split(";")  #split receive  data   
         #print("format data1",Data)     
         if Data[0]=='1':
          #print("Data reg:",Data) 
          Uid_loc=Data[2]#[11:16]
          #print("Uid_loc",Uid_loc)
          Macid=Data[1]#[2:10] 
          #print("Macid",Macid) 
          macid=str(Macid)
          #print("macid",macid)
          sentid=Uid_loc+id
          #print("sentid",sentid)
          cursor = conn.cursor()
          sql_1="select unique_id from dev_list where device_mac=%s;"
          val1=(macid,)
          cursor.execute(sql_1,val1) 
          record= cursor.fetchall()
          #print("rrrrrrrrrrrrrrr:",record)
        
                           
          if len(record)==0:
           
           #print("sentid ",sentid)
           sentuid=sentid
           #print("sentuid",sentuid)
           Client.send(bytes(sentuid,encoding="utf-8"))  #send data to client

           sql = "INSERT INTO dev_list (device_mac,device_location,added_time,unique_id) VALUES (%s , %s , %s , %s )"
           val = (macid,Uid_loc,timestr,sentuid,)
           #print("mac",macid)
           #print("loc",device_location)
           #print("addedtime",added_time)
           #print("unique_id",sentuid)
           try: #try block to execute sql query
            cursor = conn.cursor()
            cursor.execute(sql,val)
            conn.commit()  
           except:
            conn.rollback() # Rolling back in case of error
            conn.close()
          else:
            Record=record[0]
            Record=str(Record)
            #print("avilid",Record)
            Client.send(bytes(Record,encoding="utf-8"))  #send data to client
         else:
          #print("data",data)         
          #Packet=formating(Data)  #calling formating function 
          #print("packet1:",Data)
          #Response_Pack=formating(Packet) #calling formating function
          data_extract(Data) #calling data_extract function         
  

#if __name__=="__main":  
#print('main..')  
while True:
       print("inside while....")
       try:
            Client, addr = Serv_Socket.accept()
            #print("client:",Client) 
            t = Thread(target=connect, args=[Client])
            threads.append(t)
            t.start()
       except Exception as e:
            Client.close()
            print("ERROR",e)         
       # c.send(bytes("hello",encoding="utf-8")
       # Serv_Socket.close()''' 
      # app.run(debug=True)   

"""if __name__=="__main":
    print('main 2....')
    app.run(debug=True)"""





