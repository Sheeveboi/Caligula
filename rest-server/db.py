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
        
        print(f"directories: \n{databaseDirectories}");
        
        for databaseDirectory in databaseDirectories :
            
            databaseGetDirectory = f"{directory}/{databaseDirectory}/get";
            databasePostDirectory = f"{directory}/{databaseDirectory}/post";
            sqlGetFiles = os.listdir(databaseGetDirectory);
            sqlPostFiles = os.listdir(databasePostDirectory);
            
            print(f"adapter files: \n{sqlGetFiles + sqlPostFiles}");
            
            for sqlFilename in sqlGetFiles + sqlPostFiles : 
                
                functionName = "";
                functionName = sqlFilename.replace(".sql", "");
                functionName = functionName.replace(".arguments", "");
                
                print(f"function: {functionName}");
                
                if (functionName not in functions) : 
                    
                    functions[functionName] = {
                        "sql" : "",
                        "arguments" : {},
                        "method" : "unknown"
                    }
                    
                if (sqlFilename in sqlGetFiles)  : functions[functionName]["method"] = "get";
                if (sqlFilename in sqlPostFiles) : functions[functionName]["method"] = "post";
                
                if (".sql" in sqlFilename) : functions[functionName]['sql'] = open(os.path.join(databaseDirectory, sqlFilename), "r").read();
                    
            print(f"{databaseDirectories} functions:");        
            print([function for function in functions]);
        
    except Exception as e : logger.log(f"-- SQL function caching error {e}");

def runFunction(functionName, functionArguments, database, method, connection = None) : 
    
    function = functions[functionName];
    
    if (method != function["method"]) : return False;
    
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
    
    print(sql);

    try :
        
        #execute sql
        cursor.execute(sql, arguments)
    
        #gather result
        out = cursor.fetchall();
        
    except Exception as e : out = f"Sql warning: {e}";
    
    #cleanup
    connection.commit();
    cursor.close();
    
    return out