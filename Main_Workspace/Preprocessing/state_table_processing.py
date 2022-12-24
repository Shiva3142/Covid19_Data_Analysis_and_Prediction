import pandas 
import numpy
import datetime
import mysql.connector
import json
with open('./Main_Workspace/config.env') as f:
    credentials=f.read()
credentials=credentials.split(" ")
con=None
query=None
def connect_to_database():
    global con ,query
    con=mysql.connector.connect(username=credentials[0],password=credentials[1],host=credentials[2],port=int(credentials[3]),database=credentials[4])
    query=con.cursor()
connect_to_database()
if con:
    print(con)


# exit()
def processing_for_state_table(key,value):
    year=key[0:4]
    month=key[5:7]
    day=key[8:10]
    date=datetime.date(int(year),int(month),int(day))
    ordinaldate=datetime.datetime.toordinal(date)
    # print(date)
    # print(ordinaldate)
    # print(key)
    # print(value)
    for index,element in value.items():
        # print(index)
        if index!="TT":
            # print(element)
            state=index
            total_confirmed=0
            total_recovered=0
            total_deaths=0
            total_tested=0
            total_active=0
            total_other=0
            delta_confirmed=0
            delta_recovered=0
            delta_deaths=0
            delta_tested=0
            delta_active=0
            delta_other=0
            delta7_confirmed=0
            delta7_recovered=0
            delta7_deaths=0
            delta7_tested=0
            delta7_active=0
            delta7_other=0
            total_vaccinated1=0
            total_vaccinated2=0
            delta_vaccinated1=0
            delta_vaccinated2=0
            delta7_vaccinated1=0
            delta7_vaccinated2=0
            try:
                # print(element['delta'])
                if element['delta']!=None:
                    try:
                        delta_confirmed=element['delta']['confirmed']
                        # print(element['delta']['confirmed'])
                    except:
                        pass
                    try:
                        delta_recovered=element['delta']['recovered']
                        # print(element['delta']['recovered'])
                    except:
                        pass
                    try:
                        delta_deaths=element['delta']['deceased']
                        # print(element['delta']['deceased'])
                    except:
                        pass
                    try:
                        delta_tested=element['delta']['tested']
                        # print(element['delta']['tested'])
                    except:
                        pass
                    try:
                        delta_other=element['delta']['other']
                        # print(element['delta']['other'])
                    except:
                        pass
                    try:
                        delta_vaccinated1=element['delta']['vaccinated1']
                        # print(element['delta']['vaccinated1'])
                    except:
                        pass
                    try:
                        delta_vaccinated2=element['delta']['vaccinated2']
                        # print(element['delta']['vaccinated2'])
                    except:
                        pass
                    delta_active=delta_confirmed-delta_recovered-delta_deaths-delta_other
            except:
                pass
            try:
                # print(element['delta7'])
                if element['delta7']!=None:
                    try:
                        delta7_confirmed=element['delta7']['confirmed']
                        # print(element['delta7']['confirmed'])
                    except:
                        pass
                    try:
                        delta7_recovered=element['delta7']['recovered']
                        # print(element['delta7']['recovered'])
                    except:
                        pass
                    try:
                        delta7_deaths=element['delta7']['deceased']
                        # print(element['delta7']['deceased'])
                    except:
                        pass
                    try:
                        delta7_tested=element['delta7']['tested']
                        # print(element['delta7']['tested'])
                    except:
                        pass
                    try:
                        delta7_other=element['delta7']['other']
                        # print(element['delta7']['other'])
                    except:
                        pass
                    try:
                        delta7_vaccinated1=element['delta7']['vaccinated1']
                        # print(element['delta7']['vaccinated1'])
                    except:
                        pass
                    try:
                        delta7_vaccinated2=element['delta7']['vaccinated2']
                        # print(element['delta7']['vaccinated2'])
                    except:
                        pass
                    delta7_active=delta7_confirmed-delta7_recovered-delta7_deaths-delta7_other
            except:
                pass
            try:
                # print(element['total'])
                if element['total']!=None:
                    try:
                        total_confirmed=element['total']['confirmed']
                        # print(element['total']['confirmed'])
                    except:
                        pass
                    try:
                        total_recovered=element['total']['recovered']
                        # print(element['total']['recovered'])
                    except:
                        pass
                    try:
                        total_deaths=element['total']['deceased']
                        # print(element['total']['deceased'])
                    except:
                        pass
                    try:
                        total_tested=element['total']['tested']
                        # print(element['total']['tested'])
                    except:
                        pass
                    try:
                        total_other=element['total']['other']
                        # print(element['total']['other'])
                    except:
                        pass
                    try:
                        total_vaccinated1=element['total']['vaccinated1']
                        # print(element['total']['vaccinated1'])
                    except:
                        pass
                    try:
                        total_vaccinated2=element['total']['vaccinated2']
                        # print(element['total']['vaccinated2'])
                    except:
                        pass
                    total_active=total_confirmed-total_recovered-total_deaths-total_other
            except:
                pass
            # print(state,total_confirmed,total_recovered,total_deaths,total_tested,total_active,total_other,delta_confirmed,delta_recovered,delta_deaths,delta_tested,delta_active,delta_other,delta7_confirmed,delta7_recovered,delta7_deaths,delta7_tested,delta7_active,delta7_other,total_vaccinated1,total_vaccinated2,delta_vaccinated1,delta_vaccinated2,delta7_vaccinated1,delta7_vaccinated2, sep="   ")
            sql=f"INSERT INTO total_state_cases(`date`,`state_name`, `total_confirmed`, `total_active`, `total_recovered`, `total_deaths`, `total_tested`, `delta_confirmed`, `delta_active`, `delta_recovered`, `delta_deaths`, `delta_tested`, `delta7_confirmed`, `delta7_active`, `delta7_recovered`, `delta7_deaths`, `delta7_tested`, `total_other`, `delta_other`, `delta7_other`, `ordinal_date`,`total_vaccinated1`,`total_vaccinated2`,`delta_vaccinated1`,`delta_vaccinated2`,`delta7_vaccinated1`,`delta7_vaccinated2`) VALUES ('{date}','{state}',{total_confirmed},{total_active},{total_recovered},{total_deaths},{total_tested},{delta_confirmed},{delta_active},{delta_recovered},{delta_deaths},{delta_tested},{delta7_confirmed},{delta7_active},{delta7_recovered},{delta7_deaths},{delta7_tested},{total_other},{delta_other},{delta7_other},{ordinaldate},{total_vaccinated1},{total_vaccinated2},{delta_vaccinated1},{delta_vaccinated2},{delta7_vaccinated1},{delta7_vaccinated2});"
            # print(sql)
            query.execute(sql)
    print("done : ",date)

data=[]
with open('./Main_Workspace/data/jsondata.json') as f:
    data=json.load(fp=f)

for key,value in data.items():
    processing_for_state_table(key,value)


data=[]
with open('./Main_Workspace/data/jsondata2.json') as f:
    data=json.load(fp=f)

for i in data:
    for key,value in i.items():
        processing_for_state_table(key,value)

data=[]
with open('./Main_Workspace/data/jsondata3.json') as f:
    data=json.load(fp=f)

for i in data:
    for key,value in i.items():
        processing_for_state_table(key,value)


data=[]
with open('./Main_Workspace/data/jsondata4.json') as f:
    data=json.load(fp=f)

for i in data:
    for key,value in i.items():
        processing_for_state_table(key,value)



data=[]
with open('./Main_Workspace/data/jsondata5.json') as f:
    data=json.load(fp=f)

for i in data:
    for key,value in i.items():
        processing_for_state_table(key,value)

con.rollback()


# con.commit()
con.close()

