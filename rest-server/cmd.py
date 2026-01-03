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
    
    out = db.runSQL(sql, database);
    print(out);
    
    await disc.sendMsg(c['channel_id'], str(out));

disc.addCommand(sql, plaintext = True);

async def recache(c) : db.cacheFunctions()
disc.addCommand(recache)
