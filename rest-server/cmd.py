import disc;
import db;
import logger;
import util;

config = util.getConfig();

global database;
database = "postgres";

async def checkAuth(c) :
    
    if (not disc.checkRoles(c['author']['id'])) : 
        
        await disc.sendMsg(c['channel_id'], "You do not have permission to perform this action.", reference = c['id']);
        return False;
    
    if (not config["Sql"]["discord_terminal"]) :
        
        await disc.sendMsg(c['channel_id'], "Discord SQL queries are not allowed!");
        return False;
        
    return True;

async def sqldb(c, dbname) :
    
    if (not await checkAuth(c)) : return;
        
    global database;
    database = dbname;
    
    await disc.sendMsg(c['channel_id'], "Verifying DB...");
    
    await disc.sendMsg(c['channel_id'], f"Connection object: {db.createConnection(database)}");
    
disc.addCommand(sqldb);

async def sql(c, sql) :
    
    if (not await checkAuth(c)) : return;
    
    logger.log(f"-- SQL executed: {sql}");
    
    await disc.sendMsg(c['channel_id'], db.runSQL(sql, database));

disc.addCommand(sql, plaintext = True);

async def run(c, query) : 
    
    if (not await checkAuth(c)) : return;
    
    logger.log(f"-- SQL Function executed: {sql}");
    
    #-- start assemble arguments tuple
    
    query = query.split("(");
    
    functionName = util.clip(query[0]);
    argumentMappings = db.getFunctionArguments(functionName);
    arguments = [];
    
    query[1] = query[1].replace(")", "");
    query[1] = query[1].split(",");
    
    for argument in query[1] :
    
        argument = argument.split("=");
        
        argumentKey = util.clip(argument[0]);
        
        argumentValue = None;
        
        if ("'" in argument[1]) : argumentValue = util.clip(argument[1].replace("'" , ""));
        else                    : argumentValue = int(argument[1]);
        
        arguments.insert(argumentMappings[argumentKey], argumentValue);
        
    tuple(arguments);
    
    #-- end assemble arguments tuple 
    
    await disc.sendMsg(c['channel_id'], f"Running function {functionName} in {database}");
    
    connection = db.createConnection(database);
    
    #execute function 
    await disc.sendMsg(c['channel_id'], db.runFunction(functionName, arguments, database, connection = connection));

disc.addCommand(run, plaintext = True);

async def recache() : db.cacheFunctions()
disc.addCommand(recache)