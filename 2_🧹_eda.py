import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#importing the data
data=pd.read_csv('final.csv')
data.drop(['Unnamed: 0','location_details'],inplace=True,axis=1)
st.set_page_config(layout='wide')
st.title('Property Management dashboard')
col1,col2=st.columns(2)

def select_city():
    city=st.selectbox('City',['Bangalore','kolkata','chennai','pune','UtterPradesh'])
    if city=='Bangalore':
        df1=pd.read_csv('final.csv')
    if city=='kolkata':
        df1=pd.read_csv('kolkata.csv')
    if city=='chennai':
        df1=pd.read_csv('chennai_data.csv')
    if city=='pune':
        df1=pd.read_csv('pune.csv')
    if city=='UtterPradesh':
        df1=pd.read_csv('Utterpradesh.csv')
    return df1


def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{:.1f}%\n({v:d})'.format(pct, v=val)
        return my_format





with col1:
    continaer1=st.container()
    data_selected=select_city()
    x_element=st.selectbox('Parameter',['region','availability','area_type','size'])
    #y_element=st.selectbox('Y-Element',['avg_area','avg_price'])
    st.subheader('Count Plot')
    fig=plt.figure()
    fig=plt.figure(figsize=(10,5))
    sns.countplot(x=x_element,data=data_selected)
    #sns.barplot(data[x_element],data[y_element])
    plt.xlabel(x_element)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)
    temp2=data_selected[data_selected['avg_price']==data_selected['avg_price'].max()]
    st.subheader('Property with highest selling price')
    st.write(temp2[['property_name','size','region','availability','avg_price','avg_area']])
with col2:
    st.subheader('Pie chart')
    fig=plt.figure()
    fig=plt.figure(figsize=(5,5))
    s = data_selected['size'].value_counts()
    plt.pie(s,labels = s.index, autopct=autopct_format(s))
    plt.legend()
    st.pyplot(fig)
    temp1=data_selected[data_selected['avg_price']==data_selected['avg_price'].min()]
    
    st.subheader('Property with lowest Price')
    st.write(temp1[['property_name','size','region','availability','avg_price','avg_area']])



