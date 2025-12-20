import psycopg2;
import util;
import logger;
import os;
import json;

config = util.getConfig();

functions = {};

def functionExists(functionName)          : return functionName in functions;
def getFunctionArguments(functionName)    : return functions[functionName]['arguments'];

def cacheFunctions() :
    
    try :
        
        directory = config["Sql"]["function_dir"];
        databaseDirectories = os.listdir(directory);
        
        print(databaseDirectories);
        
        for databaseDirectory in databaseDirectories :
            
            databaseDirectory = f"{directory}/{databaseDirectory}";
            sqlFiles = os.listdir(databaseDirectory);
            
            print(sqlFiles);
            
            for sqlFilename in sqlFiles : 
                
                functionName = "";
                functionName = sqlFilename.replace(".sql", "");
                functionName = functionName.replace(".arguments", "");
                
                print(functionName);
                
                if (functionName not in functions) : 
                    
                    functions[functionName] = {
                        "sql" : "",
                        "arguments" : {}
                    }
                
                if (".sql" in sqlFilename) : 
                    
                    functions[functionName]['sql'] = open(os.path.join(databaseDirectory, sqlFilename), "r").read();
                
                if (".arguments" in sqlFilename) : 
                    
                    functions[functionName]['arguments'] = json.loads(open(os.path.join(databaseDirectory, sqlFilename), "r").read());
                    
            print(f"{databaseDirectories} functions:");        
            print([function for function in functions]);
        
    except Exception as e : logger.log(f"-- SQL function caching error {e}");

def runFunction(functionName, functionArguments, database, connection = None) : 
    
    function = functions[functionName];
    
    return runSQL(function['sql'], database, arguments = functionArguments, connection = connection);
    
    
def createConnection(database) :
    
    connection = psycopg2.connect (
        dbname = database,
        user = config["Sql"]["user"],
        password = config["Sql"]["password"],
        host = config["Sql"]["host"]
    );
    
    return connection;

def runSQL(sql, database, arguments = None, connection = None,) :
    
    if (not connection) :
        
        #create connection
        connection = psycopg2.connect (
            dbname = database,
            user = config["Sql"]["user"],
            password = config["Sql"]["password"],
            host = config["Sql"]["host"]
        );
    
    #create cursor
    cursor = connection.cursor();
    
    #execute sql
    cursor.execute(sql, arguments);
    
    #gather result
    try    : out = f"Sql result: {cursor.fetchall()}";
    except Exception as e : out = f"Sql warning: {e}";
    
    #cleanup
    connection.commit();
    cursor.close();
    
    return out