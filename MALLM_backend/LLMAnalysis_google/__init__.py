# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import google.generativeai as gemini_client
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY= os.environ['GOOGLE_API_KEY']
gemini_client.configure(api_key=GOOGLE_API_KEY)

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
model = gemini_client.GenerativeModel('gemini-pro',safety_settings=safety_settings)

def extract_text(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
    req = Request(url,headers=hdr)
    

    html = urlopen(req).read()
    soup = BeautifulSoup(html, features="html.parser",from_encoding="utf-8-sig")
    #kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
   # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print('-----start')
    #print(text)
    print('------enrd')
    return text

def analysis(text,company):
    prompt='Assume you are the owner of the company '+company+ '. The below text contains some information about your company. You have to Analyse if the text has any negative content regarding your company. If there is any negative content you will summarize it and just respond with the summary and if there isn\'t any negative content you will just respond with the text None. \nThe text:\n'
    prompt+=text+'\n\nYour response?\n\n Note: If the answer is None, then refrain from introducing additonal text.'
    response = model.generate_content(prompt)
    print('-----startb')
    print(response.text)
    print('-------stop')
    if "none" in response.text.lower() and len(response.text)<7:
        return 'none'
    
    return(response.text)
    



def main(load):

    text=extract_text(load['url'])
    analysed_text = analysis(text,load['company'])
    payload={'url':load['url'],'Analysis':analysed_text}
    return payload
   
    
    

