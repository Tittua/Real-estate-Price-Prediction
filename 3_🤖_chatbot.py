import pandas as pd
import pandas as pd
import random
import streamlit as st
from streamlit_chat import message
import time


st.set_page_config()

#importing the data
data=pd.read_csv('final.csv')
data.drop(['Unnamed: 0','location_details'],inplace=True,axis=1)

#Defining all the input/output elements
GREET_INPUTS=('hello','hi','greetings','sup',"what's up",'hey')
GREET_RESPONSES=('hi','hey','nods','hi there','hello',"I'm glad! you are talking to me","Hey I'm Dolly how can i help")
end_greets=('bye','thanks','thank you','bye bye')
end_responses=('BYE!','See You Soon','Good Bye')
type_of_property=('appartment','plot','house','place','plots','houses','home','flat','flats')
house_options=('bhk','house','home','place','place to live')
name=('name','call you') 
hosur_size=('1bhk','2bhk','3bhk','4bhk','5bhk','9bhk','12bhk','open plot')



st.header('ChatBot')
#for storing the chat
# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

#function for getting the input
def get_text():
    with col1:
        input_t=st.text_input('type here for text',value='')
    return input_t

#property details function
def property_details():
    with col2:
        n_rooms=int(st.select_slider('Please select the number of rooms',[1,2,3,4,5,6,9,10,12],label_visibility='visible'))
        n_max_price=st.text_input('Please specify the max budget(In lakhs)',placeholder=int)
        n_min_price=st.text_input('Please specify the min budget(In lakhs)',placeholder=int) 
        time.sleep(4)
        k=data[(data['size']==(str(n_rooms)+' bhk'))&(data['avg_price']>int(n_min_price))&(data['avg_price']<int(n_max_price))]
        if len(k!=0):
            st.write(k.head(5))
        else:
            return 'Sorry There is no Property That Meet your Requirements'    
    return 'no:of rooms selected =  '+str(n_rooms)+'rooms','\n max budget ='+str(n_max_price),'\n min budget='+str(n_min_price)


col1,col2=st.columns([2,3])

#filter algo
def bot(sentence):
    if sentence:
        response=sentence.lower()
        if(response!='bye'or response!='thanks'or response!='thank you'):
            for word in response.split():
                if word.lower() in GREET_INPUTS:
                    return random.choice(GREET_RESPONSES)
                elif word.lower() in type_of_property:
                    return property_details()
                elif word.lower() in end_greets:
                    return random.choice(end_responses)
                elif word.lower() in name:
                    return random.choice(["I'm Dolly",'Its Me Dolly'])

            else:
                return "Sorry I didn't get you"
                    
                    
                    
                    

user_response=get_text()
if user_response:
    #output=greet(user_response)
    output1=bot(user_response)
    st.session_state.past.append(user_response)
    st.session_state.generated.append(output1)


#Output screen
with col1:

    if st.session_state['generated']:
        
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
