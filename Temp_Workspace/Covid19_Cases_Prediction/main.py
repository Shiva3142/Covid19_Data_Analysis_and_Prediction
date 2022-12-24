import pandas 
import numpy
import datetime
import mysql.connector
import json
import matplotlib.pyplot as plt
with open('./config.env') as f:
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

# sql="SELECT * FROM total_india_cases;"
# query.execute(sql)
# result=query.fetchall()
# # print(query.description)
# column_names=[i[0] for i in query.description]
# print(column_names)
# # print(result)
# dataframe=pandas.DataFrame(result)
# dataframe.columns=column_names
# # print(dataframe)
# print(dataframe.describe())
# print(dataframe.info())
# # print(dataframe.corr())
# # print(dataframe['total_confirmed'].to_numpy())
# # dataframe.plot(kind='line',x="date",y="total_confirmed")
# x=dataframe['date']
# y=dataframe['total_confirmed']
# plt.plot(x,y)
# plt.show()


# # exit()

# data=[]
# with open('./data/jsondata.json') as f:
#     data=json.load(fp=f)
# # print(data.keys())
# i=0
# for key,value in data.items():
#     year=key[0:4]
#     month=key[5:7]
#     day=key[8:10]
#     date=datetime.date(int(year),int(month),int(day))
#     ordinaldate=datetime.datetime.toordinal(date)
#     # print(date)

#     # print(ordinaldate)
#     # ordinaldate=
#     # print(key)




#     total_confirmed=0
#     total_recovered=0
#     total_deaths=0
#     total_tested=0
#     total_active=0
#     total_other=0
#     delta_confirmed=0
#     delta_recovered=0
#     delta_deaths=0
#     delta_tested=0
#     delta_active=0
#     delta_other=0
#     delta7_confirmed=0
#     delta7_recovered=0
#     delta7_deaths=0
#     delta7_tested=0
#     delta7_active=0
#     delta7_other=0
#     total_vaccinated1=0
#     total_vaccinated2=0
#     delta_vaccinated1=0
#     delta_vaccinated2=0
#     delta7_vaccinated1=0
#     delta7_vaccinated2=0

#     # print(value.keys())
#     try:
#         # print(value['TT'])
#         if value['TT']!=None:
#             try:
#                 # print(value['TT']['delta'])
#                 if value['TT']['delta']!=None:
#                     try:
#                         delta_confirmed=value['TT']['delta']['confirmed']
#                         # print(value['TT']['delta']['confirmed'])
#                     except:
#                         pass
#                     try:
#                         delta_recovered=value['TT']['delta']['recovered']
#                         # print(value['TT']['delta']['recovered'])
#                     except:
#                         pass
#                     try:
#                         delta_deaths=value['TT']['delta']['deceased']
#                         # print(value['TT']['delta']['deceased'])
#                     except:
#                         pass
#                     try:
#                         delta_tested=value['TT']['delta']['tested']
#                         # print(value['TT']['delta']['tested'])
#                     except:
#                         pass
#                     try:
#                         delta_other=value['TT']['delta']['other']
#                         # print(value['TT']['delta']['other'])
#                     except:
#                         pass
#                     try:
#                         delta_vaccinated1=value['TT']['delta']['vaccinated1']
#                         # print(value['TT']['delta']['vaccinated1'])
#                     except:
#                         pass
#                     try:
#                         delta_vaccinated2=value['TT']['delta']['vaccinated2']
#                         # print(value['TT']['delta']['vaccinated2'])
#                     except:
#                         pass
#                     delta_active=delta_confirmed-delta_recovered-delta_deaths-delta_other
#             except:
#                 pass
#             try:
#                 # print(value['TT']['delta7'])
#                 if value['TT']['delta7']!=None:
#                     try:
#                         delta7_confirmed=value['TT']['delta7']['confirmed']
#                         # print(value['TT']['delta7']['confirmed'])
#                     except:
#                         pass
#                     try:
#                         delta7_recovered=value['TT']['delta7']['recovered']
#                         # print(value['TT']['delta7']['recovered'])
#                     except:
#                         pass
#                     try:
#                         delta7_deaths=value['TT']['delta7']['deceased']
#                         # print(value['TT']['delta7']['deceased'])
#                     except:
#                         pass
#                     try:
#                         delta7_tested=value['TT']['delta7']['tested']
#                         # print(value['TT']['delta7']['tested'])
#                     except:
#                         pass
#                     try:
#                         delta7_other=value['TT']['delta7']['other']
#                         # print(value['TT']['delta7']['other'])
#                     except:
#                         pass
#                     try:
#                         delta7_vaccinated1=value['TT']['delta7']['vaccinated1']
#                         # print(value['TT']['delta7']['vaccinated1'])
#                     except:
#                         pass
#                     try:
#                         delta7_vaccinated2=value['TT']['delta7']['vaccinated2']
#                         # print(value['TT']['delta7']['vaccinated2'])
#                     except:
#                         pass
#                     delta7_active=delta7_confirmed-delta7_recovered-delta7_deaths-delta7_other
#             except:
#                 pass
#             try:
#                 # print(value['TT']['total'])
#                 if value['TT']['total']!=None:
#                     try:
#                         total_confirmed=value['TT']['total']['confirmed']
#                         # print(value['TT']['total']['confirmed'])
#                     except:
#                         pass
#                     try:
#                         total_recovered=value['TT']['total']['recovered']
#                         # print(value['TT']['total']['recovered'])
#                     except:
#                         pass
#                     try:
#                         total_deaths=value['TT']['total']['deceased']
#                         # print(value['TT']['total']['deceased'])
#                     except:
#                         pass
#                     try:
#                         total_tested=value['TT']['total']['tested']
#                         # print(value['TT']['total']['tested'])
#                     except:
#                         pass
#                     try:
#                         total_other=value['TT']['total']['other']
#                         # print(value['TT']['total']['other'])
#                     except:
#                         pass
#                     try:
#                         total_vaccinated1=value['TT']['total']['vaccinated1']
#                         # print(value['TT']['total']['vaccinated1'])
#                     except:
#                         pass
#                     try:
#                         total_vaccinated2=value['TT']['total']['vaccinated2']
#                         # print(value['TT']['total']['vaccinated2'])
#                     except:
#                         pass
#                     total_active=total_confirmed-total_recovered-total_deaths-total_other
#             except:
#                 pass
        
        


#         #     try:
#         #         for totalkeys,totalvalues in value['TT'].items():
#         #             print(totalkeys)
#         #         # print()

#         #     except:
#         #         pass


#     except:
#         pass
#     i+=1


#     # print("total : ",sep="  ",end="  ")
#     # print(total_confirmed,sep="  ",end="  ")
#     # print(total_recovered,sep="  ",end="  ")
#     # print(total_deaths,sep="  ",end="  ")
#     # print(total_tested,sep="  ",end="  ")
#     # print(total_active,sep="  ",end="  ")
#     # print(total_other,sep="  ",end="  ")
#     # print()
#     # print("delta : ",end="  ")
#     # print(delta_confirmed,sep="  ",end="  ")
#     # print(delta_recovered,sep="  ",end="  ")
#     # print(delta_deaths,sep="  ",end="  ")
#     # print(delta_tested,sep="  ",end="  ")
#     # print(delta_active,sep="  ",end="  ")
#     # print(delta_other,sep="  ",end="  ")
#     # print()
#     # print("delta7 : ",end="  ")
#     # print(delta7_confirmed,sep="  ",end="  ")
#     # print(delta7_recovered,sep="  ",end="  ")
#     # print(delta7_deaths,sep="  ",end="  ")
#     # print(delta7_tested,sep="  ",end="  ")
#     # print(delta7_active,sep="  ",end="  ")
#     # print(delta7_other,sep="  ",end="  ")
#     # print()
#     sql=f"INSERT INTO total_india_cases(`date`, `total_confirmed`, `total_active`, `total_recovered`, `total_deaths`, `total_tested`, `delta_confirmed`, `delta_active`, `delta_recovered`, `delta_deaths`, `delta_tested`, `delta7_confirmed`, `delta7_active`, `delta7_recovered`, `delta7_deaths`, `delta7_tested`, `total_other`, `delta_other`, `delta7_other`, `ordinal_date`,`total_vaccinated1`,`total_vaccinated2`,`delta_vaccinated1`,`delta_vaccinated2`,`delta7_vaccinated1`,`delta7_vaccinated2`) VALUES ('{date}',{total_confirmed},{total_active},{total_recovered},{total_deaths},{total_tested},{delta_confirmed},{delta_active},{delta_recovered},{delta_deaths},{delta_tested},{delta7_confirmed},{delta7_active},{delta7_recovered},{delta7_deaths},{delta7_tested},{total_other},{delta_other},{delta7_other},{ordinaldate},{total_vaccinated1},{total_vaccinated2},{delta_vaccinated1},{delta_vaccinated2},{delta7_vaccinated1},{delta7_vaccinated2});"
#     # print(sql)
#     print("done : ",date)
#     query.execute(sql)
#     # if i==100:
#     #     break
# # # con.commit()




data=[]
with open('./data/jsondata6.json') as f:
    data=json.load(fp=f)
# print(data.keys())
i=0

for i in data:
    # print(i)
    for key,value in i.items():
        year=key[0:4]
        month=key[5:7]
        day=key[8:10]
        date=datetime.date(int(year),int(month),int(day))
        ordinaldate=datetime.datetime.toordinal(date)
        # print(date)

        # print(ordinaldate)
        # ordinaldate=
        # print(key)




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

        # print(value.keys())
        try:
            # print(value['TT'])
            if value['TT']!=None:
                try:
                    # print(value['TT']['delta'])
                    if value['TT']['delta']!=None:
                        try:
                            delta_confirmed=value['TT']['delta']['confirmed']
                            # print(value['TT']['delta']['confirmed'])
                        except:
                            pass
                        try:
                            delta_recovered=value['TT']['delta']['recovered']
                            # print(value['TT']['delta']['recovered'])
                        except:
                            pass
                        try:
                            delta_deaths=value['TT']['delta']['deceased']
                            # print(value['TT']['delta']['deceased'])
                        except:
                            pass
                        try:
                            delta_tested=value['TT']['delta']['tested']
                            # print(value['TT']['delta']['tested'])
                        except:
                            pass
                        try:
                            delta_other=value['TT']['delta']['other']
                            # print(value['TT']['delta']['other'])
                        except:
                            pass
                        try:
                            delta_vaccinated1=value['TT']['delta']['vaccinated1']
                            # print(value['TT']['delta']['vaccinated1'])
                        except:
                            pass
                        try:
                            delta_vaccinated2=value['TT']['delta']['vaccinated2']
                            # print(value['TT']['delta']['vaccinated2'])
                        except:
                            pass
                        delta_active=delta_confirmed-delta_recovered-delta_deaths-delta_other
                except:
                    pass
                try:
                    # print(value['TT']['delta7'])
                    if value['TT']['delta7']!=None:
                        try:
                            delta7_confirmed=value['TT']['delta7']['confirmed']
                            # print(value['TT']['delta7']['confirmed'])
                        except:
                            pass
                        try:
                            delta7_recovered=value['TT']['delta7']['recovered']
                            # print(value['TT']['delta7']['recovered'])
                        except:
                            pass
                        try:
                            delta7_deaths=value['TT']['delta7']['deceased']
                            # print(value['TT']['delta7']['deceased'])
                        except:
                            pass
                        try:
                            delta7_tested=value['TT']['delta7']['tested']
                            # print(value['TT']['delta7']['tested'])
                        except:
                            pass
                        try:
                            delta7_other=value['TT']['delta7']['other']
                            # print(value['TT']['delta7']['other'])
                        except:
                            pass
                        try:
                            delta7_vaccinated1=value['TT']['delta7']['vaccinated1']
                            # print(value['TT']['delta7']['vaccinated1'])
                        except:
                            pass
                        try:
                            delta7_vaccinated2=value['TT']['delta7']['vaccinated2']
                            # print(value['TT']['delta7']['vaccinated2'])
                        except:
                            pass
                        delta7_active=delta7_confirmed-delta7_recovered-delta7_deaths-delta7_other
                except:
                    pass
                try:
                    # print(value['TT']['total'])
                    if value['TT']['total']!=None:
                        try:
                            total_confirmed=value['TT']['total']['confirmed']
                            # print(value['TT']['total']['confirmed'])
                        except:
                            pass
                        try:
                            total_recovered=value['TT']['total']['recovered']
                            # print(value['TT']['total']['recovered'])
                        except:
                            pass
                        try:
                            total_deaths=value['TT']['total']['deceased']
                            # print(value['TT']['total']['deceased'])
                        except:
                            pass
                        try:
                            total_tested=value['TT']['total']['tested']
                            # print(value['TT']['total']['tested'])
                        except:
                            pass
                        try:
                            total_other=value['TT']['total']['other']
                            # print(value['TT']['total']['other'])
                        except:
                            pass
                        try:
                            total_vaccinated1=value['TT']['total']['vaccinated1']
                            # print(value['TT']['total']['vaccinated1'])
                        except:
                            pass
                        try:
                            total_vaccinated2=value['TT']['total']['vaccinated2']
                            # print(value['TT']['total']['vaccinated2'])
                        except:
                            pass
                        total_active=total_confirmed-total_recovered-total_deaths-total_other
                except:
                    pass
            
            


            #     try:
            #         for totalkeys,totalvalues in value['TT'].items():
            #             print(totalkeys)
            #         # print()

            #     except:
            #         pass


        except:
            pass
        # i+=1


        # print("total : ",sep="  ",end="  ")
        # print(total_confirmed,sep="  ",end="  ")
        # print(total_recovered,sep="  ",end="  ")
        # print(total_deaths,sep="  ",end="  ")
        # print(total_tested,sep="  ",end="  ")
        # print(total_active,sep="  ",end="  ")
        # print(total_other,sep="  ",end="  ")
        # print()
        # print("delta : ",end="  ")
        # print(delta_confirmed,sep="  ",end="  ")
        # print(delta_recovered,sep="  ",end="  ")
        # print(delta_deaths,sep="  ",end="  ")
        # print(delta_tested,sep="  ",end="  ")
        # print(delta_active,sep="  ",end="  ")
        # print(delta_other,sep="  ",end="  ")
        # print()
        # print("delta7 : ",end="  ")
        # print(delta7_confirmed,sep="  ",end="  ")
        # print(delta7_recovered,sep="  ",end="  ")
        # print(delta7_deaths,sep="  ",end="  ")
        # print(delta7_tested,sep="  ",end="  ")
        # print(delta7_active,sep="  ",end="  ")
        # print(delta7_other,sep="  ",end="  ")
        # print()
        sql=f"INSERT INTO total_india_cases(`date`, `total_confirmed`, `total_active`, `total_recovered`, `total_deaths`, `total_tested`, `delta_confirmed`, `delta_active`, `delta_recovered`, `delta_deaths`, `delta_tested`, `delta7_confirmed`, `delta7_active`, `delta7_recovered`, `delta7_deaths`, `delta7_tested`, `total_other`, `delta_other`, `delta7_other`, `ordinal_date`,`total_vaccinated1`,`total_vaccinated2`,`delta_vaccinated1`,`delta_vaccinated2`,`delta7_vaccinated1`,`delta7_vaccinated2`) VALUES ('{date}',{total_confirmed},{total_active},{total_recovered},{total_deaths},{total_tested},{delta_confirmed},{delta_active},{delta_recovered},{delta_deaths},{delta_tested},{delta7_confirmed},{delta7_active},{delta7_recovered},{delta7_deaths},{delta7_tested},{total_other},{delta_other},{delta7_other},{ordinaldate},{total_vaccinated1},{total_vaccinated2},{delta_vaccinated1},{delta_vaccinated2},{delta7_vaccinated1},{delta7_vaccinated2});"
        # print(sql)
        print("done : ",date)
        query.execute(sql)
        # if i==100:
        #     break
con.commit()










