from flask import Flask,render_template,redirect,request,send_from_directory,jsonify
import mysql.connector
import pandas
from Main import Forecasting_of_covid_cases_for_district,Forecasting_of_covid_cases_for_india, Forecasting_of_covid_cases_for_state
import matplotlib.pyplot as pyplot
import sklearn

with open('./Main_Workspace/config.env') as f:
    credentials=f.read()
credentials=credentials.split(" ")
con = mysql.connector.connect(username=credentials[0],password=credentials[1],host=credentials[2],port=credentials[3],database=credentials[4])
query=con.cursor()
visualization_type='statistical'
cases_level='district_level'
state_name='MH'
district_name='Raigad'
start_date="2020-01-30"
last_date="2021-10-31"
class_confirmed=[]
class_recovered=[]
class_deaths=[]
class_active=[]
confirmed_result=[]
recovered_result=[]
deaths_result=[]
active_result=[]
number_of_next_days=15
graph_data=[]
confirmed_data=[]
recovered_data=[]
deaths_data=[]
active_data=[]
delta_confirmed_data=[]
delta_recovered_data=[]
delta_deaths_data=[]
delta_active_data=[]
combined_total_data=[]
combined_delta_data=[]
combined_delta7_data=[]
vaccination_data=[]


app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
    # return 'hello world'


@app.route('/machinelearning')
def machinelearning():
    global class_confirmed,class_recovered,class_deaths,class_active,confirmed_result,recovered_result,deaths_result,active_result
    print(confirmed_result)
    return render_template('final_prediction_input.html')
    # return 'Machine Learning'

@app.route('/covidprediction',methods=['POST','GET'])
def covidprediction():
    global class_confirmed,class_recovered,class_deaths,class_active,confirmed_result,recovered_result,deaths_result,active_result
    icu_requirement="ICU requrement is not Available for this place"
    if request.method=='POST':
        print(request.form)
        cases_level=request.form.get('cases_level')
        state_name=request.form.get('state')
        district_name=request.form.get('district')
        if cases_level=='india_level':
            class_confirmed=Forecasting_of_covid_cases_for_india('delta_confirmed')
            confirmed_result=class_confirmed.Predict_cases()
            print(confirmed_result)
            class_recovered=Forecasting_of_covid_cases_for_india('delta_recovered')
            recovered_result=class_recovered.Predict_cases()
            print(recovered_result)
            class_deaths=Forecasting_of_covid_cases_for_india('delta_deaths')
            deaths_result=class_deaths.Predict_cases()
            print(deaths_result)
            class_active=Forecasting_of_covid_cases_for_india('delta_active')
            active_result=class_active.Predict_cases()
            print(active_result)
            place_name="India"
        elif cases_level=='state_level':
            class_confirmed=Forecasting_of_covid_cases_for_state('delta_confirmed',state_name)
            confirmed_result=class_confirmed.Predict_cases()
            print(confirmed_result)
            class_recovered=Forecasting_of_covid_cases_for_state('delta_recovered',state_name)
            recovered_result=class_recovered.Predict_cases()
            print(recovered_result)
            class_deaths=Forecasting_of_covid_cases_for_state('delta_deaths',state_name)
            deaths_result=class_deaths.Predict_cases()
            print(deaths_result)
            class_active=Forecasting_of_covid_cases_for_state('delta_active',state_name)
            active_result=class_active.Predict_cases()
            print(active_result)
            place_name="{} , India".format(state_name)
        elif cases_level=='district_level':
            class_confirmed=Forecasting_of_covid_cases_for_district('delta_confirmed',state_name,district_name)
            confirmed_result=class_confirmed.Predict_cases()
            print(confirmed_result)
            class_recovered=Forecasting_of_covid_cases_for_district('delta_recovered',state_name,district_name)
            recovered_result=class_recovered.Predict_cases()
            print(recovered_result)
            class_deaths=Forecasting_of_covid_cases_for_district('delta_deaths',state_name,district_name)
            deaths_result=class_deaths.Predict_cases()
            print(deaths_result)
            class_active=Forecasting_of_covid_cases_for_district('delta_active',state_name,district_name)
            active_result=class_active.Predict_cases()
            print(active_result)
            class_total_active=Forecasting_of_covid_cases_for_district('total_active',state_name,district_name)
            total_active_result=class_total_active.Predict_cases()
            print(total_active_result)
            icu_data=pandas.read_csv('./Main_Workspace/data/icu_counts.csv')
            # print(icu_data)
            district_icu_data=icu_data[icu_data['district']==district_name]
            if len(district_icu_data)>0:
                icu_numbers=district_icu_data['icu_count'].to_numpy()[0]
                isolation_beds=district_icu_data['isolation_bed_count'].to_numpy()[0]
                predicted_active_cases=total_active_result['Final Excepted Prediction'].to_numpy()[-1]
                # print(icu_numbers)
                # print(isolation_beds)
                print(predicted_active_cases)
                if icu_numbers>=predicted_active_cases*1.15:
                    icu_requirement=" There are Suffecient Numbers ICUs are Available "
                    if isolation_beds>=predicted_active_cases*1.5:
                        icu_requirement=icu_requirement+" and There are also Suffecient Numbers Isolation Beds are Available "
                    else:
                        icu_requirement=icu_requirement+" But There are {} ICU beds in {} which is not Suffecient for Future ".format(icu_numbers,district_name)
                else:
                    icu_requirement="There are {} ICU beds in {} which is not Suffecient for Future ".format(icu_numbers,district_name)
                    if isolation_beds>=predicted_active_cases*1.5:
                        icu_requirement=icu_requirement+" But There are Suffecient Numbers Isolation Beds are Available "
                    else:
                        icu_requirement=icu_requirement+"and There are {} ICU beds in {} which is also not Suffecient for Future ".format(icu_numbers,district_name)
                print(icu_data[icu_data['district']==district_name])        
            place_name="{} , {} , India".format(district_name,state_name)
        return render_template('Final_Prediction.html',number_of_next_days=number_of_next_days,place_name=place_name,confirmed_result=confirmed_result,recovered_result=recovered_result,deaths_result=deaths_result,active_result=active_result,icu_requirement=icu_requirement)
    else:
        return redirect('final_prediction_input')
    # return 'Machine Learning'

@app.route('/get_district_names/<string:state_name>')
def get_district_names(state_name):
    # print(str(state_name))
    global query
    sql1="SELECT distinct district_name FROM total_district_cases where state_name='{}' and district_name!='Unknown';".format(state_name)
    query.execute(sql1)
    district_names=query.fetchall()
    # print(district_names)
    districts={"district_list":district_names}
    return jsonify(districts)

@app.route('/get_target_data/<string:string_value>')
def get_target_data(string_value):
    print(str(string_value))
    global class_confirmed,class_recovered,class_deaths,class_active,confirmed_result,recovered_result,deaths_result,active_result
    result=pandas.DataFrame()
    if string_value=='confirmed':
        result=confirmed_result
    elif string_value=='recovered':
        result=recovered_result
    elif string_value=='death':
        result=deaths_result
    elif string_value=='active':
        result=active_result
    # data={'future_dates':result['Future Dates']}
    # data.update({'ARIMA_Prediction':result['ARIMA Prediction']})
    # data.update({'SARIMA_Prediction':result['SARIMA Prediction']})
    # data.update({'Final_Excepted_Prediction':result['Final Excepted Prediction']})
    # data={'prediction_data':data}
    # print(data)
    return result.to_json()

@app.route('/get_graph_data/<string:string_value>')
def get_graph_data(string_value):
    global confirmed_data,recovered_data,deaths_data,active_data,delta_confirmed_data,delta_recovered_data,delta_deaths_data,delta_active_data,combined_total_data,combined_delta_data,combined_delta7_data,vaccination_data  
    if string_value=='total_confirmed':
        return confirmed_data.to_json()
    elif string_value=='total_recovered':
        return recovered_data.to_json()
    elif string_value=='total_death':
        return deaths_data.to_json()
    elif string_value=='total_active':
        return delta_confirmed_data.to_json()
    elif string_value=='delta_confirmed':
        return delta_confirmed_data.to_json()
    elif string_value=='delta_recovered':
        return delta_recovered_data.to_json()
    elif string_value=='delta_death':
        return delta_deaths_data.to_json()
    elif string_value=='delta_active':
        return delta_active_data.to_json()
    elif string_value=='combined_total':
        return combined_total_data.to_json()
    elif string_value=='combined_delta':
        return combined_delta_data.to_json()
    elif string_value=='combined_delta7':
        return combined_delta7_data.to_json()
    elif string_value=='combined_vaccination':
        return vaccination_data.to_json()
    else:
        delta_confirmed_data.to_json()

@app.route('/get_graph/<string:string_value>')
def get_graph(string_value):
    print(str(string_value))
    global class_confirmed,class_recovered,class_deaths,class_active,confirmed_result,recovered_result,deaths_result,active_result
    if string_value=='confirmed':
        class_confirmed.Draw_graph_of_prediction()
    elif string_value=='recovered':
        class_confirmed.Draw_graph_of_prediction()
    elif string_value=='death':
        class_confirmed.Draw_graph_of_prediction()
    elif string_value=='active':
        class_confirmed.Draw_graph_of_prediction()
    pyplot.show()
    return "done"


@app.route('/visualization',methods=['POST','GET'])
def visualization():
    global visualization_type,cases_level,state_name,district_name
    global query
    if request.method=='POST':
        print(request.form)
        visualization_type=request.form.get('visualization_type')
        cases_level=request.form.get('cases_level')
        state_name=request.form.get('state')
        district_name=request.form.get('district')
        if request.form.get('visualization_type')=='statistical':
            return redirect('/statistics')
        elif request.form.get('visualization_type')=='graphical':
            return redirect('/graphs')
    else:
        return render_template('visualization.html')

@app.route('/statistics',methods=['POST','GET'])
def statistics():
    global visualization_type,cases_level,state_name,district_name,start_date,last_date
    place="India"
    
    if request.method=="POST":
        print(request.form)
        start_date=request.form.get('start_date')
        last_date=request.form.get('last_date')
    if cases_level=='india_level':
        sql1="SELECT * FROM total_india_cases WHERE date>='{}' and date<='{}' order by ordinal_date desc;".format(start_date,last_date)
    elif cases_level=='state_level':
        sql1="SELECT * FROM total_state_cases where state_name='{}' and date>='{}' and date<='{}' order by ordinal_date desc;".format(state_name,start_date,last_date)
        place=state_name+", "+place
    elif cases_level=='district_level':
        sql1="SELECT * FROM total_district_cases where district_name='{}' and date>='{}' and date<='{}' order by ordinal_date desc;".format(district_name,start_date,last_date)
        place=district_name+", "+state_name+","+place
        
    query.execute(sql1)
    result1=query.fetchall()
    column=[columns[0] for columns in query.description]
    print(column)
    data=pandas.DataFrame(result1,columns=column)
    print(data)
    data=data.drop('index_no',axis=1)
    corrrelation=data.corr()
    corrrelation['columns']=corrrelation.columns
    print(corrrelation)
    description=data.describe()
    print(description)
    description['columns']=['count','mean','standard deviation','minimum','25% th value','50% th value','75% th value','maximum']
    return render_template('statistics.html',place=place,start_date=start_date,last_date=last_date,data=data,correlation=corrrelation,description=description,columns=column)

@app.route('/graphs',methods=['POST','GET'])
def graphs():
    global visualization_type,cases_level,state_name,district_name,start_date,last_date,graph_data
    global confirmed_data,recovered_data,deaths_data,active_data,delta_confirmed_data,delta_recovered_data,delta_deaths_data,delta_active_data,combined_total_data,combined_delta_data,combined_delta7_data,vaccination_data  
    
    place="India"
    if request.method=="POST":
        print(request.form)
        start_date=request.form.get('start_date')
        last_date=request.form.get('last_date')
    if cases_level=='india_level':
        sql1="SELECT * FROM total_india_cases WHERE date>='{}' and date<='{}' order by ordinal_date asc;".format(start_date,last_date)
    elif cases_level=='state_level':
        sql1="SELECT * FROM total_state_cases where state_name='{}' and date>='{}' and date<='{}' order by ordinal_date asc;".format(state_name,start_date,last_date)
        place=state_name+", "+place
    elif cases_level=='district_level':
        sql1="SELECT * FROM total_district_cases where district_name='{}' and date>='{}' and date<='{}' order by ordinal_date asc;".format(district_name,start_date,last_date)
        place=district_name+", "+state_name+","+place
    query.execute(sql1)
    result1=query.fetchall()
    column=[columns[0] for columns in query.description]
    print(column)
    data=pandas.DataFrame(result1,columns=column)
    print(data)
    data['date']=[str(date) for date in data['date'].to_numpy()]
    graph_data=data
    confirmed_data=data[['date','total_confirmed']]
    recovered_data=data[['date','total_recovered']]
    deaths_data=data[['date','total_deaths']]
    active_data=data[['date','total_active']]
    delta_confirmed_data=data[['date','delta_confirmed']]
    delta_recovered_data=data[['date','delta_recovered']]
    delta_deaths_data=data[['date','delta_deaths']]
    delta_active_data=data[['date','delta_active']]
    combined_total_data=data[['date','total_confirmed','total_recovered','total_deaths','total_active']]
    combined_delta_data=data[['date','delta_confirmed','delta_recovered','delta_deaths','delta_active']]
    combined_delta7_data=data[['date','delta7_confirmed','delta7_recovered','delta7_deaths','delta7_active']]
    vaccination_data=data[['date','delta_vaccinated1','delta_vaccinated2']]
    print(combined_total_data)
    return render_template('graphs.html',place=place,start_date=start_date,last_date=last_date,data=data,columns=column)

if __name__=='__main__':
    app.run(debug=True)
    con.close()