# k12InspectorServer

To run the web app directly:
1. Set up Python virtual environment: `python3 -m venv env; source env/bin/activate`.
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the server: `flask run` in the virtual environment.

Alternatively in a tmux instance: 
1. Type tmux, hit enter, do control b, then c (not control c).
2. Launch the virtual environment in tmux: `python3 -m venv env; source env/bin/activate`
3. Run `./test.sh`. 




## Mongo Knowledge 

### What If Mongo stops working 
There are four functions that would be useful here:
- `systemctl start mongod` => Start the the service
- `systemctl status mongod` => Status of the service
- `systemctl restart mongod` => restart the service
- `systemctl reload mongod` => reload the service

My suggestion is to check status (`systemctl status mongod`) and then try starting it again (`systemctl start mongod`)



### Exporting The DB
- First go to the root directory 
    - The line to run is `mongoexport --db database_name --collection <collection_name> --out <output_file>.json` from the base terminal, not the mongo shell
    - Which is: `mongoexport --db testdb --collection test_column --out result2.json`

#### What If I Forgot My DB Info?
To find the info do the following 

1. Open a terminal or command prompt.

2. Navigate to the directory where MongoDB is installed or where the `mongo` shell tool is located.

3. Run the following command to start the MongoDB shell without specifying the URI:
```
mongo
```

This command will start the MongoDB shell and connect to a default MongoDB instance running on the local machine.

4. Once you're in the MongoDB shell, you can list the available databases by running the following command:
```
show databases
```

This command will display a list of databases available on the connected MongoDB instance.

5. Identify the database that contains the collection you want to export.

6. To switch to the desired database, run the following command:
```
use <database_name>
```
   - `<database_name>`: The name of the database you want to switch to.

7. To list the collections in the current database, run the following command:
```
show collections
```

This command will display the collection names present in the current database.

8. Identify the collection contents 

```
db.<collection_name>.find()
```
Or
```
db.<collection_name>.find().pretty()
```

#### What If I Run A Python Script To Export
Run that python script in the background with `nohup python3 mongoExport.py &`.
If you want to stop that script you need to do the following in bash
1. `jobs`
2. `kill %1`