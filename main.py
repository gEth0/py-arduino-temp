#! python3.8
try:
    import serial
    import time
    import mysql.connector
    from mysql.connector import cursor
    from datetime import datetime
    import matplotlib.pyplot as plt
    import numpy as np
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import os
    import sys
except:
    print('Unable to find all the dependences needed! Look at the dependences.txt')
    quit()
try:
    ardPort='/dev/ttyACM0'#Set here the arduino port which is connected to
    arduino=serial.Serial(ardPort,9600)
    print('Found Arduino at ',ardPort)
except:
    print(f'Error Unable to find Arduino on {ardPort} port')
    quit()

try:
    db_one=mysql.connector.connect(
        host='localhost',#set in base of your mysql connection and database, keep this if you didn't modified the config file
        user='root', #set in base of your mysql connection and database, keep this if you didn't modified the config file
        password=''
        )

    c_DB='create database if not exists temp_hum;'
    cursor=db_one.cursor()

    cursor.execute(c_DB)
    db_one.commit()
except:
    print('Unable to create database')

try:
    db=mysql.connector.connect(
        host='localhost',#set in base of your mysql connection and database, keep this if you didn't modified the config file
        user='root', #set in base of your mysql connection and database, keep this if you didn't modified the config file
        password='',
        database='temp_hum' #keep this name (the script will automatically create a new database with this name if not exists yet)
    )
except:
    print('Unable to connect at Mysql service. Check if it is running on Localhost')
    quit()

while True:
    try:
        email=open('./email.txt','r')
        if email.readline() == '':
            print('Add your Email and the bot ones in the email.txt file')
            email.close()
            quit()
        else:
            print('Emails have been read correctly')
    except:
        print('Unable to find or open "email.txt"')
        quit()
    temp=str(arduino.readline())
    tot_array=list(temp)
    
    temp_fin=tot_array[2], tot_array[3]
    hum=tot_array[5],tot_array[6]
    hum="".join(hum)
    temp_fin="".join(temp_fin)
    hum=int(hum)
    temp_fin=int(temp_fin)
    print(temp_fin,hum)
    try:
        cursor=db.cursor()
        hour=(float(datetime.today().strftime('%H.%M')))
        giorno=(str(datetime.today().strftime('%Y-%m-%d')))
        
        sql='insert into  ArdTempData (temperatura , umidità, ora, giorno) values (%s,%s,%s,%s);'
        values=(temp_fin,hum,hour,giorno)
        try:

            c_TB='create table if not exists ArdTempData (temperatura int , umidità int , ora float , giorno varchar(255));'
            cursor.execute(c_TB)
            db.commit()
        except:
            print('Unable to create table')
        time.sleep(2)
        cursor.execute(sql,values)
        db.commit()
    except:
        print('Unable to update data on database')
        break
    #Waiting time
    time.sleep(3600) #Set here the time in sec for repeating the sending and the generating of the graph
    try:
        sql_dump_y=f"select temperatura from ArdTempData where giorno='{giorno}'"
        cursor_dump_y=db.cursor()
        cursor_dump_y.execute(sql_dump_y)
        response_temp=cursor_dump_y.fetchall()
    except:
        print('Uable to dump data from database. Check your Mysql database connection')
        break
    arr_y=[]
    for row in response_temp:
        arr_y.append(row)

    sql_dump_x=f"select ora from ArdTempData where giorno='{giorno}'"
    cursor_dump_x=db.cursor()
    cursor_dump_x.execute(sql_dump_x)
    response_ora=cursor_dump_x.fetchall()
    arr_x=[]
    for row in response_ora:
        arr_x.append(row)
    x=arr_x
    y=arr_y
    plt.plot(x, y, marker = "o", color = 'red')
    plt.title("temperatura")
    plt.xlabel("X")
    plt.ylabel("Y")
    try:
        hour=str(hour)
        plt.savefig(f'temp_grafico_{hour}_{giorno}.png')
    except:
        print('Unable to save graphic')
        break
    #Email preparation
    email_c=open('./email.txt','r')
    fromaddr = email_c.readline()    
    password=email_c.readline()
    toaddr = email_c.readline()
    email_c.close()
    
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = f"Grafico del Giorno {giorno} , {hour}"
    body = "Ecco il grafico di oggi"

    msg.attach(MIMEText(body, 'plain'))
    try:

        filename = f"temp_grafico_{hour}_{giorno}.png"
        attachment = open(f"./temp_grafico_{hour}_{giorno}.png", "rb")
    except:
        print('Unable to find any Graphic')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(fromaddr, password)
    except:
        print('Unable to login at Email Service : Control your Mail or Password')
    text = msg.as_string()
    graph=f"./temp_grafico_{hour}_{giorno}.png"
    try:

        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print('Email sent')
    except:
        print('Unable to send Email')
        break
    try:
        os.remove(graph)
        print(graph, 'deleted')
    except:
        print('Unable to remove the last Graphic')
#gEth0