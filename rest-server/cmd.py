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
    query[1] = query[1].replace(")", "");
    
    functionName = util.clip(query[0]);
    arguments = [];
    
    argumentMappings = db.getFunctionArguments(functionName);
    argumentPairs = util.parseArgumentQuery(query[1])
    
    print(argumentPairs);
    
    for argument in argumentPairs :
    
        mapping = argumentMappings[argument]
        
        arguments.insert(mapping, argumentPairs[argument]);
    
    #-- end assemble arguments tuple 
    
    await disc.sendMsg(c['channel_id'], f"Running function {functionName} in {database}");
    
    connection = db.createConnection(database);
    
    #execute function 
    await disc.sendMsg(c['channel_id'], db.runFunction(functionName, arguments, database, connection = connection));

disc.addCommand(run, plaintext = True);

async def recache(c) : db.cacheFunctions()
disc.addCommand(recache)
