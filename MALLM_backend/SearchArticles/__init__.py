# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
load_dotenv()

CUSTOM_API_KEY= os.environ['CUSTOM_SEARCH_API_1']

def main(query: str):
    ''' This is an activity function which returns relevant urls from past 1 year form google search api for the query passed.
    Input -> query(string)
    Output ->List of URL's
    '''
    service = build(
        "customsearch", "v1", developerKey=CUSTOM_API_KEY
    )
    #old "47277e31ddb064b72" 644edb1529def47cf
    res = (
        service.cse()
        .list(
            q=query,
            cx="644edb1529def47cf", 
            dateRestrict="y1",

        )
        .execute()
    )
    #pprint.pprint(res)
    urls=[]
    for i in range(len(res['items'])):
        urls.append(res['items'][i]['link'])
        print(urls)
    return urls

