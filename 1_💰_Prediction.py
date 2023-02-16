import streamlit as st
import re 
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
import numpy as np

st.title('Price Predcition page')
showErrorDetails = False

#This model will clean the data and send the model for predictions

def model_clean():
        #to extract the year from the completion status feature
    def search(x):
        ob1=re.compile(r'\d{4}')
        ob2=ob1.findall(x)
        if(len(ob2)!=0):
            temp=ob2[0]
        else:
            temp=2023
        return temp
    #to extract the year from the completion status feature
    def rooms(x):
        ob1=re.compile(r'\d')
        ob2=ob1.findall(x)
        if(len(ob2)!=0):
            temp=ob2[0]
        else:
            temp=0
        return temp
    #age calculator
    def extract_age(x):
        temp=2023-int(x)
        return temp
    model_data=pd.read_csv('final.csv')
    model_data.drop(['Unnamed: 0','location_details','property_name'],axis=1,inplace=True)
    #dropping the duplicate values
    model_data.duplicated().sum()
    #extracting only year part
    model_data['completion_status']=model_data['completion_status'].map(search)
    #extracting the age of the building
    model_data['age_of_building']=model_data['completion_status'].map(extract_age)
    #dropping the duplicate values
    #converting the data to lower case the removing the space
    model_data['area_type']=model_data['area_type'].str.lstrip()
    model_data['area_type']=model_data['area_type'].str.lower()
    model_data=model_data.drop_duplicates(None).reset_index()
    #extracting the size of the room
    model_data['no_rooms']=model_data['size'].map(rooms)
    model_data.drop(['completion_status','index','size','price_per_sq_ft'],axis=1,inplace=True)
    model_data=model_data[model_data['no_rooms']!=0]
    X=model_data.drop('avg_price',axis=1)
    y=model_data['avg_price']
    #one hot encoder for converting the categorical values
    col=make_column_transformer((OneHotEncoder(sparse=False),['region','availability','area_type']),remainder='passthrough')
    model=RandomForestRegressor()
    pipe=make_pipeline(col,model)
    pipe.fit(X,y)
    return pipe

def clean_model2(city):
    data=pd.read_csv('{}.csv'.format(city))
    data=data.drop(['location_details','property_name','Unnamed: 0'],axis=1)
    #converting the data to lower case the removing the space
    data['area_type']=data['area_type'].str.lstrip()
    data['area_type']=data['area_type'].str.lower()
    X=data.drop('avg_price',axis=1)
    y=data['avg_price']
    column_tran=make_column_transformer((OneHotEncoder(sparse=False),['region','size','availability','area_type']),remainder='passthrough')
    sclar=StandardScaler()
    model=RandomForestRegressor()
    pipe=make_pipeline(column_tran,model)
    pipe.fit(X,y)
    return pipe

col1,col2=st.columns(2)
with col1:
    city=st.selectbox('City',['Chennai','Pune','Bangalore','Kolkata'])
    area=st.text_input('Please specify the Carpet Area ',0)
    if city=='Bangalore':
        region=st.selectbox('Specify the Region',['bangalore north','bangalore south','bangalore east','bangalore west','bangalore central','bangalore others']) 
    elif city=='Chennai':
        region=st.selectbox('Specify the Region',['chennai north','chennai south','bangalore east','chennai west','chennai others'])
    elif city=='Kolkata':
        region=st.selectbox('Specify the Region',['kolkata north','kolkata west','kolkata east','kolkata south','kolkata others'])
    else:
        region=st.selectbox('Specify the Region',['Pune others'])

    rooms=st.select_slider('Number of rooms',[1,2,3,4,5,6,9,12])
with col2:
    if city=='Bangalore':
        avail_stat=st.selectbox('Availability status',['Ready To Move','New Launch','Under Construction','Partially Ready To Move'])
        age_of_building=int(st.text_input('Enter the age of the building',0))
        area_type=st.selectbox('Choose the Area type',['built-up area','super built-up area','carpet area'])
        pred_df=pd.DataFrame({'region':region,'availability':avail_stat,'area_type':area_type,'avg_area':area,'age_of_building':age_of_building,'no_rooms':rooms},index=[0])
    else:
        avail_stat=st.selectbox('Availability status',['Ready To Move','New Launch','Under Construction','Partially Ready To Move'])
        age_of_building=int(st.text_input('Enter the age of the building',0))
        area_type=st.selectbox('Choose the Area type',['built-up area','super built-up area','carpet area'])
        pred_df=pd.DataFrame({'region':region,'availability':avail_stat,'area_type':area_type,'age_of_building':age_of_building,'size':rooms,'avg_area':area},index=[0])

if city=='Bangalore':
    model_pipe=model_clean()
else:
    model_pipe=clean_model2(city)
estimated_price=model_pipe.predict(pred_df)
price='₹ '+str(np.round(estimated_price[0],2))+' Lakhs'
button=st.button('Submit')
if button:
    st.subheader('The Estimated Price is...')
    st.subheader(price)

