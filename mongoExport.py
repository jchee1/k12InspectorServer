"""
J. Chanenson
6/1/23
Exports mongo DB
"""
from pymongo import MongoClient
import pandas as pd
# import pdmongo as pdm
from tqdm import tqdm
from datetime import datetime



def main():
    # uri = "mongodb://localhost:27017"
    # client = MongoClient(uri)
    # db = client['testdb']
    # collection = db['test_column']

    # print("Connected to DB")

    # df = pdm.read_mongo("test_column", [], "mongodb://localhost:27017/testdb")

    # gc.collect()

    # df = pd.DataFrame(list(collection.find()))

    # df = pd.DataFrame.from_records(collection.find())


    df = read_mongo("testdb", "test_column")
    print("Done")

    # df.to_csv('export_all.csv', mode='a', index=False)



def read_mongo(db, 
           collection, query={}, 
           host='localhost', port=27017, 
           username=None, password=None,
           chunksize = 100, no_id=True):
    """ Read from Mongo and Store into DataFrame """


    # Connect to MongoDB
    #db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    client = MongoClient(host=host, port=port)
    # Make a query to the specific DB and Collection
    db_aux = client[db]
    print("Set up db params")

    # Some variables to create the chunks
    # skips_variable = range(0, db_aux[collection].find(query).count(), int(chunksize))
    skips_variable = range(0, db_aux[collection].count_documents(query), int(chunksize))
    print("Connected to db")
    if len(skips_variable)<=1:
        skips_variable = [0,len(skips_variable)]

    print("Created chunk sizes")

    # Iteration to create the dataframe in chunks.
    for i in range(1,len(skips_variable)):

        # Expand the cursor and construct the DataFrame
        try:
            df_aux =pd.DataFrame(list(db_aux[collection].find(query)[skips_variable[i-1]:skips_variable[i]]))
        except:
            dead = f" || Query failed. Current skip {skips_variable[i-1]} {skips_variable[i]}"
            updateProgress(i, len(skips_variable), died = dead)

        if no_id:
            del df_aux['_id']
        
        if i % 50 == 0:
            updateProgress(i, len(skips_variable))
            
        if i == 1:
            df_aux.to_csv('export_all2.csv', mode='a', index=False)
            print("Started Export")
        else:
            df_aux.to_csv('export_all2.csv', mode='a', index=False, header=False)

        # # Concatenate the chunks into a unique df
        # if 'df' not in locals():
        #     df =  df_aux
        # else:
        #     # df = pd.concat([df, df_aux], ignore_index=True)

    return "done"

def updateProgress(currStep, total, died = ""):
    """
    Silly function that writes to txt file the time and what step we are on. I do this so I can run this pythonfile detached
    """
    ## Print to file
    with open("mongoExportStatus.txt", "w") as file:
        status = f" Currently on step {currStep} out of {total} | {(currStep/total)*100:.0f}%"
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        file.write(formatted_datetime + status + died)
    
    ##Output to log via nohup
    ## To kill do in bash `jobs` `then kill %1`
    # status = f" Currently on step {currStep} out of {total} | {(currStep/total)*100:.0f}%"
    # current_datetime = datetime.now()
    # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # print(formatted_datetime + status + died)




main()