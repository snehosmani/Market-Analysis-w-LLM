import streamlit as st
import requests
import time


URL = "http://localhost:7071/api/orchestrators/CompetitorAnalysis"
GoogleGem=0
Cohere=0
st.title('Market Analysis with LLMs')
title = st.text_input('Competitor name', 'Spotify')
options = st.multiselect(
    'Choose LLM model',
    ['Cohere','Google-Gemini Pro'],
    ['Google-Gemini Pro'])
print(options)

if 'Google-Gemini Pro' in options:
    GoogleGem=1
if 'Cohere' in options:
    Cohere=1
#st.write('You selected:', options)

if st.button('Analyze',type="primary"):
    #st.write('Analyzing')
    success=False
    ini_resp = requests.get(url = URL, json = {"name":title,"Model":{"GoogleGem":GoogleGem,"Cohere":Cohere}},
                     )

    ini_json=ini_resp.text
    print(ini_json)
    st.write(ini_json)
    


    # while not success:
    #     final_resp=requests.get(second_uri)
    #     response=final_resp.json()
    #     if response['output'] is None:
    #         time.sleep(5)
    #     else:         
            
    #         print(response['output'])
    #         st.subheader("REPORT!!!")
    #         st.divider()
    #         st.write(response['output'])
    #         success=True
    
