import json
import requests
data=[]
date=4
month=10
for i in range(27):
    if (date==32):
        date=1
        month+=1
    if (date<10):
        linkdate=f"2021-{month}-0{date}"
    else:
        linkdate=f"2021-{month}-{date}"
    print(linkdate)
    response = requests.get(f"https://data.covid19india.org/v4/min/data-{linkdate}.min.json")
    result=response.json()
    # print(result)
    date+=1
    data.append({linkdate:result})
    # print(data)
# data={"maindata":data}
# print(data)
with open('jsondata5.json','w') as f:
    jsondata=json.dump(data,fp=f)
    # f.write(str(data))


data=None
with open('./jsondata5.json') as f:
    data=json.load(f)
print(data[26]['2021-10-30']['MH']['districts']['Raigad']['total'])