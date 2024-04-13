import azure.functions as func
import azure.durable_functions as df
import logging
import traceback


def orchestrator_function(context: df.DurableOrchestrationContext):
    try :
        #initializing variables for retry mechanism
        first_retry_interval_in_milliseconds = 5000
        max_number_of_attempts = 3
        #back_of_coeff=3
        retry_options = df.RetryOptions(first_retry_interval_in_milliseconds, max_number_of_attempts)

        #loading user json data
        userInput: str = context.get_input()
        #calling activity function SearchArticles which returns list of urls to be analysed by dooing a Google Search
        searchURLs=yield context.call_activity_with_retry("SearchArticles",retry_options, userInput['name'])
        #variabke that will hold the return results
        ret_analysis=''
        count_analysis=0  #deceiding variable of the return stmt

        #Based on moodel selected, respective activity functions are called simaltaneously in a round robin fashion
        if userInput['Model']['GoogleGem'] ==1:
            tasks,tasks_1 =[],[]
            sendAlert=0
            print('No.of URLS: ',len(searchURLs))
            #round robin
            for i in range(len(searchURLs)):
                if i%2==0:
                    load={"company":userInput['name'],"url":searchURLs[i]}
                    tasks.append(context.call_activity_with_retry("LLMAnalysis_google",retry_options, load))
                    print('------------------------------------')
                    print(f'Assigned {i}th URL to Google Engine 1')
                    print('------------------------------------')
                else:
                    load={"company":userInput['name'],"url":searchURLs[i]}
                    tasks_1.append(context.call_activity_with_retry("LLMAnalysis_google_1",retry_options, load))
                    print('------------------------------------')
                    print(f'Assigned {i}th URL to Google Engine 2')
                    print('------------------------------------')
            results = yield context.task_all(tasks) #results from Gemini-Pro instance 1
            results_1 = yield context.task_all(tasks_1) ##results from Gemini-Pro instance 2
            results.extend(results_1) 
            # ret_analysis.extend(results)

            # for item in results:
            #     if item['Analysis']!="none":
            #         count_analysis+=1
            #         break
            #     else:
            #         continue
            # # print(results)
            # email will be triggered only if there is some analysis
            for item in results:
                if item['Analysis']!="none":
                    sendAlert=1
                    break
                else:
                    continue
            
            if sendAlert==1:
                load={"results":results,"model":"Google Gemini Pro"}
                analysis=yield context.call_activity_with_retry("Alert",retry_options, load)
                count_analysis+=1
                ret_analysis+=analysis
        #same as above, but for Cohere models
        if userInput['Model']['Cohere'] ==1:
            tasks,tasks_1 =[],[]
            sendAlert=0
            print('No.of URLS: ',len(searchURLs))
            for i in range(len(searchURLs)):
                if i%2==0:
                    load={"company":userInput['name'],"url":searchURLs[i]}
                    tasks.append(context.call_activity_with_retry("LLMAnalysis",retry_options, load))
                    print('------------------------------------')
                    print(f'Assigned {i}th URL to Cohere Engine 1')
                    print('------------------------------------')
                else:
                    load={"company":userInput['name'],"url":searchURLs[i]}
                    tasks_1.append(context.call_activity_with_retry("LLMAnalysis_1",retry_options, load))
                    print('------------------------------------')
                    print(f'Assigned {i}th URL to Cohere Engine 2')
                    print('------------------------------------')
            results = yield context.task_all(tasks)
            results_1 = yield context.task_all(tasks_1)
            results.extend(results_1)
            # ret_analysis.extend(results)
            # #print(results)

            # for item in results:
            #     if item['Analysis']!="none":
            #         count_analysis+=1
            #         break
            #     else:
            #         continue

            for item in results:
                if item['Analysis']!="none":
                    sendAlert=1
                    break
                else:
                    continue
            
            if sendAlert==1:
                load={"results":results,"model":"Cohere"}
                analysis=yield context.call_activity_with_retry("Alert",retry_options, load)
                count_analysis+=1
                ret_analysis+=analysis
        
        if(count_analysis==0):
            return "No Negative Content found in the past 1 year"
        else:
            return ret_analysis




        
    except Exception as e:
        logging.error(traceback.format_exc())
        raise Exception(f'Oops!!! Encounterd an Internal Error, Please check logs')
    


main = df.Orchestrator.create(orchestrator_function)