import pandas
import numpy
from matplotlib import pyplot
from pandas.plotting import scatter_matrix
import mysql.connector
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error,mean_absolute_error
import joblib
import datetime
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.vector_ar.var_model import VAR
import warnings
warnings.filterwarnings('ignore')



class Forecasting_of_covid_cases():

    number_of_next_days=7
    def __init__(self,data,place,order1,order2,type_of_case):
        self.maindata=data
        self.prediction_start_date=self.maindata['ordinal_date'].to_numpy()[-1]
        print(data)
        self.predictingdate,self.daterange=self.returnNextdays()
        self.try_data=numpy.concatenate((self.maindata['ordinal_date'].to_numpy(),self.predictingdate),axis=None)
        self.type_of_case=type_of_case
        self.name_of_case=type_of_case
        self.lavel_of_cases=place
        self.maindata_labels=self.maindata[self.type_of_case]
        self.train_data,self.test_data=self.splitting(self.maindata,0.95)
        self.train_labels=self.train_data[self.type_of_case]
        self.test_labels=self.test_data[self.type_of_case]
        self.order_of_forecasting_models1=order1
        self.order_of_forecasting_models2=order2
        self.random_forest_model=RandomForestRegressor()


        self.forcasting_data_features=self.maindata[['date',self.type_of_case]]
        self.forcasting_train_data_features=self.train_data[['date',self.type_of_case]]
        self.forcasting_test_data_features=self.test_data[['date',self.type_of_case]]
        self.forcasting_data_features['date']=pandas.to_datetime(self.forcasting_data_features['date'])
        self.forcasting_train_data_features['date']=pandas.to_datetime(self.forcasting_train_data_features['date'])
        self.forcasting_test_data_features['date']=pandas.to_datetime(self.forcasting_test_data_features['date'])
        self.forcasting_data_features=self.forcasting_data_features.set_index('date')
        self.forcasting_train_data_features=self.forcasting_train_data_features.set_index('date')
        self.forcasting_test_data_features=self.forcasting_test_data_features.set_index('date')

        
        
    def Predict_cases(self):
        self.main_arima_model = ARIMA(self.forcasting_data_features,order=self.order_of_forecasting_models1)
        self.train_arima_model = ARIMA(self.forcasting_train_data_features,order=self.order_of_forecasting_models1)
        self.main_arima_fit_model=self.main_arima_model.fit()
        self.train_arima_fit_model=self.train_arima_model.fit()
        self.main_arima_fit_model_predicted=self.main_arima_fit_model.predict()
        self.train_arima_fit_model_predicted=self.train_arima_fit_model.predict()
        self.test_arima_predicted=self.train_arima_fit_model.forecast(steps=len(self.forcasting_test_data_features))
        self.arima_model_forcast=self.main_arima_fit_model.forecast(steps=self.number_of_next_days)
        self.try_arima_labels=numpy.concatenate((self.maindata_labels,self.arima_model_forcast))
        self.random_forest_model.fit(pandas.DataFrame(self.try_data),self.try_arima_labels)
        self.final_arima_model_forcast=self.random_forest_model.predict(pandas.DataFrame(self.try_data))[-self.number_of_next_days:]


        self.main_sarima_model=SARIMAX(self.forcasting_data_features,order=self.order_of_forecasting_models2)
        self.train_sarima_model = SARIMAX(self.forcasting_train_data_features,order=self.order_of_forecasting_models2)
        self.main_sarima_fit_model=self.main_sarima_model.fit()
        self.train_sarima_fit_model=self.train_sarima_model.fit()
        self.main_sarima_fit_model_predicted=self.main_sarima_fit_model.predict()
        self.train_sarima_fit_model_predicted=self.train_sarima_fit_model.predict()
        self.test_sarima_predicted=self.train_sarima_fit_model.forecast(steps=len(self.forcasting_test_data_features))
        self.sarima_model_forcast=self.main_sarima_fit_model.forecast(steps=self.number_of_next_days)
        self.try_sarima_labels=numpy.concatenate((self.maindata_labels,self.sarima_model_forcast))
        self.random_forest_model.fit(pandas.DataFrame(self.try_data),self.try_sarima_labels)
        self.final_sarima_model_forcast=self.random_forest_model.predict(pandas.DataFrame(self.try_data))[-self.number_of_next_days:]
        self.final_data_forcast=(self.final_arima_model_forcast+self.final_sarima_model_forcast)/2
        self.final_forecast_labels=numpy.concatenate((self.maindata_labels,self.final_data_forcast))
        self.random_forest_model.fit(pandas.DataFrame(self.try_data),self.final_forecast_labels)
        self.final_model_forcast=self.random_forest_model.predict(pandas.DataFrame(self.try_data))[-self.number_of_next_days:]
        self.final_prediction=pandas.DataFrame()
        self.final_prediction['Future Dates']=self.daterange
        self.final_prediction['ARIMA Prediction']=self.arima_model_forcast.to_numpy()
        self.final_prediction['SARIMA Prediction']=self.sarima_model_forcast.to_numpy()
        self.range_of_prediction=[]
        for i in range(self.number_of_next_days):
            self.range_of_prediction.append(self.range_finder(self.arima_model_forcast.to_numpy()[i],self.sarima_model_forcast.to_numpy()[i]))
        # print(range_of_prediction)
        self.excepted_range_of_prediction=["{}   to   {}".format(int(value[0]),int(value[1])) for value in self.range_of_prediction]
        print(self.excepted_range_of_prediction)
        self.final_prediction['Excepted Range of Prediction']=self.excepted_range_of_prediction
        
        self.final_prediction['Final Excepted Prediction']=self.final_model_forcast.astype(int)
        return self.final_prediction

    def range_finder(self,x,y):
        if x<y:
            return(x,y)
        else:
            return(y,x)



    def returnNextdays(self):
        date=self.prediction_start_date
        date_range=[]
        l=[]
        for i in range(1,self.number_of_next_days+1):
            l.append([date+i])
            date_range.append(datetime.date.fromordinal(date+i))
        return l,date_range



    def Draw_graph_of_prediction(self):
        pyplot.figure('Final model Forcasting')
        pyplot.plot(self.maindata['date'],self.maindata_labels,label='Original Data')
        pyplot.plot(self.daterange,self.arima_model_forcast,label='ARIMA Future Prediction')
        pyplot.plot(self.daterange,self.sarima_model_forcast,label='SARIMA Future Prediction')
        pyplot.plot(self.daterange,self.final_model_forcast,label='final Future {} Prediction'.format(self.name_of_case))
        for i in range(self.number_of_next_days):
            pyplot.text(self.daterange[i],self.arima_model_forcast.to_numpy()[i],'{}'.format(int(self.arima_model_forcast.to_numpy()[i])))
        for i in range(self.number_of_next_days):
            pyplot.text(self.daterange[i],self.sarima_model_forcast.to_numpy()[i],'{}'.format(int(self.sarima_model_forcast.to_numpy()[i])))
        for i in range(self.number_of_next_days):
            pyplot.text(self.daterange[i],self.final_model_forcast[i],'{}'.format(int(self.final_model_forcast[i])))
        pyplot.title("{} level {} cases prediction".format(self.lavel_of_cases,self.type_of_case))
        pyplot.xlabel('Date')
        pyplot.ylabel('{}'.format(self.name_of_case))
        pyplot.grid(axis='x')
        pyplot.legend()
        # pyplot.show()



    def ErrorEvaluation(self):
        print('ARIMA model')
        print(mean_absolute_error(self.train_arima_fit_model_predicted,self.train_labels),numpy.sqrt(mean_squared_error(self.train_arima_fit_model_predicted,self.train_labels)))
        print(mean_absolute_error(self.test_arima_predicted,self.test_labels),numpy.sqrt(mean_squared_error(self.test_arima_predicted,self.test_labels)))
        print('SARIMA model')
        print(mean_absolute_error(self.train_sarima_fit_model_predicted,self.train_labels),numpy.sqrt(mean_squared_error(self.train_sarima_fit_model_predicted,self.train_labels)))
        print(mean_absolute_error(self.test_sarima_predicted,self.test_labels),numpy.sqrt(mean_squared_error(self.test_sarima_predicted,self.test_labels)))
    
    def splitting(self,data,training_ratio):
        print('Training data percentage = {}%'.format(training_ratio*100))
        length=len(data)
        traing_indexes=int(length*training_ratio)
        training_set=data[:traing_indexes]
        testing_set=data[traing_indexes:]
        print('rows in training data : {}     rows in testing data : {}'.format(len(training_set),len(testing_set)))
        return training_set,testing_set




class Forecasting_of_covid_cases_for_india(Forecasting_of_covid_cases):
    def __init__(self,type_of_case):
        with open('./Main_Workspace/config.env') as f:
            credentials=f.read()
        credentials=credentials.split(" ")
        con = mysql.connector.connect(username=credentials[0],password=credentials[1],host=credentials[2],port=credentials[3],database=credentials[4])
        query=con.cursor()
        sql="SELECT * FROM total_india_cases"
        query.execute(sql)
        result=query.fetchall()
        column=[columns[0] for columns in query.description]
        india_data=pandas.DataFrame(result,columns=column)
        order_of_forecasting_models1=(5,0,2)
        order_of_forecasting_models2=(4,0,3)
        super().__init__(india_data, "India",order_of_forecasting_models1,order_of_forecasting_models2,type_of_case)

class Forecasting_of_covid_cases_for_district(Forecasting_of_covid_cases):
    def __init__(self,type_of_case,state_name,district_name):
        with open('./Main_Workspace/config.env') as f:
            credentials=f.read()
        credentials=credentials.split(" ")
        con = mysql.connector.connect(username=credentials[0],password=credentials[1],host=credentials[2],port=credentials[3],database=credentials[4])
        query=con.cursor()
        sql="SELECT * FROM total_district_cases WHERE state_name='{}' and district_name='{}'".format(state_name,district_name)
        query.execute(sql)
        result=query.fetchall()
        column=[columns[0] for columns in query.description]
        district_data=pandas.DataFrame(result,columns=column)
        order_of_forecasting_models1=(5,0,3)
        order_of_forecasting_models2=(3,0,3)
        super().__init__(district_data,district_name,order_of_forecasting_models1,order_of_forecasting_models2,type_of_case)



if __name__=="__main__":
    india_class=Forecasting_of_covid_cases_for_district('delta_confirmed','MH','Raigad')
    print(india_class.Predict_cases())
    india_class=Forecasting_of_covid_cases_for_district('delta_recovered','MH','Raigad')
    print(india_class.Predict_cases())
    india_class=Forecasting_of_covid_cases_for_district('delta_deaths','MH','Raigad')
    print(india_class.Predict_cases())
    india_class=Forecasting_of_covid_cases_for_district('delta_active','MH','Raigad')
    print(india_class.Predict_cases())
    # n=0
    # while n!=5:
    #     intinput=int(input('Enter the option : '))
    #     if intinput==0:
    #         print(predicted_data)
    #     if intinput==1:
    #         india_class.Draw_graph_of_prediction()
    #         pyplot.show()
    #     if intinput==2:
    #         india_class.ErrorEvaluation()
    #     else:
    #         exit()
    #     n+=1







